#!/usr/bin/env python3
"""Check that every field in the OpenPIA schemas has a type, a description and a constraint.

Implements the rule in docs/field-completeness.md. Standard library only.

Usage:
    python3 tools/check_field_completeness.py                    # summary + failures, exit 1 if any
    python3 tools/check_field_completeness.py --report           # full per-field table
    python3 tools/check_field_completeness.py --json             # machine-readable
    python3 tools/check_field_completeness.py --write-baseline tools/field-completeness-baseline.json
    python3 tools/check_field_completeness.py --baseline tools/field-completeness-baseline.json
                                                                 # ratchet: fail only on NEW gaps
"""
from __future__ import annotations

import argparse
import json
import os
import sys

# --- what counts as a constraint, per declared type -------------------------
STRING_CONSTRAINTS = {"enum", "const", "pattern", "format", "maxLength", "minLength"}
NUMERIC_CONSTRAINTS = {
    "enum", "const", "minimum", "maximum",
    "exclusiveMinimum", "exclusiveMaximum", "multipleOf",
}
ARRAY_REQUIRED = {"items", "prefixItems"}
ARRAY_BOUNDS = {"minItems", "maxItems"}
OBJECT_CONSTRAINTS = {"additionalProperties", "unevaluatedProperties"}
POLYMORPHIC_CONSTRAINTS = {"anyOf", "oneOf", "enum", "const"}

DEFAULT_SCHEMAS = [
    "schema/v0.1/a55a.schema.json",
    "schema/v0.1/a55b.schema.json",
]

# JSON Schema keywords whose values are schema maps keyed by name, not schemas themselves.
SCHEMA_MAP_KEYWORDS = {"properties", "$defs", "definitions", "patternProperties"}


class Loader:
    """Loads the schema documents and resolves local + relative-file $refs."""

    def __init__(self, root: str, relpaths: list[str]) -> None:
        self.root = root
        self.docs: dict[str, dict] = {}
        for rel in relpaths:
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                self.docs[os.path.normpath(rel)] = json.load(fh)

    def resolve(self, ref: str, curfile: str):
        filepart, _, pointer = ref.partition("#")
        if filepart:
            target = os.path.normpath(os.path.join(os.path.dirname(curfile), filepart))
        else:
            target = curfile
        if target not in self.docs:
            raise KeyError(f"$ref target not loaded: {target}")
        node = self.docs[target]
        for seg in (s for s in pointer.split("/") if s):
            node = node[seg.replace("~1", "/").replace("~0", "~")]
        return node, target

    def effective(self, subschema: dict, curfile: str, depth: int = 0) -> dict:
        """Merge a subschema with its $ref target so $ref'd descriptions/constraints count."""
        merged = dict(subschema)
        ref = subschema.get("$ref")
        if ref and depth < 8:
            try:
                target, targetfile = self.resolve(ref, curfile)
            except (KeyError, TypeError):
                return merged
            for key, value in self.effective(target, targetfile, depth + 1).items():
                merged.setdefault(key, value)
        return merged


def declared_types(schema: dict) -> set[str]:
    raw = schema.get("type")
    if raw is None:
        if "const" in schema:
            return {"__const__"}
        if "enum" in schema:
            return {"__enum__"}
        return set()
    return set(raw) if isinstance(raw, list) else {raw}


def branches_are_typed(schema: dict, loader=None, curfile=None) -> bool:
    """True when a polymorphic field states its value space as typed anyOf/oneOf branches.

    A branch that is a $ref is typed when its target is typed, so resolve refs when a
    loader is supplied (the generator emits nullable unions as anyOf[$ref, {type:null}])."""
    def branch_types(b):
        if loader is not None and curfile is not None:
            b = loader.effective(b, curfile)
        return declared_types(b)
    for keyword in ("anyOf", "oneOf"):
        branches = schema.get(keyword)
        if isinstance(branches, list) and branches and all(
            isinstance(b, dict) and branch_types(b) for b in branches
        ):
            return True
    return False


