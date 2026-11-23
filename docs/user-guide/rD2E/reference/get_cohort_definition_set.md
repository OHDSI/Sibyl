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
2       49           gusto_nongdm_cohort          TRUE
3       50 Postpartum T2D Outcome Cohort          TRUE
```

## Messages you'll see

One line per cohort while it loads. They are shown in red but are not errors.

```
Fetching cohortId: 44
Fetching cohortId: 49
Fetching cohortId: 50
```

## Errors

| Message | Cause | Fix | Checked |
|---|---|---|---|
| `Must provide a non-zero length cohortIds vector.` | No IDs were given | Pass at least one ID | host |
| `HTTP GET failed with status <code>: <details>` | The cohort could not be loaded: for example the ID doesn't exist, or your session has expired | Check the ID in ATLAS; if you were signed out, sign in again and re-run your cells. [TO VERIFY] which status codes appear in each case | source |

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

---

Checked on internal.d2e.sg, 2026-11-23, against trex-notebook `242febe`.
