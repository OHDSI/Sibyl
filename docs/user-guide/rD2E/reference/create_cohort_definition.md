# create_cohort_definition()

Create a new cohort definition in ATLAS from R.

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

Running this creates a real cohort definition in ATLAS. [TO VERIFY]

## See also

- [get_cohort_definition_set()](get_cohort_definition_set.md)
- [Working with cohorts](../guides/working-with-cohorts.md)
