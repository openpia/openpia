# Contributing to OpenPIA

This working draft is only as good as the real-world workflow knowledge behind it — from planning, build/field, and software/GIS alike.

## Right now (early stage)

OpenPIA is in early design, focused on **A55a — reactive works** first. The most useful help at this stage is a direct conversation about how the schema matches real A55a/A55b practice.

**Until v1.0, feedback is by direct review, not public issues:**

- **Email [feedback@openpia.org](mailto:feedback@openpia.org)** — a field is missing, wrong, or ambiguous; an evidence prompt or icon doesn't match what you see in the field; or a challenge to a past decision. No GitHub account needed.
- **Join a review** — ask at the same address. Practitioner reviewers are invited to the repository, where their issues are visible to everyone.

**From v1.0**, public GitHub issues and pull requests open to anyone:

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

The normative schema files under `schema/v0.1/` are generated from OpenPIA's canonical rule set and copied into the repo, so a schema-shape change is proposed (by email to feedback@openpia.org pre-1.0, as an issue from v1.0) and lands through regeneration rather than by hand-editing the JSON.

## Before you open a PR

For invited reviewers now, and everyone from v1.0. The same checks CI runs:

```sh
python3 tools/check_field_completeness.py    # type + description + constraint on every field
python3 tools/sync_slot_codes.py --check     # slotCode enum matches evidence/slots.json
uv run tools/validate_examples.py            # examples still validate
python3 tools/check_icons.py                 # every infrastructure type has an icon
```

All but `validate_examples.py` need nothing but Python 3.11+. The third needs `jsonschema>=4.18` — `uv run` provisions it for you, or `pip install -r tools/requirements.txt` if you'd rather manage it yourself.

The evidence taxonomy lives in `slots.json`; the `slotCode` enum in the schemas is generated from it and verified by `python3 tools/sync_slot_codes.py --check`. Propose taxonomy changes against the registry, not the enum.

## Recognition

Contributions are credited. When a field or workflow step exists because someone raised it, the changelog and release notes say so.