def check_constraint(schema: dict) -> tuple[bool, str]:
    """Return (satisfied, explanation) for the constraint dimension."""
    types = declared_types(schema)
    if types & {"__const__", "__enum__"}:
        return True, "enum/const"
    concrete = types - {"null"}
    if not concrete:
        hits = POLYMORPHIC_CONSTRAINTS & schema.keys()
        if hits:
            return True, ",".join(sorted(hits))
        return False, "untyped: needs anyOf/oneOf/enum"

    satisfied: list[str] = []
    missing: list[str] = []
    for jtype in sorted(concrete):
        if jtype == "boolean":
            satisfied.append("boolean: type is the constraint")
        elif jtype == "string":
            hits = STRING_CONSTRAINTS & schema.keys()
            (satisfied if hits else missing).append(
                ",".join(sorted(hits)) if hits
                else "string: needs enum/pattern/format/maxLength"
            )
        elif jtype in ("integer", "number"):
            hits = NUMERIC_CONSTRAINTS & schema.keys()
            (satisfied if hits else missing).append(
                ",".join(sorted(hits)) if hits
                else f"{jtype}: needs minimum/maximum/enum/multipleOf"
            )
        elif jtype == "array":
            hits = (ARRAY_REQUIRED & schema.keys(), ARRAY_BOUNDS & schema.keys())
            if hits[0] and hits[1]:
                satisfied.append(",".join(sorted(hits[0] | hits[1])))
            elif not hits[0]:
                missing.append("array: needs items")
            else:
                missing.append("array: needs minItems/maxItems")
        elif jtype == "object":
            hits = OBJECT_CONSTRAINTS & schema.keys()
            (satisfied if hits else missing).append(
                ",".join(sorted(hits)) if hits
                else "object: needs additionalProperties"
            )
        else:
            satisfied.append(f"{jtype}: no constraint keywords defined")
    if missing:
        return False, "; ".join(missing)
    return True, "; ".join(satisfied)


def audit(loader: Loader) -> tuple[list[dict], list[dict]]:
    fields: dict[tuple[str, str], dict] = {}
    defs: list[dict] = []

    def walk(node, curfile: str, path: str) -> None:
        if not isinstance(node, dict):
            return
        props = node.get("properties")
        required = set(node.get("required", []))
        if isinstance(props, dict):
            for name, sub in props.items():
                if not isinstance(sub, dict):
                    continue
                merged = loader.effective(sub, curfile)
                types = declared_types(merged)
                has_type = (
                    bool(types - {"null"})
                    or bool(types & {"__const__", "__enum__"})
                    or branches_are_typed(merged, loader, curfile)
                )
                has_desc = bool(merged.get("description"))
                ok_con, why = check_constraint(merged)
                fieldpath = f"{path}.{name}" if path else name
                fields[(curfile, fieldpath)] = {
                    "file": curfile,
                    "path": fieldpath,
                    "field": name,
                    "types": ",".join(sorted(types)) or "(none)",
                    "type_ok": has_type,
                    "description_ok": has_desc,
                    "description_inherited": has_desc and not sub.get("description"),
                    "constraint_ok": ok_con,
                    "constraint_detail": why,
                    "ref": sub.get("$ref"),
                    "required": name in required,
                    "nullable": "null" in types,
                }
        for key, value in node.items():
            if key in {"$ref", "not", "if", "then", "else"}:
                continue
            if isinstance(value, dict):
                if key in SCHEMA_MAP_KEYWORDS:
                    for subname, subschema in value.items():
                        walk(subschema, curfile, f"{path}.{subname}" if path else subname)
                else:
                    walk(value, curfile, f"{path}.{key}" if path else key)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        walk(item, curfile, f"{path}.{key}[{index}]" if path else f"{key}[{index}]")

    for relpath, doc in loader.docs.items():
        walk(doc, relpath, "")
        for name, subschema in (doc.get("$defs") or {}).items():
            if isinstance(subschema, dict):
                defs.append({
                    "file": relpath,
                    "name": name,
                    "description_ok": bool(subschema.get("description")),
                })

    return list(fields.values()), defs


