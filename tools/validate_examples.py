#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.18"]
# ///
"""Check the schemas are valid, then validate the example submissions against them.

Two passes:

1. **Meta-schema** — every schema that declares a `$schema` is checked against JSON Schema
   2020-12 itself, so a typo'd keyword or a malformed construct is caught here rather than
   silently doing nothing at validation time.
2. **Examples** — each example is validated against its schema.

`$ref`s resolve from disk. The schemas carry absolute `$id` URLs under https://openpia.org/,
so a relative `$ref` resolves against that base and a validator left to itself tries to
resolve those `$id`s over the network — which would make CI depend on the
website serving the schema files. A registry built from the local files avoids that.

    uv run tools/validate_examples.py        # provisions jsonschema itself, no venv needed
    python3 tools/validate_examples.py       # needs jsonschema>=4.18 already installed
"""
from __future__ import annotations

import glob
import json
import sys

MIN_JSONSCHEMA = "4.18"

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:
    try:
        from importlib.metadata import version

        installed = version("jsonschema")
    except Exception:
        installed = None
    if installed is None:
        sys.exit(
            f"jsonschema>={MIN_JSONSCHEMA} is required and is not installed.\n"
            "  uv run tools/validate_examples.py   (provisions it automatically)\n"
            "  pip install 'jsonschema>=4.18'      (or use a virtual environment)"
        )
    sys.exit(
        f"jsonschema {installed} is installed but too old — "
        f"{MIN_JSONSCHEMA} or newer is required.\n"
        "The `referencing` library this script builds its registry on arrived in "
        "jsonschema 4.18.\n"
        "  uv run tools/validate_examples.py   (ignores the system version entirely)\n"
        "  pip install --upgrade 'jsonschema>=4.18'"
    )

SCHEMA_GLOB = "schema/v0.1/**/*.json"
PAIRS = [
    ("schema/v0.1/a55a.schema.json", "examples/v0.1/a55a.example.json"),
    ("schema/v0.1/a55b.schema.json", "examples/v0.1/a55b.example.json"),
]


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def build_registry() -> Registry:
    """Register every local schema under its own $id, so relative $refs resolve offline."""
    registry = Registry()
    for path in glob.glob(SCHEMA_GLOB, recursive=True):
        doc = load(path)
        if not isinstance(doc, dict) or "$id" not in doc:
            continue
        # The data registries (slots, rules, infrastructure map) carry an $id but no
        # $schema, so the dialect has to be supplied rather than detected.
        resource = Resource.from_contents(doc, default_specification=DRAFT202012)
        registry = registry.with_resource(doc["$id"], resource)
    return registry


def check_schemas() -> int:
    """Validate every declared schema against the 2020-12 meta-schema. Returns a failure count."""
    failures = 0
    for path in sorted(glob.glob(SCHEMA_GLOB, recursive=True)):
        doc = load(path)
        if not isinstance(doc, dict) or "$schema" not in doc:
            # Data registries (slots, rules, infrastructure map) carry an $id but no
            # $schema — they are catalogues, not schemas, so there is nothing to check.
            continue
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as error:
            failures += 1
            print(f"FAIL {path} is not a valid 2020-12 schema")
            print(f"  {error}")
        else:
            print(f"OK   {path} is a valid 2020-12 schema")
    return failures


def main() -> int:
    schema_failures = check_schemas()
    if schema_failures:
        print(f"\n{schema_failures} invalid schema(s) — not validating examples against them.")
        return 1

    registry = build_registry()
    failures = 0
    for schema_path, example_path in PAIRS:
        schema = load(schema_path)
        validator = Draft202012Validator(schema, registry=registry)
        errors = sorted(
            validator.iter_errors(load(example_path)),
            key=lambda e: list(e.absolute_path),
        )
        if errors:
            failures += len(errors)
            print(f"FAIL {example_path} against {schema_path}")
            for error in errors:
                location = "/".join(str(p) for p in error.absolute_path) or "(root)"
                print(f"  {location}: {error.message}")
        else:
            print(f"OK   {example_path} against {schema_path}")
    if failures:
        print(f"\n{failures} validation error(s).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
