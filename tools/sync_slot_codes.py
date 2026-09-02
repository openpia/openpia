#!/usr/bin/env python3
"""Verify the inline slotCode enum in each notice schema matches evidence/slots.json.

    python3 tools/sync_slot_codes.py            # verify; exit 1 if out of step
    python3 tools/sync_slot_codes.py --check    # same (kept for CI compatibility)

The registry in evidence/slots.json is the source of truth; the enum exists so an
unknown slot_code fails plain schema validation, not only the rules engine. The
schemas are produced by the external generator, so this tool only checks — it never
writes into them.
"""
from __future__ import annotations

import argparse
import json
import sys

SLOTS = "schema/v0.1/evidence/slots.json"
SCHEMAS = [
    "schema/v0.1/a55a.schema.json",
    "schema/v0.1/a55b.schema.json",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify only (default); kept for CI compatibility")
    parser.add_argument("--slots", default=SLOTS)
    parser.add_argument("--schemas", nargs="*", default=SCHEMAS)
    args = parser.parse_args()

    with open(args.slots, encoding="utf-8") as fh:
        codes = sorted(json.load(fh)["registry"])

    ok = True
    for schema_path in args.schemas:
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
        current = schema.get("$defs", {}).get("slotCode", {}).get("enum")
        if current is None:
            print(f"FAIL — {schema_path} has no $defs.slotCode.enum.")
            ok = False
            continue
        if current == codes:
            print(f"OK   {schema_path}: slotCode enum in step with the registry ({len(codes)} codes).")
            continue
        ok = False
        added = [c for c in codes if c not in current]
        removed = [c for c in current if c not in codes]
        print(f"FAIL — {schema_path}: slotCode enum out of step with {args.slots}.")
        if added:
            print(f"  in the registry, missing from the enum: {', '.join(added)}")
        if removed:
            print(f"  in the enum, missing from the registry: {', '.join(removed)}")

    if not ok:
        print("The schemas are generated externally; regenerate them from the registry.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
