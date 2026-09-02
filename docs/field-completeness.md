# Field completeness

Every field in an OpenPIA schema carries three things: a **type**, a **description**, and a **constraint**. This document defines what each means precisely enough to be checked mechanically, and [`../tools/check_field_completeness.py`](../tools/check_field_completeness.py) does the checking.

The reason is interoperability. A field with a type but no description is guessed at by each implementer, and they guess differently. A field with a description but no constraint validates values the description rules out. Neither shows up as a validation failure, so neither gets found until two vendors' payloads disagree in production.

This is a rule about the **schema**. It is distinct from [validation rules](validation-rules.md): the schema says what shape and range a value may take on its own; the rules say whether a submission is consistent and complete across fields. `excavation_depth_m` being a non-negative number belongs here; a road-closure requiring site-detail fields belongs there.

## The three dimensions

### 1. Type

A field declares `type` explicitly. `null` may appear in a type union but does not count on its own — `["string", "null"]` satisfies this, `["null"]` does not. `const` and `enum` satisfy it without a `type` keyword, since both fix the type by fixing the value.

A genuinely polymorphic field (one whose type varies by context) satisfies this with `anyOf`/`oneOf` over typed branches. "No `type` keyword at all" is not a way to express polymorphism — it means *any JSON value*, which is almost never what is meant.

### 2. Description

A field has a non-empty `description` stating what the value *is* — the thing in the world it records, and any unit or reference frame a reader could otherwise get wrong.

A nullable field does not need to explain its nullability. Absent and `null` mean the same thing throughout OpenPIA — stated once in the [spec](../spec/v0.1/README.md#conventions) — so "optional" and "if available" are noise in a field blurb.

A field that is only a `$ref` inherits the description from the referenced `$def`, which counts. This is deliberate: shared meaning is written once as a `$def` and referenced, not restated at each use. It follows that **every `$def` also needs a description**, and the checker reports those separately.

Descriptions state meaning, not provenance or reassurance. "The UUID identifying this submission" — not "a stable identifier assigned by the producer". Rationale goes in the [spec narrative](../spec/v0.1/README.md) or [rationale](rationale.md); the field blurb stays tight.

Where a field applies only in some contexts, the description says which: which `job_type` a `works_details` field belongs to, which `stage` a `stage_details` field belongs to. Today those conditions live only in the parent object's description, which is where implementers stop reading.

### 3. Constraint

A field carries at least one keyword narrowing the values its type admits. What qualifies depends on the type:

| Declared type | Satisfied by |
| --- | --- |
| `string` | `enum`, `const`, `pattern`, `format`, `maxLength`, `minLength` |
| `integer`, `number` | `enum`, `const`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf` |
| `boolean` | nothing further — `true`/`false` is already the complete value set |
| `array` | `items` (or `prefixItems`) **and** at least one of `minItems` / `maxItems` |
| `object` | `additionalProperties` (or `unevaluatedProperties`) |
| polymorphic | `anyOf`, `oneOf`, `enum`, `const` |

Two of those rows deserve saying out loud.

**Objects must set `additionalProperties`.** Listing `properties` is documentation, not constraint — a producer may add any key it likes and still validate. For an interchange format that is the difference between "we agree on the fields" and "we agree on the fields we happened to both think of". Set `additionalProperties: false` on every object; where extension is genuinely wanted, add a named extension object rather than leaving the whole record open.

**Arrays need a bound, not just an item schema.** `items` says what a member looks like; it does not stop the array being empty. `"evidence_items": []` validating against a schema whose description says evidence is required is exactly the kind of silent disagreement this rule exists to catch.

An unbounded free-text field is unconstrained. Notes fields take a `maxLength` — pick one value and apply it consistently rather than leaving some at 5000 and others open.

## Where a constraint should not go

Some limits look like field constraints but belong in [`validation/rules.json`](../schema/v0.1/validation/rules.json):

- **Cross-field consistency** — lat/lng agreeing with easting/northing, route length matching summed GPS distance, `pole_bend` starting at a chamber.
- **Conditional presence** — dimension fields required for `repair_installation`, `TM_BOARD` required when traffic management is active.
- **Anything an adopter may switch off.** Schema constraints are absolute; controllable rules are not.

A field range that is always true regardless of context (a latitude is between −90 and 90) is a schema constraint. A range that is only true in a context (a latitude is within UK bounds *for a UK submission*) is a rule.

## Checking it

```sh
python3 tools/check_field_completeness.py            # summary + every gap; exit 1 if any
python3 tools/check_field_completeness.py --report   # per-field T/D/C table
python3 tools/check_field_completeness.py --json     # machine-readable
```

This one and `sync_slot_codes.py` use the standard library only, so they run on any Python 3.11+ with nothing installed. That is deliberate — reading and checking the standard shouldn't require setting up a toolchain.

v0.1 passes clean, so CI runs the plain check and any new or edited field has to meet the rule to merge.

A **ratchet** mode exists for the case where a future version needs to land gaps deliberately: a baseline file lists the fields not yet meeting the rule, and the check fails only on gaps that are *not* in it.

```sh
python3 tools/check_field_completeness.py --write-baseline tools/field-completeness-baseline.json
python3 tools/check_field_completeness.py --baseline tools/field-completeness-baseline.json
```

The baseline may only shrink; regenerating it to accommodate a new gap is a deliberate act, visible in the diff. Delete it and drop the flag once it reaches empty.

Two related checks run alongside:

```sh
python3 tools/sync_slot_codes.py --check   # slotCode enum still matches evidence/slots.json
uv run tools/validate_examples.py          # schemas are valid 2020-12; examples validate
```

`validate_examples.py` runs two passes. First it checks every schema against the **2020-12 meta-schema**, so a typo'd keyword or a malformed construct is caught rather than silently doing nothing — `"maxLength": "255"` as a string, for instance, imposes no limit at all and produces no error without this pass. Then it validates the examples. An invalid schema stops the run, because example results mean nothing if the schema itself is broken.

`validate_examples.py` exists because the schemas carry absolute `$id` URLs under `https://openpia.org/`. A validator left to itself resolves those `$id`s against that base over the network — which would make CI depend on the website serving the schema files. Building the reference registry from the local files instead keeps validation offline and self-contained.

It is the one tool with a dependency: **`jsonschema>=4.18`**, pinned in [`../tools/requirements.txt`](../tools/requirements.txt). The floor matters — the `referencing` library the registry is built on only arrived in 4.18, so an older version fails in a way that looks like a missing package. Three ways to satisfy it, in order of least fuss:

```sh
uv run tools/validate_examples.py            # PEP 723 header; uv provisions it, no venv
python3 tools/validate_examples.py           # if you already have jsonschema>=4.18
pip install -r tools/requirements.txt        # or into a virtual environment
```

There is deliberately **no virtual environment in the repo**. Most people who touch OpenPIA read JSON and Markdown and never run a script, so a Python setup step shouldn't stand between them and the standard.
