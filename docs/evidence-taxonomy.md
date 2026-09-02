# Evidence taxonomy — capture guide

Getting the **right photos, first time** is the core of what OpenPIA is for. This taxonomy is the shared list of **evidence slots** — each a prompt telling the field engineer exactly what to photograph, and how many images.

**OpenPIA requires an explicit `slot_code` on every evidence item** — the deliberate improvement over inferred/unslotted submissions (where a model guesses which requirement a photo meets).

Machine-readable catalogue: [`../schema/v0.1/evidence/slots.json`](../schema/v0.1/evidence/slots.json). Infrastructure map: [`../schema/v0.1/common/infrastructure-map.json`](../schema/v0.1/common/infrastructure-map.json).

> Derived from a real canonical slot registry — **to be ratified with practitioners**, not final. A55b is complete; A55a is now the full matrix below.

## Slot attributes

- **requirement** — `required` (absence is an error), `optional` (absence is silent), or `conditional` (required only `when` a condition holds; otherwise a warning).
- **max_images** — cap per slot (1 unless noted).
- **hash_only** — for signatures: the record carries only `file_hash`, with **no `file_url`** and no image in the package — proof-of-capture without retaining personal data. Every other evidence item carries its file (see [packaging](packaging.md)).

## A55a — required slots resolve on `job_type × infrastructure_category × point_type`

Each **path endpoint (start/end) is evaluated independently**, so the two ends can require different slots depending on the asset at each. **Infrastructure category drives the endpoint/item slots** — `jointing_chamber` and `chamber_non_standard` reuse the `junction_box` set (see [infrastructure map](../schema/v0.1/common/infrastructure-map.json): 24 types → 5 categories).

### Submission level (all A55a)

| Slot | Requirement | Max |
|---|---|---|
| `SITE_OVERVIEW` | optional | 3 |
| `TM_BOARD` | conditional — when `traffic_management ≠ none` | 3 |

### New-track route level (`new_track` only)

`TRACK_SURFACE_CLOSEUP` (required), `TRACK_SURFACE_CONTEXT` (required).

### Path endpoints — `start_point` / `end_point`, by infrastructure category

**Junction box** (and jointing_chamber, chamber_non_standard):

| Job | Required endpoint slots |
|---|---|
| blockage / desilt / pole_bend / new_track | `CHAMBER_INTERNAL`, `CHAMBER_CONTEXT` |
| new_box (on a path) | `CHAMBER_ROD_BORE`, `CHAMBER_CONTEXT` |
| tree_cutting (on a path) | `CHAMBER_INTERNAL`, `CHAMBER_CONTEXT`, `TREE_CUTTING` |

**Pole:** `POLE_DP_TAG`, `POLE_CONTEXT` (all path jobs) — tree_cutting adds `TREE_CUTTING`.
**Structure:** `STRUCTURE_ENTRY`, `STRUCTURE_CONTEXT` (all path jobs) — tree_cutting adds `TREE_CUTTING`.

### Blockage points — `blockage_point` (`blockage`, `pole_bend`)

`BLOCKAGE_MARKED` (required), `BLOCKAGE_CONTEXT` (required). *(desilt has no blockage points.)*

### Item points — `item_point` (point-type jobs)

| Job | Required | Optional |
|---|---|---|
| `d_pole` | `POLE_DP_TAG_D_LABEL`, `POLE_TOP_ANGLE_1..4`, `POLE_BASE`, `POLE_CONTEXT` | — |
| `pole_top_capacity` | `POLE_DP_TAG`, `POLE_TOP_ANGLE_1..4`, `POLE_BASE`, `POLE_CONTEXT` | — |
| `chamber_capacity` | `CHAMBER_INTERNAL`, `CHAMBER_CONTEXT`, `CHAMBER_EQUIPMENT` | — |
| `gully_suck` | `CHAMBER_INTERNAL`, `CHAMBER_CONTEXT` | — |
| `frame_cover_replacement` | `CHAMBER_LID`, `CHAMBER_CONTEXT`, `CHAMBER_DAMAGE` | — |
| `new_box` | `ITEM_PROPOSED_LOCATION`, `ITEM_CONTEXT` | `ITEM_EXISTING_CHAMBER` |
| `new_pole` | `ITEM_PROPOSED_LOCATION`, `ITEM_CONTEXT` | `ITEM_EXISTING_POLE` |
| `tree_cutting` | branches by category — jb: `CHAMBER_INTERNAL`+`CHAMBER_CONTEXT`+`TREE_CUTTING`; pole: `POLE_DP_TAG`+`POLE_CONTEXT`+`TREE_CUTTING`; structure: `STRUCTURE_ENTRY`+`STRUCTURE_CONTEXT`+`TREE_CUTTING` | — |
| `traffic_management` | (no evidence slots) | — |

### Free-form (any A55a)

`ROUTE_MAP` (optional), `ADDITIONAL_EVIDENCE` (optional, up to 8).

## A55b — slots per stage (universal; no job/infra branching)

Only `close_off` is mandatory across a parent's stages; stages 2–3 are optional and may arrive in any order. Stages 3 and 4 deliberately duplicate evidence under distinct codes.

| Stage | Required | Conditional / optional |
|---|---|---|
| `preliminary_checks` | `RISK_ASSESSMENT`(2), `HG47_MARKUP`(4), `SITE_SETUP`(8) | `TM_BOARD`(3, when TM active), `SITE_OVERVIEW`(3), `ADDITIONAL_EVIDENCE`(8) |
| `repair_installation` | `PRE_WORK_DIG`(4), `EXCAVATION`(4), `REPAIR_INSTALLATION`(4), `BACK_FILL`(4) | `ADDITIONAL_EVIDENCE` |
| `reinstatement` | `REINSTATEMENT`(4), `COMPLETED_START`(2), `COMPLETED_END`(2), `SITE_SHUTDOWN`(4), `SIGNATURE`(1, hash-only) | `ADDITIONAL_EVIDENCE` |
| `close_off` | `CLOSEOFF_REINSTATEMENT`(4), `CLOSEOFF_START`(2), `CLOSEOFF_END`(2), `CLOSEOFF_SIGNATURE`(1, hash-only) | `ADDITIONAL_EVIDENCE` |
