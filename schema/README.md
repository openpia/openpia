# Schema

The OpenPIA JSON Schema for Openreach PIA **A55**, organised by version.

> The `v0.1/*.json` schema files are generated from OpenPIA's canonical rule set and copied into the repo. Treat them as build output: propose changes through the registry/spec, not by hand-editing the JSON.

- [`v0.1/a55a.schema.json`](v0.1/a55a.schema.json) — **point-based** reactive works. `submission_type: a55a`, required `job_type`.
- [`v0.1/a55b.schema.json`](v0.1/a55b.schema.json) — **stage/workflow-based** civil evidence. `submission_type: a55b`, required `stage`. Linked to its parent A55a by `parent_submission_uid` (each record carries its own `submission_uid`).
- [`v0.1/common/infrastructure-map.json`](v0.1/common/infrastructure-map.json) — the 24 infrastructure types → 5 categories; **category drives evidence**.
- [`v0.1/evidence/slots.json`](v0.1/evidence/slots.json) — the evidence slot catalogue + the A55a `job_type × category × point_type` requirement matrix. See [`../docs/evidence-taxonomy.md`](../docs/evidence-taxonomy.md).
- [`v0.1/validation/rules.json`](v0.1/validation/rules.json) — declarative validation rules. See [`../docs/validation-rules.md`](../docs/validation-rules.md).

**Structure vs conformance:** the `*.schema.json` files validate the *shape* of a record. Which slots are required (the matrix) and which rules must pass (validation rules) are **conformance logic** expressed in `slots.json` and `rules.json` — deliberately separate from JSON Schema, and free of any engine/scoring/ML.

**Evidence is slotted and content-addressed:** every evidence item requires a `slot_code` and a `file_hash` (the file's identity); `file_url` may be a package-relative path (local) or a URL (remote). See [`../docs/packaging.md`](../docs/packaging.md).

**Every field carries a type, a description and a constraint.** The rule is in [`../docs/field-completeness.md`](../docs/field-completeness.md) and enforced in CI by `tools/check_field_completeness.py`. Two consequences worth knowing before you build against these schemas:

- **Objects set `additionalProperties: false`** — unknown keys are rejected, not ignored. If you need to carry extra data, propose a field rather than adding one.
- **The `slotCode` enum mirrors the registry** in [`v0.1/evidence/slots.json`](v0.1/evidence/slots.json); `tools/sync_slot_codes.py --check` verifies the two are in step. The registry is the source of truth — the enum is regenerated with the schema, not hand-edited.

Validate the examples with `uv run tools/validate_examples.py` (or `python3` with `jsonschema>=4.18`). The schemas' absolute `$id`s mean a validator will otherwise try to resolve them over the network; that script resolves the references from disk.

## Scope order

**A55a (point-based) first**, then A55b (stage-based). UK Openreach A55 only. v0.1 — expect breaking changes until v1.0.
