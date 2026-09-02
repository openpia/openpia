# Contributing to OpenPIA

This standard is only as good as the real-world workflow knowledge behind it — from planning, build/field, and software/GIS alike.

## Right now (early stage)

OpenPIA is in early design, focused on **A55a — reactive works** first. The most useful help at this stage is a direct conversation about how the schema matches real A55a/A55b practice. As the project opens up, contribution moves to GitHub in the open:

- **Issues** — a field is missing, wrong, or ambiguous; or a challenge to a past decision.
- **Pull requests** — concrete changes to the schema or docs, referencing an issue first so the discussion is public.

## What makes good input

- **Concrete beats abstract.** "We can't photograph a collapsed box well enough to avoid rejection" is worth more than "the evidence handling is weak."
- **Say which world you're in** — planning, build/field, or software/GIS. The same blockage looks different from each.
- **Field-safe.** Keep feedback about tooling and workflow, not about identifiable people, sites, or performance.

## Schema changes

For changes to the schema, note whether it's a PATCH, MINOR, or MAJOR change (see [`GOVERNANCE.md`](GOVERNANCE.md)) and add a line to [`CHANGELOG.md`](CHANGELOG.md).

**Every field needs a type, a description and a constraint** — the rule is in [`docs/field-completeness.md`](docs/field-completeness.md), and CI enforces it, so a new field without all three won't merge. The description conventions are in that doc; keep them short and in the same voice as their neighbours.

Remember that objects are closed (`additionalProperties: false`), so adding a field is a schema change rather than something a producer can do on its own side. That is the point — see the [spec conventions](spec/v0.1/README.md#conventions).

The normative schema files under `schema/v0.1/` are generated from OpenPIA's canonical rule set and copied into the repo, so a schema-shape change is proposed as an issue and lands through regeneration rather than by hand-editing the JSON.

## Before you open a PR

The same three checks CI runs:

```sh
python3 tools/check_field_completeness.py    # type + description + constraint on every field
python3 tools/sync_slot_codes.py --check     # slotCode enum matches evidence/slots.json
uv run tools/validate_examples.py            # examples still validate
```

The first two need nothing but Python 3.11+. The third needs `jsonschema>=4.18` — `uv run` provisions it for you, or `pip install -r tools/requirements.txt` if you'd rather manage it yourself.

The evidence taxonomy lives in `slots.json`; the `slotCode` enum in the schemas is generated from it and verified by `python3 tools/sync_slot_codes.py --check`. Propose taxonomy changes against the registry, not the enum.

## Recognition

Contributions are credited. When a field or workflow step exists because someone raised it, the changelog and release notes say so.
