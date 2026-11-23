# create_cohort_definition()

Create a new cohort definition in ATLAS from R.

> **Not yet checked on the test host.** Everything on this page comes from the source code. Run the example on the test host before relying on it. [TO VERIFY]

## Usage

```r
create_cohort_definition(name, description, cohort_definition)
```

## Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `name` | text | required | Name of the new cohort. Must not be empty. |
| `description` | text | required | Description of the new cohort. Must not be empty. |
| `cohort_definition` | list or JSON text | required | The cohort definition. Either the definition itself, or an ATLAS export that has an `expression` field (and optionally `expressionType`). |

If `expressionType` is not given, `SIMPLE_EXPRESSION` is used.

## Value

The new cohort definition as stored in ATLAS, as a list. Its `id` is the new cohort ID to use in [get_cohort_definition_set()](get_cohort_definition_set.md). [TO VERIFY] the other fields returned.

The new cohort is tagged `created_by_rD2E`, so you can find it in ATLAS → Cohort Definitions.

## Messages you'll see

```
Cohort definition created successfully with id: <new id>
```

## Errors

| Message | Cause | Fix | Checked |
|---|---|---|---|
| `Name must be provided and cannot be empty.` | `name` is missing or `""` | Give the cohort a name | source |
| `Description must be provided and cannot be empty.` | `description` is missing or `""` | Add a description | source |
| `Cohort definition must be provided and cannot be empty.` | `cohort_definition` is empty | Pass the definition | source |
| `cohort_definition must be a list or a JSON string.` | Wrong type, for example a number | Pass a list or JSON text | source |
| `Cohort definition JSON must contain an 'expression' field.` | The export has an `expression` field, but it is empty | Use a complete ATLAS export | source |
| `Status code: <code>` then `Error occurred while creating cohort definition for cohort: <name>` | D2E refused to create it, for example because your session expired | Sign in again and retry; if it persists, contact the platform team | source |

## Examples

Copy an existing cohort under a new name:

```r
existing <- get_cohort_definition_set(50)

newCohort <- create_cohort_definition(
  name              = "Postpartum T2D (copy for sensitivity analysis)",
  description       = "Copy of cohort 50, created from the notebook",
  cohort_definition = existing$json[1]
)

newCohort$id   # the new cohort's ID
```

[TO VERIFY] This example has not been run. Running it creates a real cohort definition in ATLAS.

## See also

- [get_cohort_definition_set()](get_cohort_definition_set.md)
- [Working with cohorts](../guides/working-with-cohorts.md)

---

From the source of trex-notebook `242febe`. Not yet checked on internal.d2e.sg.
