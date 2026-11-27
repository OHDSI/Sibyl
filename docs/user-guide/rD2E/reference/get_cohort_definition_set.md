# get_cohort_definition_set()

Load cohort definitions from ATLAS into R, ready to use in a Strategus analysis specification.

## Usage

```r
get_cohort_definition_set(cohortIds, generateStats = FALSE)
```

## Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `cohortIds` | numeric vector | required | ATLAS cohort definition IDs (the **ID** column in ATLAS → Cohort Definitions). At least one. |
| `generateStats` | `TRUE` / `FALSE` | `FALSE` | Stored in the `generateStats` column of every row. Set it to match the `generateStats` you give the Cohort Generator module. |

## Value

A data frame with one row per cohort, in the order you asked for them:

| Column | Contents |
|---|---|
| `atlasId` | The ATLAS ID |
| `cohortId` | The same ID; this is the one Strategus uses |
| `cohortName` | The name in ATLAS |
| `sql` | Always empty in the notebook |
| `json` | The cohort definition, as JSON text |
| `logicDescription` | The description in ATLAS, or `NA` if there is none |
| `generateStats` | The value you passed |

```r
print(cohortDefinitionSet[, c("cohortId", "cohortName", "generateStats")])
```

```
  cohortId                    cohortName generateStats
1       44                    GDM Cohort          TRUE
2       49                Non-GDM Cohort          TRUE
3       50 Postpartum T2D Outcome Cohort          TRUE
```

## Examples

```r
# Load three cohorts and keep inclusion statistics
cohortDefinitionSet <- get_cohort_definition_set(
  cohortIds = c(44, 49, 50),
  generateStats = TRUE
)

# Check you got what you expected before building the specification
stopifnot(identical(as.integer(cohortDefinitionSet$cohortId), c(44L, 49L, 50L)))
print(cohortDefinitionSet[, c("cohortId", "cohortName")])
```

## See also

- [Working with cohorts](../guides/working-with-cohorts.md)
- [create_cohort_definition()](create_cohort_definition.md) to create a new cohort
- [Getting started](../getting-started.md)
