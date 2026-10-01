#!/usr/bin/env python3
"""Check the icon library against the infrastructure map.

- every type in schema/v0.1/common/infrastructure-map.json has an entry in
  assets/icons/icons.json "types" (and "types" holds nothing else);
- every file icons.json names exists;
- every SVG in assets/icons/ is referenced by icons.json;
- every SVG is 104 units high (viewBox "0 0 W 104"), with width/height
  attributes matching the viewBox so it renders at its native size.

Standard library only. Exit 1 on any problem.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "assets" / "icons"
MAP = ROOT / "schema" / "v0.1" / "common" / "infrastructure-map.json"


def main() -> int:
    index = json.loads((ICONS / "icons.json").read_text())
    height = index.get("height", 104)
    types = {k: v for k, v in index["types"].items() if not k.startswith("$")}
    extras = {k: v for k, v in index.get("extras", {}).items() if not k.startswith("$")}
    schema_types = set(json.loads(MAP.read_text())["type_to_category"])

    errors = []
    for code in sorted(schema_types - set(types)):
        errors.append(f"schema type '{code}' has no icon in icons.json 'types'")
    for code in sorted(set(types) - schema_types):
        errors.append(f"icons.json 'types' has '{code}', which is not a schema type (move it to 'extras')")
    for code in sorted(set(types) & set(extras)):
        errors.append(f"'{code}' is in both 'types' and 'extras'")

    referenced = set(types.values()) | set(extras.values())
    for name in sorted(referenced):
        if not (ICONS / name).is_file():
            errors.append(f"icons.json names '{name}', which does not exist")
    on_disk = {p.name for p in ICONS.glob("*.svg")}
    for name in sorted(on_disk - referenced):
        errors.append(f"'{name}' is not referenced by icons.json")

    for name in sorted(on_disk):
        m = re.search(r'viewBox="0 0 [\d.]+ ([\d.]+)"', (ICONS / name).read_text())
        if not m or float(m.group(1)) != height:
            errors.append(f"'{name}' viewBox height is not {height}")
        svg = (ICONS / name).read_text()
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
        if vb and not (re.search(rf'<svg[^>]*\swidth="{vb[1]}"', svg) and re.search(rf'<svg[^>]*\sheight="{vb[2]}"', svg)):
            errors.append(f"'{name}' width/height attributes must match viewBox {vb[1]} x {vb[2]}")

    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        return 1
    print(f"OK  {len(types)} schema types + {len(extras)} extras -> {len(on_disk)} icons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
