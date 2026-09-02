# OpenPIA Specification — v0.1 (draft)

> Early draft. Expect breaking changes until v1.0. UK Openreach PIA A55 only; **A55a first, then A55b**. Aligned to real submission shapes, with one deliberate raise-the-bar difference: **evidence must carry explicit slot codes** (see below).

OpenPIA defines two separate but linked Openreach PIA notices. Each submission carries its own `submission_uid` (a UUID). An A55b is linked to its A55a by **`parent_submission_uid`** — the value of the parent A55a's `submission_uid`; every stage of an A55b carries the same `parent_submission_uid`. The `submission_uid` is minted by the system producing the submission, so the link travels with the data rather than depending on any one consumer's internal identifiers. (`pia_noi_reference` is a shared Notice-of-Intent grouping attribute, **not** the link.)

## Conventions

These hold across both notices. Every field in the schemas carries a type, a description and a constraint — the rule is in [field completeness](../../docs/field-completeness.md).

**Absent and `null` mean the same thing.** Many fields are typed as a union with `null` (`["string", "null"]`) because real submissions carry explicit nulls. A producer may omit the key or send `null`; both say "no value recorded", and a consumer must treat them identically. Neither is a way to say "not applicable" — that is what the field's stated `job_type` or `stage` applicability is for.

**Objects are closed.** Every object sets `additionalProperties: false`, so an unknown key is a validation **error**, not something a consumer ignores. This is deliberate: it is what stops two implementations quietly disagreeing about a field neither of them agreed to. If you need to carry something the schema does not define, propose a field — a new field is a version change, not a private extension.

**Arrays are non-empty.** Where an array is present it must hold at least one item. Omit the key, or send `null` where the type allows it, rather than `[]`.

## A55a — reactive works (point-based)

| Field | Purpose |
|---|---|
| `submission_type` | `a55a` (required). |
| `submission_uid` | The UUID identifying this submission (required). A55b stages reference it via `parent_submission_uid`. |
| `schema_code` | Schema identifier + version, e.g. `openpia_a55a_v0.1`. |
| `pia_noi_reference` | PIA Notice of Intent reference — a grouping/context attribute, **not** the A55a↔A55b link. |
| `job_type` | The A55a job type (required): `blockage`, `desilt`, `pole_bend`, `new_track`, `new_box`, `tree_cutting`, `chamber_capacity`, `pole_top_capacity`, `d_pole`, `frame_cover_replacement`, `gully_suck`, `traffic_management`, `new_pole`. |
| `location` | WGS84 and/or OSGB, postcode, what3words, USRN. |
| `notice` | Contractor/engineer, works date, traffic management, site details, supplementary items. |
| `works_details` | Works-specific fields (vary by job type). |
| `points[]` | Points, with `point_type`, `infrastructure_category`/`type`, and per-point `point_data`. |
| `routes[]` | Route polylines (optional); each has a `route_index` and ordered `route_points`. |
| `surfaces[]` | Surface spans along the routes (optional); each references a route by `route_index` and carries its `surface_type`(s) and length. |
| `evidence_items[]` | Evidence items — each **requires** a `slot_code`, a `file_hash` and an `evidence_type`. `file_url` locates the file and is omitted for hash-only slots. |

> Generated reference tables for this section live in [`tables/`](tables/): [`works-details-applicability.md`](tables/works-details-applicability.md), [`point-presence.md`](tables/point-presence.md), and [`evidence-taxonomy.md`](tables/evidence-taxonomy.md) — derived from the schema and kept in step with it.

### Which `works_details` fields apply to which job type

The schema permits every field on every job type; this table says which are *meaningful*. A field outside its job types should be omitted rather than sent null.

| Field | Job types |
|---|---|
| `route_length_m` | blockage, desilt, pole_bend, new_box, new_track, tree_cutting |
| `blockage_span_m` | blockage, pole_bend |
| `existing_cable_count` | blockage, desilt, pole_bend, new_box |
| `capacity_utilization_percent` | blockage, desilt, pole_bend, new_box |
| `duct_reference` | blockage, desilt, pole_bend, new_box, new_track |
| `new_cable_specification` | desilt, new_box, new_track |
| `rods_25mm_used` | blockage, desilt, pole_bend, new_track, new_box |
| `dropwire_count` | d_pole, pole_top_capacity |

### Which points a job type carries

`start_point` and `end_point` are the required point types generally; the rest depend on `job_type`. ✔ = present.

