# The A55 notices

OpenPIA covers two linked Openreach PIA notices:

1. **A55a — reactive works (point-based).** The notice carries a `job_type`, its `points[]` (including any blockage points), and **slotted evidence per point**.
2. **A55b — civil evidence report (stage-based).** One record per workflow `stage` (`preliminary_checks` → `repair_installation` → `reinstatement` → `close_off`), with **slotted evidence per stage**.

An A55b is linked to its parent A55a by `parent_submission_uid` (the A55a's `submission_uid`); `pia_noi_reference` is a shared grouping attribute, not the link. Getting the right evidence at each point and stage is what the [evidence taxonomy](evidence-taxonomy.md) exists for.
