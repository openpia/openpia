# Security Policy

OpenPIA is a specification, JSON schema, and evidence taxonomy — not runtime
software — so "security" here means primarily **data-handling and privacy**
concerns in the specification, and defects in the **reference tooling**
(`tools/`).

## Supported versions

OpenPIA is pre-1.0 and under active development; expect breaking change until
`1.0.0`. Only the most recent release, and the `main` branch, are supported.

| Version        | Supported          |
| -------------- | ------------------ |
| latest release | :white_check_mark: |
| `main`         | :white_check_mark: |
| older releases | :x:                |

## What to report here

Please use the security channel below — rather than a public report — for:

- **Privacy / personal-data concerns** — anything in the schema, evidence
  taxonomy, or packaging model that could encourage or require retaining
  personal data unnecessarily (for example, exposure of location, imagery of
  premises, or signatures), or that weakens the deliberate privacy choices
  such as hash-only signatures.
- **Defects in the reference tooling** (`tools/`) that could be exploited when
  run against untrusted input.
- **Integrity concerns** in the evidence model (for example, weaknesses in the
  `file_hash` content-addressing approach).

General spec questions, field-definition debates, and ratification feedback are
**not** security issues and will be handled through the normal contribution
process once it opens.

## Reporting a vulnerability

Report privately via GitHub's **"Report a vulnerability"** button on this
repository's **Security** tab (Private Vulnerability Reporting is enabled).

You can expect an acknowledgement within about **5 working days**. If the report
is accepted, we'll agree a disclosure timeline with you and credit you in the
fix unless you'd prefer otherwise; if it's declined, we'll explain why. Please
give us reasonable time to address a valid report before disclosing it publicly.
