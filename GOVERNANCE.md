# Governance

OpenPIA is developed in the open. This document describes how the standard is built, and how decisions are made, recorded, versioned, and revisited.

## How the standard is built

OpenPIA is **practitioner-led**. The schema is shaped by the people who live the work — **build partners, altnets, and the software / GIS vendors who serve them**, together with the field-QA practitioners who know what evidence a submission really needs.

Input comes primarily from **direct engagement** with those practitioners: detailed conversations and review of a draft against real A55a / A55b submissions. Once the project is public, it also comes from **open discussion on GitHub issues and pull requests**. A data model is defined through worked examples and precise discussion, not tick-box surveys — so direct engagement, not forms, is the mechanism.

The rhythm is ordinary open-source development applied to a data standard: **ship a draft, gather input, iterate, and credit the people whose input shaped it.** Each change is grounded in real operational reality, then written down precisely so the whole chain can point at the same definition of "done."

_(We may run occasional structured input drives if and when a broad contributor community forms, but that is an option, not the mechanism — and not a commitment.)_

## How input reaches the standard

Three channels, so contributors always know where to put what — and no decision is ever truly locked:

- **Direct practitioner engagement** — the primary channel. Detailed input from build partners, altnets, vendors, and field-QA leads, reviewed against real submissions.
- **Standing channel — GitHub issues & pull requests** — the permanent, open way to propose a change, raise something out of scope, or challenge a past decision, always against the live schema. Open to anyone, always.
- **Versioned decisions, open to challenge** — a decision lives on in the versioned schema, which is never truly locked. If real-world use shows a decision was wrong, the standing channel is how it gets reopened — with evidence.

## Versioning

The schema uses **semantic versioning** (`MAJOR.MINOR.PATCH`):

- **PATCH** — clarifications and non-breaking fixes, including correcting an older part of the schema while newer work is in progress (e.g. `0.2.1`).
- **MINOR** — new fields or objects. Pre-1.0, minor bumps may break.
- **MAJOR** — breaking changes to structure or meaning; `1.0.0` signals "stable, safe to build on."

`main` is the rolling working draft; meaningful milestones are frozen as in-tree version folders (`schema/v0.1/`, ...) plus a git tag and a GitHub Release. Every published version stays in-tree — nothing is archived elsewhere. Once published, a version's files are never edited; corrections go into the next PATCH. All changes are logged in `CHANGELOG.md`.

## Decision-making

- Proposals and changes are discussed **in the open**, on issues and pull requests.
- A change is accepted when there is rough consensus among active contributors and no unresolved substantive objection.
- Maintainers are responsible for triage, keeping the record honest (what changed and why), and cutting versioned releases. Maintainers steward the process; they do not own the standard.

## Resolving disagreements

Most disagreements resolve in open discussion. The ones that don't need a defined path — and for a *standard* this matters more than for ordinary software, because the losing side can fork or keep its own format, and a standard with a competing dialect is no longer a standard.

**Consensus-seeking, not consensus-requiring.** We aim for agreement, but unanimity is never the bar — no single party holds a veto. A change proceeds when there is no *sustained* substantive objection: everyone with a concern has been heard and addressed, even if not everyone agrees.

**Escalation ladder.** When a decision is stuck: (1) **discuss** in the open; (2) **summarise** — after a reasonable time (guideline ~2 weeks), a maintainer writes a neutral summary of the positions and calls for a decision; (3) **decide** — if still contested, the deciding body makes the call and records it.

**Record the decision, including the rejected side.** Every contested decision is written up as a short decision record: what was proposed, what was chosen, why, and the case *against* stated fairly. This is what makes a losing party stay (their argument is understood, not ignored) and it stops the same debate recurring.

**Disagree and commit — nothing is permanent.** Because the schema is versioned, a decision is "current," not forever. A dissenter is asked to commit to the group's choice now; if real-world use proves them right, the standing channel is how they reopen it *with evidence*.

## Who decides when consensus fails

- *Interim:* while the project is small, the maintainers (currently the founder) act as tie-breaker — normal for an early project, and stated plainly so it's not a surprise.
- *Intended:* a standard can't credibly be adjudicated by its founder, or by any party with a commercial stake, indefinitely. As the contributor base forms, final adjudication is intended to move to a **neutral industry body's PIA / standards working group** (e.g. within INCA). That neutrality is what lets a vendor accept a decision that went against them — and therefore what makes the standard adoptable.

> This process is deliberately lightweight while the project is pre-contributor. It formalises as the group grows — detail gets added when disagreements actually need it, not before.

## Roles

- **Contributors** — anyone who helps shape the standard: taking part in a practitioner review or conversation, opening an issue, or submitting a pull request.
- **Maintainers** — steward triage, versioning, and the record.
- **Working group** — as the project matures, standing review is intended to move into an industry body's PIA / standards working group so the standard is owned collectively rather than by any single party.
