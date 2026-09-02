# Validation rules

Declarative definitions of what makes an A55 submission complete and compliant. These describe the rules; they do not prescribe an engine, a score, or any machine learning. Whether a photo shows the right thing — content assessment — is out of scope. Derived from a canonical A55 rule set; to be ratified with practitioners.

A rule is anything conditional or contestable; an unconditional limit on a single value is a schema constraint, and lives in the notice schema (see field-completeness.md).

## Families

- **structural** — Submission and point shape — required structure and recognised values.
- **evidence** — Evidence slot presence and file integrity.
- **cross_field** — Consistency between declared values and physical logic.
- **image_quality** — Deterministic image gates — blur, exposure, and resolution.

## Severities

- **error** — Blocks a compliant outcome.
- **warning** — Advisory.
- **info** — Audit note only.

## Mandatory vs controllable

A mandatory rule is always applied. A non-mandatory rule may be switched off per adopter; a disabled rule produces no defect and drops out of any completeness measure, so results stay comparable.

## Rules

### structural

| Code | Severity | Applies | Mandatory | Description |
| --- | --- | --- | --- | --- |
| SUBMISSION_TYPE_VALID | error | both | yes | submission_type is a recognised notice type (a55a or a55b). |
| SUBMISSION_UID_PRESENT | error | both | yes | submission_uid is present and a valid UUID — the record's own identity, referenced by A55b stages through parent_submission_uid. |
| HAS_START_AND_END_POINT | error | a55a | yes | Path works carry both a start point and an end point; point-type works are exempt. |
| BLOCKAGE_POINTS_PRESENT | error | a55a | yes | Blockage and pole-bend works carry one or two blockage points. |
| POINTS_NON_EMPTY | error | a55a | yes | At least one work point is present. |
| GPS_WITHIN_UK | error | a55a | yes | Each point's latitude and longitude fall within United Kingdom bounds. |
| GPS_GRID_CONSISTENT | warning | a55a | no | A point's latitude/longitude agrees with its easting/northing to within roughly fifty metres. |
| TM_TYPE_VALID | error | both | yes | traffic_management is a recognised value. |
| INFRA_TYPE_VALID | warning | a55a | no | infrastructure_type is recognised and maps to a category. |
| POINTS_SEQUENTIAL | warning | a55a | no | point_index values run sequentially from zero. |
| ROUTE_HAS_SURFACE | warning | a55a | no | A route-bearing submission declares a surface type. |
| CHAMBER_HAS_DUCT_DATA | warning | a55a | no | A chamber-category point without duct data is flagged. |
| POLE_HAS_REFERENCE | warning | a55a | no | A pole point without a distribution-point number is flagged. |
| POINT_HAS_GRID_REF | warning | a55a | no | A point carrying latitude/longitude but no British National Grid easting/northing is noted. |
| NOI_REFERENCE_PRESENT | warning | both | no | pia_noi_reference is present. |
| PARENT_SUBMISSION_UID_PRESENT | error | a55b | yes | parent_submission_uid is present — every A55b civil-evidence report belongs to a parent A55a, and this is the link between them. |
| PARENT_A55A_EXISTS | error | a55b | no | parent_submission_uid resolves to a known A55a submission_uid; applied when the parent A55a set is available to the validator. |
| CIVIL_EVIDENCE_STAGE_INCOMPLETE | error | a55b | yes | The close-off stage is present across the A55b reports sharing a parent_submission_uid; only close-off is required. |
| EXCAVATION_DIMENSIONS_MISSING | warning | a55b | yes | A repair-and-installation stage carries excavation dimensions. |
| REINSTATEMENT_DIMENSIONS_MISSING | warning | a55b | yes | A reinstatement stage carries reinstatement dimensions. |

### evidence

| Code | Severity | Applies | Mandatory | Description |
| --- | --- | --- | --- | --- |
| REQUIRED_SLOTS_POPULATED | error | both | yes | Every required evidence slot, and every conditional slot whose condition holds, has at least one file. The slot catalogue in evidence/slots.json is the source of which slots apply. |
| EVIDENCE_GPS_PROXIMITY | warning | both | no | An evidence item is captured within roughly two hundred metres of the point it belongs to. |
| EVIDENCE_TIMESTAMP_PRESENT | warning | both | no | Each evidence item carries a capture timestamp. |
| EVIDENCE_TIMESTAMP_RECENT | warning | both | no | An evidence item's capture timestamp is within thirty days of submission. |
| NO_DUPLICATE_HASHES | warning | both | yes | No two evidence files in a submission share the same file_hash, which would mean one image reused across slots. |
| HASH_VERIFIED | error | both | yes | Each evidence item's recorded hash-verification outcome is consistent: where the declared file_hash was checked against the fetched file, the two matched. An item with no file_hash, or one whose file was never fetched, is not verified rather than failed — the byte comparison runs in the fetch pipeline, and this rule reads its recorded result. |
| IMAGE_FETCH_OK | error | both | yes | Each evidence file is retrievable from its file_url. |
| TM_BOARD_WHEN_TM_ACTIVE | error | both | yes | A traffic-management board photograph is present whenever traffic management is active. |
| FILE_TYPE_VALID | warning | both | no | An evidence file matches its declared evidence_type. |
| SLOT_CODES_MATCH_TAXONOMY | warning | a55a | no | Evidence slot codes belong to the A55a taxonomy for the works type. |

### cross_field

| Code | Severity | Applies | Mandatory | Description |
| --- | --- | --- | --- | --- |
| ROUTE_LENGTH_CONSISTENT | warning | a55a | no | A declared route length agrees with the summed point-to-point GPS distance to within roughly twenty per cent. |
| BLOCKAGE_SPAN_CONSISTENT | warning | a55a | no | A declared blockage span agrees with the distance between the blockage points. |
| POLE_BEND_ENDPOINTS | warning | a55a | no | A pole-bend job starts at a chamber-category point and ends at a pole. |
| CAPACITY_TRIGGERS_EVIDENCE | warning | a55a | no | High capacity utilisation calls for additional evidence. |
| ROAD_CLOSURE_SITE_DETAILS | warning | a55a | no | A road or lane closure carries the relevant site-detail fields. |
| WORK_PLAN_MISMATCH | warning | a55b | yes | Completed works declared not to match the original plan are flagged. |
| JOB_NOT_COMPLETED | warning | a55b | yes | A close-off stage declaring the job not complete is flagged. |

### image_quality

| Code | Severity | Applies | Mandatory | Description |
| --- | --- | --- | --- | --- |
| IMAGE_NOT_BLURRED | warning | both | no | An image is not blurred beyond a deterministic sharpness threshold. |
| IMAGE_EXPOSURE_OK | warning | both | no | An image is neither significantly under- nor over-exposed, by deterministic thresholds. |
| IMAGE_MIN_RESOLUTION | warning | both | no | An image meets a minimum resolution. |

## Evidence slot conditions

The evidence slot catalogue (`evidence/slots.json`) marks some slots `conditional`. Each such slot carries a machine-readable `when` object, which REQUIRED_SLOTS_POPULATED reads to decide whether the slot applies:

```json
{ "field": <schema field>, "op": "equals" | "not_equals", "value": <enum member> }
```

The grammar is closed: `op` is one of `equals` / `not_equals`; `field` is a root-relative dot-path resolving to a declared property in the notice's own schema; `value` is a member of that field's enum. Generation fails on any violation. The current conditions are:

- `job_type` `equals` `new_track`
- `notice.traffic_management` `not_equals` `none`
- `stage_details.traffic_management` `not_equals` `none`
