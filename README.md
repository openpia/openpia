# OpenPIA

**An open standard for the Openreach Physical Infrastructure Access (PIA) A55 workflow.**

OpenPIA is an agreed, vendor-neutral schema for the Openreach PIA **A55a** and **A55b** notices — capturing the operational reality that proprietary tools leave out, and the **evidence** field engineers must capture. As an added benefit, a shared schema lets systems interchange PIA data directly.

- **A55a** — *reactive works*, **point-based**, with a `job_type` (blockage, desilt, new_track, ...).
- **A55b** — *civil evidence report*, **stage/workflow-based**, linked to its parent A55a by `parent_submission_uid`.

> **Scope:** UK Openreach A55 only, **A55a first, then A55b**. Pre-1.0 and actively designed — expect breaking changes until v1.0.

## Repository layout

| Path | What's in it |
|---|---|
| [`CHARTER.md`](CHARTER.md) | Mission and the six principles |
| [`GOVERNANCE.md`](GOVERNANCE.md) | How decisions get made, versioned, and challenged |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to get involved |
| [`CHANGELOG.md`](CHANGELOG.md) | Running log of changes |
| [`spec/`](spec/) | The human-readable specification, by version |
| [`schema/`](schema/) | The normative JSON Schema (`a55a`, `a55b`, `common/`), the `evidence/` slot catalogue + A55a matrix, the infrastructure map, and `validation/` rules |
| [`examples/`](examples/) | Sample valid A55a and A55b records |
| [`docs/`](docs/) | Lifecycle, glossary, the **evidence taxonomy** (capture prompts), the **validation rules**, the **design rationale** (the *why*), **packaging**, and the **field-completeness** rule |
| [`tools/`](tools/) | Checks anyone can run: field completeness, slot-code check, example validation |
| [`.github/`](.github/) | CI that runs those checks on every push and pull request |

## Licensing

- Schema & reference code — **Apache License 2.0** (permissive, with an explicit patent grant). See [`LICENSE`](LICENSE).
- Specification & documentation — **CC BY 4.0**. See [`LICENSE`](LICENSE).
- The name **OpenPIA** and the **"OpenPIA-conformant"** claim are handled by trademark + a usage/conformance policy — use the schema and docs freely; use the *name* only for conformant implementations.

_Licence choice is settled; the verbatim licence-text files and trademark registration are the remaining steps before v1.0._

## Status

Early and pre-1.0. Development prioritises **A55a** first, then **A55b**. Wider co-design — through GitHub issues and pull requests — opens as the project goes public.

---

*OpenPIA is community-run and vendor-neutral. It defines the interchange, not a product.*
