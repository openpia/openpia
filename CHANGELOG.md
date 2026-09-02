# Changelog

All notable changes to OpenPIA are recorded here.

- Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
- Versioning: [Semantic Versioning](https://semver.org/). **Pre-1.0, minor bumps may break** — expect change until `1.0.0`.
- `main` is the rolling working draft; entries under **Unreleased** roll up under a version heading when that version is cut.

## [Unreleased]

## [0.1.0] - 2026-09-02

First public release. OpenPIA is a vendor-neutral schema, specification and evidence taxonomy for UK Openreach A55 physical-infrastructure-access submissions. Scope for v0.1: UK Openreach A55 only, with **A55a (point-based)** prioritised ahead of **A55b (stage-based)**. Everything below is pre-1.0 and subject to change; several field meanings are flagged for practitioner ratification.

### Schema

- **A55a schema** (`schema/v0.1/a55a.schema.json`) — point-based reactive works: `submission_type: a55a`, a required `job_type` (blockage, desilt, new_track, ...), points, and slotted evidence. Path jobs carry `start_point` / `end_point`, blockage jobs a `blockage_point`, point jobs an `item_point`. Evidence is a single flat `evidence_items[]` array whose items reference where they belong.
- **A55b schema** (`schema/v0.1/a55b.schema.json`) — stage-based civil evidence: a required `stage`, a `submission_uid`, and a `parent_submission_uid` linking the report to its parent A55a. The A55a↔A55b link is `parent_submission_uid` (`pia_noi_reference` is a Notice-of-Intent grouping attribute, not the link).
- **Shared definitions inline** — enums (point types, infrastructure category/type, traffic management, job types, stages, surface types) and objects (location, notice, evidence items) live as `$defs` inside each schema, so `$ref`'d fields inherit a single shared description. Both schemas are valid JSON Schema 2020-12.
- **Closed objects and bounded arrays** — `additionalProperties: false` on every object, so an unknown key is rejected rather than validating silently; a new field is therefore a schema change. `points`, `evidence_items` and the nullable arrays require at least one item — omit or null an array rather than sending `[]`. Convention: **absent and `null` mean the same thing**.
- **Every field is typed, described and constrained** — each field carries a type, a description and a constraint, checked in CI. Text lengths are consistent (255 for references and identifiers, 5000 for free text); numeric ranges are bounded (coordinates to WGS84 and OSGB36 National Grid limits; lengths, depths, dimensions and counts non-negative).
- **`supplementaryItem.value`** states its value space as typed `anyOf` branches while staying deliberately open — it is the generic answer-carrier, so a new supplementary question needs no schema change.

### Evidence taxonomy

- **Slot catalogue** (`schema/v0.1/evidence/slots.json`) and **capture guide** (`docs/evidence-taxonomy.md`) — 45 evidence slot codes. **Every evidence item requires a `slot_code`** — OpenPIA's deliberate improvement over inferred/unslotted submissions, where a model guesses which requirement a photo meets. An unknown `slot_code` fails schema validation, not only the rules.
- **Full A55a slot matrix** — required slots resolve on `job_type × infrastructure_category × point_type`, with each path endpoint evaluated independently so the two ends can require different slots.
- **Infrastructure map** (`schema/v0.1/common/infrastructure-map.json`) — 24 infrastructure types → 5 categories; category drives the endpoint/item evidence set (`jointing_chamber` and `chamber_non_standard` reuse the `junction_box` set).
- **Content-addressed, packaged evidence** — `file_hash` (bare 64-hex, sha256 recommended) is the evidence file's identity and is required; `file_url` may be a package-relative path (local) or a URL (remote); no inline bytes. `evidenceType` is `photo` or `video`. Signatures are hash-only (`file_hash`, no `file_url`), keeping proof-of-capture without retaining personal data. `docs/packaging.md` describes the submission-package interchange model.

### Validation

- **Declarative rule set** (`schema/v0.1/validation/rules.json` + `docs/validation-rules.md`) — structural, evidence, cross-field and image-quality rules, with severity and a mandatory-vs-controllable distinction. No engine, scoring or ML; content assessment is out of scope. `docs/validation-rules.md` states the boundary: a constraint holds unconditionally and lives in the schema; a rule is conditional, contestable, or switchable by an adopter, and lives here.

### Specification & docs

- **Spec** (`spec/v0.1/`) — normative conventions (closed objects, non-empty arrays, absent≡`null`) and a job-type shape reference: a `works_details` field inventory by job type and a point-type presence table, so "what is a valid blockage" is answerable from the spec. The shape reference is documentation, not yet enforced.
- **Design rationale** (`docs/rationale.md`), **lifecycle** and **glossary** docs. Canonical notice labels are **PIA A55a — Reactive Works** and **PIA A55b — Civil Evidence Report**.
- **Governance & licensing** — `CHARTER.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`; dual-licensed (Apache-2.0 for code/schema, CC-BY-4.0 for the specification text).

### Tooling & CI

- **`tools/`** — `check_field_completeness.py` (audits the type/description/constraint rule; standard library only; `--report`, `--json`, `--baseline` ratchet), `sync_slot_codes.py` (verifies the inline `slotCode` enum against the slot registry), `validate_examples.py` (checks each schema against the 2020-12 meta-schema, then validates the examples, resolving `$ref`s from disk).
- **CI** (`.github/workflows/validate.yml`) — runs schema and example validation, the slot-code check and the completeness check via `astral-sh/setup-uv` and `uv run`, so CI provisions its one dependency exactly as a local run does and does not depend on the website serving the schema files.
- **Sample records** — slotted A55a and A55b examples that validate against the schemas.

### For practitioner ratification

- Two field descriptions are inferred rather than taken from a canonical PIA source: `h_g47_notes` (read as the HSG47 underground-services check, supported by the `HG47_MARKUP` slot) and `whereabouts_id`.
- Known gaps recorded for v0.1: the path-vs-point variants of `new_box` and `tree_cutting` are not yet distinctly expressible, and `traffic_management`'s point type disagrees between the spec table (`location_point`) and `slots.json` (item points). The evidence taxonomy is derived from a real canonical slot registry and is **to be ratified with practitioners**, not final.
