# Working with cohorts

Strategus studies run on cohorts defined in ATLAS. rD2E brings those definitions into your notebook.

## Find the IDs

1. In ATLAS, open **Cohort Definitions**.
2. Find your cohorts. The **ID** column is the number to use in R.
3. Note which cohorts are targets, comparators and outcomes for your study.

## Load them

```r
cohortDefinitionSet <- get_cohort_definition_set(
  cohortIds = c(44, 49, 50),
  generateStats = TRUE
)
```

Use one call for all the cohorts in your study. The result goes into the specification as shared resources:

```r
cohortResources <- createCohortSharedResourceSpecifications(
  cohortDefinitionSet = cohortDefinitionSet)
```

## Check before you build

A quick check catches a wrong or missing ID before you submit:

```r
stopifnot(identical(as.integer(cohortDefinitionSet$cohortId), c(44L, 49L, 50L)))
print(cohortDefinitionSet[, c("cohortId", "cohortName", "generateStats")])
```

The IDs you use later in module settings (targets, outcomes) must be IDs you loaded here.

## Keep `generateStats` consistent

`generateStats` in `get_cohort_definition_set()` should match `generateStats` in the Cohort Generator module:

```r
cgSpecs <- createCohortGeneratorModuleSpecifications(generateStats = TRUE)
```

## Changed a cohort in ATLAS?

The notebook holds the definition as it was when you loaded it. After editing a cohort in ATLAS, run the `get_cohort_definition_set()` cell again, and the cells after it.

## Create a cohort from the notebook

[create_cohort_definition()](../reference/create_cohort_definition.md) creates a new cohort definition in ATLAS, for example a copy of an existing one under a new name. [TO VERIFY]

## See also

- [get_cohort_definition_set()](../reference/get_cohort_definition_set.md)
- [Troubleshooting](troubleshooting.md)