| Job type | start | end | blockage | item | location |
|---|---|---|---|---|---|
| blockage | ✔ | ✔ | ✔ | | |
| pole_bend | ✔ | ✔ | ✔ | | |
| desilt | ✔ | ✔ | | | |
| new_track | ✔ | ✔ | | | |
| new_box *(path)* | ✔ | ✔ | | ✔ | |
| new_box *(point)* | | | | ✔ | |
| tree_cutting *(path)* | ✔ | ✔ | | | |
| tree_cutting *(point)* | | | | ✔ | |
| chamber_capacity | | | | ✔ | |
| pole_top_capacity | | | | ✔ | |
| d_pole | | | | ✔ | |
| frame_cover_replacement | | | | ✔ | |
| gully_suck | | | | ✔ | |
| new_pole | | | | ✔ | |
| traffic_management | | | | | ✔ |

So a **blockage** is: `start_point` and `end_point` bounding the path, a `blockage_point` marking the blockage, and `works_details` carrying `route_length_m`, `blockage_span_m`, `existing_cable_count`, `capacity_utilization_percent`, `duct_reference` and `rods_25mm_used`.

Per-point fields are also scoped: `ducts`, `length_to_item_m` and `blockage_discovery_method` are carried on start and end points; `distribution_point_number` on pole-category points; infrastructure is borne by start, end and item points.

> **Not yet enforced.** These are stated, not validated — a `gully_suck` carrying `blockage_span_m` currently passes. Encoding them (as conditional subschemas, or as rules in [`validation/rules.json`](../../schema/v0.1/validation/rules.json)) is open work. One known gap: the **path vs point variants** of `new_box` and `tree_cutting` are not expressible in v0.1. (`traffic_management` sits on a `location_point`, matching [`slots.json`](../../schema/v0.1/evidence/slots.json).)

## A55b — civil evidence report (stage-based)

| Field | Purpose |
|---|---|
| `submission_type` | `a55b` (required). |
| `submission_uid` | The UUID identifying this submission (required). |
| `parent_submission_uid` | The A55a's `submission_uid`; every stage of an A55b carries the same value — the A55a↔A55b link (required). |
| `schema_code` | e.g. `openpia_a55b_v0.1`. |
| `pia_noi_reference` | PIA Notice of Intent reference — a grouping/context attribute, **not** the link. |
| `stage` | Required: `preliminary_checks`, `repair_installation`, `reinstatement`, `close_off`. |
| `notice` | Contractor/engineer, works date, whereabouts. |
| `stage_details` | Stage-specific fields (which apply depends on `stage`). |
| `evidence_items[]` | Stage evidence — each **requires** a `slot_code`, a `file_hash` and an `evidence_type`. |

## Evidence is slotted — by design

OpenPIA **requires an explicit `slot_code` on every evidence item.** This is the core improvement over inferred/unslotted submissions (where a model guesses which slot a photo belongs to): the engineer is prompted per slot, so the right evidence is captured against a known requirement. Valid slots are the [evidence taxonomy](../../docs/evidence-taxonomy.md) / [`slots.json`](../../schema/v0.1/evidence/slots.json).

The normative definitions are in [`../../schema/v0.1/`](../../schema/v0.1/).

## Evidence carriage

Every evidence item carries a **`file_hash`** (the file's content-address **identity**, required) and a **`file_url`** locating the file — a **package-relative path** (`evidence/…`) when the file travels in the submission package, or an absolute URL when it's remote. Privacy-sensitive slots (signatures) are **hash-only** — `file_hash`, no `file_url`. No inline bytes. See [packaging](../../docs/packaging.md).

## Evidence linkage

Evidence is a flat array; each item says *where it belongs* by reference — the same idea across every job type.

**A55a — by `point_index` (or `item_index`).** Each entry in `points[]` has a `point_index` (0, 1, 2, …). Each evidence item carries a `point_index` that **matches** the point it documents; its `slot_code` says which required shot it is for that point. Three cases:

- `point_index` set → the evidence belongs to that point.
- `item_index` set → it belongs to that entry in `notice.supplementary_items`.
- neither set → it is submission-level (e.g. `SITE_OVERVIEW`, `TM_BOARD`).

`point_index` and `item_index` are mutually exclusive.

**A55b — by stage and `slot_code`.** An A55b record is a single `stage`, and evidence attaches to that stage; there is **no index**, because A55b has no points of its own. Where a location must be distinguished, it is encoded in the **slot code** — e.g. `COMPLETED_START` vs `COMPLETED_END`, `CLOSEOFF_START` vs `CLOSEOFF_END` — rather than by a point reference.
