# Design rationale

Why the standard is shaped the way it is — short reasoning behind the main decisions. An open standard has to be *defensible*, not just documented, so the "why" is recorded here alongside the "what".

> These reasons are derived from a real canonical PIA model — a strong starting point **to be ratified with practitioners**, not treated as final.

## Evidence integrity — hashes

- **Why hash evidence at all.** A submission references images by URL; hashing each file (SHA-256) lets a validator confirm the bytes it checks are exactly the bytes the field app captured. That makes evidence **tamper-evident** — a photo swapped or edited between capture and review is detectable.
- **Why no duplicate hashes.** Identical hashes across a submission mean one photo has been reused to fill several required slots — padding a pack with the same image pretending to be different evidence. Flagging duplicates catches it.
- **Why signatures are hash-only.** A signature proves a person was present, but the image is personal data. Fetch it, verify it, keep the hash, discard the bytes — tamper-evident proof-of-capture **without retaining PII**. Privacy-compliant by default.
- **Why the hash is *required*, and is the file's identity.** OpenPIA is an interchange format: evidence travels *with* the submission (in a package), so — unlike a validation service that fetches-and-discards — the hash is the file's permanent **content address**. It's required because it's what proves any carried or linked file is the genuine source; without it, evidence can't be verified. Bytes live in files (referenced by `file_url` + `file_hash`), never inline. See [packaging](packaging.md).

## Location & time — GPS and timestamp

- **Why capture them.** They turn a photo into geolocated, time-anchored proof — evidence that the work was photographed *at the asset* and *around the time of the works*, not sourced from elsewhere or a previous job.
- **Why a proximity threshold (~200 m).** Evidence taken far from its declared point is implausible for a photo of that asset — a signal of wrong-location or recycled imagery — while a generous radius tolerates normal GPS drift near buildings and underground.
- **Why a recency window (~30 days).** A capture date long before submission suggests a stale or reused photo rather than fresh evidence of these works — a common cause of rejection.

## Points vs stages

The plan notice (A55a) and the completion report (A55b) answer different questions — *what and where the physical problem is* versus *proof the works were done correctly across a sequence of site visits*. So one is modelled as geolocated **points** and the other as time-ordered workflow **stages** with no geometry of its own.

## Infrastructure category drives evidence

What makes a photo *meaningful proof* depends on the asset, not the reason for the visit: a chamber needs internal shots, a pole needs its ID tag — regardless of job type. So the asset at a point, not the job type alone, determines the required slots.

## Explicit slots, not inference

Making each expected photo a **declared slot** lets the system do coverage analysis — tell the engineer up front "you're missing the chamber-internal shot," and treat a missing required slot as a defect. That's impossible if you only classify whatever images happen to arrive. Guessing the slot with a model is a fallback for unslotted submissions, not the primary model — OpenPIA requires explicit slots so capture is a **known requirement, not a guess**.

## Cheap checks before expensive ones

Deterministic quality and integrity checks (hash, blur, exposure, GPS, timestamp) are near-instant and free; content assessment is slow and costly. Running the cheap gates first rejects obviously unusable evidence before spending on the expensive stage. Each layer acts as a gate.

## Rules you can turn off — with an honest denominator

Adopters differ in data maturity, so some rules are controllable. When a rule is disabled it produces no defect and drops out of the completeness measure — so a result honestly reflects only what was actually checked, and results stay comparable. (Any implementation that scores should record which rule set was active, so a result can be reproduced.)

## Fewer job types, richer rules

Near-identical works (the same job at a chamber vs a pole; capacity exceeded underground vs overhead) share most requirements. Collapsing them into fewer canonical types with conditional rules avoids duplicated, drift-prone definitions.

## Geometry is a property, not a type

The same physical work shows up "at a single point" and "along a route" (a new box, tree cutting). The work is identical; only the spatial extent differs. So point-vs-path is a **configuration attribute**, not a separate job type.

## Three kinds of point, kept apart

Infrastructure points are validated and carry evidence; route points are map-polyline geometry that must *not* be validated as assets; surface segments are length-annotated labels with no coordinates. Mixing them would force invalid checks on navigation waypoints.

## Open-world enums where the real world is messy

Some vocabularies (e.g. how a blockage was discovered) vary in real submitter data. Leaving them extendable lets new values be added as adopters onboard, without a schema change or blocking ingestion.

## Submitter-neutral canonical vocabulary

The standard defines the vocabulary; submitters map their internal naming onto it — never the reverse. No single vendor's terminology leaks into the model, and many submitters can be onboarded against one schema.

## Works vs non-works

Only jobs involving physical civil work (excavation, installation, reinstatement) produce a completion / civil-evidence report; survey and reporting notices are resolved without one. Evidence expectations follow that split.

## Evidence linkage — a flat array with a reference

- **Why a flat `evidence_items[]` array with a `point_index` reference (A55a).** Evidence is kept in one flat array, and each item references *where it belongs* — a point (`point_index`), a supplementary item (`item_index`), or the submission itself (neither). One uniform shape then covers every job type and geometry. Nesting evidence inside each point would be more rigid — it couldn't express submission-level or supplementary-item evidence without a second mechanism, and would couple evidence to the point tree. `point_index` is a stable key the evidence refers back to (a "foreign key"), not merely an array position.
- **Why A55b links differently.** An A55b record is a single workflow stage with no geometry of its own, so evidence scopes to the stage and there is nothing to index into. Where a location matters it is carried in the slot code (`COMPLETED_START` vs `COMPLETED_END`) rather than a point reference — which keeps A55b's per-stage slot sets universal and geometry-free.
