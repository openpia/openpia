# Submission packaging (interchange)

OpenPIA is an *interchange* format, so a submission has to carry its evidence — not just point at it. The unit of interchange is a **submission package**.

## The package

A package is a container (a folder or a zip) holding:

- the **record** — the A55a or A55b JSON;
- an **`evidence/` folder** — the image and document files.

Each evidence item references its file with two fields — where it is, and what it is:

```
"file_url":  "evidence/media-1.jpg",   // a path relative to the package (local), OR an absolute URL (remote)
"file_hash": "sha256:…"                // the file's content-address identity
```

The record *is* the manifest — it lists every evidence file with its location and hash. A recipient verifies each file by hashing the bytes and matching `file_hash`.

## `file_url`: local or remote

- **Local (primary).** A path relative to the package root, e.g. `evidence/media-1.jpg`. The file travels inside the package. (A relative path is preferred over a `file:` URI, which formally denotes an absolute local path and isn't portable.)
- **Remote (optional).** An absolute URL, e.g. `https://…`, for when the file is hosted elsewhere. Still hash-verified.

## `file_hash`: the identity, not just a check

The hash is the file's **identity**. Whatever `file_url` resolves to must hash to that value, so substitution or tampering is always detectable — permanently, by anyone who holds the package. (This is why the hash is required: unlike a validation *service* that fetches-and-discards, a *standard* has to make each file verifiably the genuine one.)

## Hash-only (signatures)

Signatures are personal data. Their slots are **hash-only**: the record carries `file_hash` but **no `file_url`** and no bytes — proof-of-capture without retaining the image.

## No inline

There is **no base64 / inline mode** — evidence bytes belong in files, referenced by `file_url` + `file_hash`, not embedded in the JSON.
