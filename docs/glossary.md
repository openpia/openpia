# Glossary

- **PIA** — Physical Infrastructure Access. Openreach's framework letting other operators use its ducts and poles.
- **A55a** — **PIA A55a — Reactive Works**. **Point-based**: one or more points with evidence. Carries a `job_type` (blockage, desilt, new_track, ...).
- **A55b** — **PIA A55b — Civil Evidence Report**. **Stage/workflow-based**; covers one stage (preliminary_checks, repair_installation, reinstatement, close_off). Linked to its parent A55a by `parent_submission_uid`.

> *These two are the labels OpenPIA uses throughout. Field vernacular sometimes calls them "survey" and "build" instead; whether the spec should acknowledge that vocabulary is being confirmed with practitioners. The notices themselves are not in doubt — only which words lead.*
- **`submission_uid`** — the UUID that identifies a submission; the value A55b stages reference via `parent_submission_uid`.
- **`parent_submission_uid`** — on an A55b, the parent A55a's `submission_uid`. Every stage of an A55b carries the same value; this is the A55a↔A55b link.
- **`pia_noi_reference`** — the PIA Notice of Intent reference; a grouping/context attribute shared across submissions under one Notice of Intent. **Not** the A55a↔A55b link (that is `parent_submission_uid`).
- **Job type** — the specific kind of A55a reactive works.
- **Stage** — an A55b workflow step.
- **Slot / evidence slot** — a named evidence requirement, i.e. a capture prompt telling the engineer what to photograph. OpenPIA **requires** a slot code on every evidence item.
- **Inferred / unslotted evidence** — the legacy pattern where photos carry no slot code and a model guesses the slot. OpenPIA replaces this with explicit slots.
- **Evidence taxonomy** — the catalogue of slots across A55a and A55b.
- **Point** — a discrete location/asset in an A55a with its own evidence.
- **No-build** — a determination that a planned route can't be built as designed (e.g. a blocked duct), often disputed.
- **Altnet** — an alternative network operator building fibre outside the incumbent.
- **Submission package** — the interchange unit: the record JSON plus an `evidence/` folder of files, referenced from the record by a relative `file_url` and a `file_hash`.
- **Content address (`file_hash`)** — the hash that serves as an evidence file's identity; proves the referenced file is the genuine, unaltered source.