def key_of(row: dict) -> str:
    return f"{row['file']}#{row['path']}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--schema", action="append", dest="schemas",
                        help="schema file (repeatable); defaults to the v0.1 set")
    parser.add_argument("--report", action="store_true", help="print the full per-field table")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--baseline", help="ratchet against a baseline; fail only on new gaps")
    parser.add_argument("--write-baseline", help="write the current gaps as a baseline and exit 0")
    args = parser.parse_args()

    loader = Loader(args.root, args.schemas or DEFAULT_SCHEMAS)
    fields, defs = audit(loader)

    total = len(fields)
    def is_complete(row: dict) -> bool:
        return row["type_ok"] and row["description_ok"] and row["constraint_ok"]

    complete = [f for f in fields if is_complete(f)]
    gaps = [f for f in fields if not is_complete(f)]
    def_gaps = [d for d in defs if not d["description_ok"]]

    if args.write_baseline:
        baseline = {
            "note": "Fields not yet meeting docs/field-completeness.md. This list may only shrink.",
            "fields": sorted(key_of(f) for f in gaps),
            "defs": sorted(f"{d['file']}#/$defs/{d['name']}" for d in def_gaps),
        }
        with open(args.write_baseline, "w", encoding="utf-8") as fh:
            json.dump(baseline, fh, indent=2)
            fh.write("\n")
        print(f"wrote baseline: {args.write_baseline} "
              f"({len(baseline['fields'])} fields, {len(baseline['defs'])} $defs)")
        return 0

    if args.json:
        json.dump({"fields": fields, "defs": defs}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        def pct(n: int) -> str:
            return f"{n}/{total} ({100 * n // total if total else 0}%)"

        print("OpenPIA field completeness — type + description + constraint\n")
        print(f"  fields audited      {total}")
        print(f"  has type            {pct(sum(f['type_ok'] for f in fields))}")
        print(f"  has description     {pct(sum(f['description_ok'] for f in fields))}")
        print(f"  has constraint      {pct(sum(f['constraint_ok'] for f in fields))}")
        print(f"  complete            {pct(len(complete))}")
        print(f"  $defs missing desc  {len(def_gaps)}/{len(defs)}\n")

        width = max([28] + [len(p) for p in loader.docs]) + 2
        header = f"{'file':<{width}}{'n':>5}{'type':>6}{'desc':>6}{'cons':>6}{'ok':>6}"
        print(header)
        print("-" * len(header))
        for relpath in loader.docs:
            rows = [f for f in fields if f["file"] == relpath]
            if not rows:
                continue
            print(f"{relpath:<{width}}{len(rows):>5}"
                  f"{sum(r['type_ok'] for r in rows):>6}"
                  f"{sum(r['description_ok'] for r in rows):>6}"
                  f"{sum(r['constraint_ok'] for r in rows):>6}"
                  f"{sum(is_complete(r) for r in rows):>6}")

        if args.report:
            print("\nper-field detail")
            for row in sorted(fields, key=lambda r: (r["file"], r["path"])):
                flags = "".join([
                    "T" if row["type_ok"] else "-",
                    "D" if row["description_ok"] else "-",
                    "C" if row["constraint_ok"] else "-",
                ])
                print(f"  {flags}  {row['file']}#{row['path']}  [{row['types']}]")

        if gaps:
            print(f"\nincomplete fields ({len(gaps)}):")
            for row in sorted(gaps, key=lambda r: (r["file"], r["path"])):
                missing = []
                if not row["type_ok"]:
                    missing.append("type")
                if not row["description_ok"]:
                    missing.append("description")
                if not row["constraint_ok"]:
                    missing.append(f"constraint ({row['constraint_detail']})")
                print(f"  {row['file']}#{row['path']}: missing {', '.join(missing)}")
        if def_gaps:
            print(f"\n$defs without a description ({len(def_gaps)}):")
            for d in sorted(def_gaps, key=lambda x: (x["file"], x["name"])):
                print(f"  {d['file']}#/$defs/{d['name']}")

    if args.baseline:
        with open(args.baseline, encoding="utf-8") as fh:
            baseline = json.load(fh)
        allowed_fields = set(baseline.get("fields", []))
        allowed_defs = set(baseline.get("defs", []))
        new_fields = sorted(key_of(f) for f in gaps if key_of(f) not in allowed_fields)
        new_defs = sorted(
            f"{d['file']}#/$defs/{d['name']}" for d in def_gaps
            if f"{d['file']}#/$defs/{d['name']}" not in allowed_defs
        )
        fixed = len(allowed_fields) - len([f for f in gaps if key_of(f) in allowed_fields])
        if new_fields or new_defs:
            print("\nFAIL — new gaps not present in the baseline:")
            for k in new_fields + new_defs:
                print(f"  {k}")
            print("\nAdd a type, description and constraint, or update the baseline deliberately.")
            return 1
        print(f"\nOK — no new gaps. {fixed} baseline entries now fixed "
              f"({len(allowed_fields) + len(allowed_defs)} remaining in baseline).")
        return 0

    if gaps or def_gaps:
        print(f"\nFAIL — {len(gaps)} incomplete fields, {len(def_gaps)} undescribed $defs.")
        return 1
    print("\nOK — every field has a type, a description and a constraint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
