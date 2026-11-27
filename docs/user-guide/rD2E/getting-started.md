# Getting started

This walkthrough follows an example study: the incidence of postpartum type 2 diabetes in pregnancies with and without gestational diabetes (GDM). Replace the cohort IDs, dataset code and results name with your own.

## 1. Find your cohort IDs

In ATLAS, open **Cohort Definitions**. The **ID** column is the number you use in R. This example uses:

| ID | Cohort |
|---|---|
| 44 | GDM Cohort |
| 49 | Non-GDM Cohort |
| 50 | Postpartum T2D Outcome Cohort |

## 2. Load the cohorts

```r
library(Strategus)
library(CohortIncidence)

cohortDefinitionSet <- get_cohort_definition_set(
  cohortIds = c(44, 49, 50),
  generateStats = TRUE
)
```

The notebook prints one line per cohort (in red; these are progress messages, not errors):

```
Fetching cohortId: 44
Fetching cohortId: 49
Fetching cohortId: 50
```

Check what you loaded:

```r
print(cohortDefinitionSet[, c("cohortId", "cohortName", "generateStats")])
```

```
  cohortId                    cohortName generateStats
1       44                    GDM Cohort          TRUE
2       49                Non-GDM Cohort          TRUE
3       50 Postpartum T2D Outcome Cohort          TRUE
```

## 3. Build the analysis specification

Building the specification uses Strategus functions, not rD2E. See the [Strategus documentation](https://ohdsi.github.io/Strategus/) for the modules and their settings. In this study:

```r
# The analysis: incidence of cohort 50 in cohorts 44 and 49 (irDesign is defined in an earlier cell)
ciModule <- Strategus::CohortIncidenceModule$new()
ciSpecs  <- ciModule$createModuleSpecifications(irDesign = irDesign)

# The cohorts, shared by every module, and the step that generates them
cohortResources <- createCohortSharedResourceSpecifications(
  cohortDefinitionSet = cohortDefinitionSet)
cgSpecs <- createCohortGeneratorModuleSpecifications(generateStats = TRUE)

# Put it together: cohorts first, then Cohort Generator, then the analysis
analysisSpecifications <- createEmptyAnalysisSpecifications()
analysisSpecifications$sharedResources <- list(cohortResources)
analysisSpecifications <- addModuleSpecifications(analysisSpecifications, cgSpecs)
analysisSpecifications <- addModuleSpecifications(analysisSpecifications, ciSpecs)
```

## 4. Choose the run options

```r
options <- create_options(
  source_token_study_code = "my_dataset",
  analysis_results_name   = "t2d_incidence_v1"
)
options[c("datasetId", "analysisResultsName")]
```

```
$datasetId
[1] "my_dataset"
$analysisResultsName
[1] "t2d_incidence_v1"
```

## 5. Submit

Run this once. Every run of this cell submits a new study run.

```r
result <- run_strategus_flow(
  analysisSpecification = analysisSpecifications,
  executionSettings     = NULL,
  options               = options
)
```

```
Strategus flow run triggered successfully with id: 923fb707-c76f-45cd-ba05-4a8c8d03a214
```

```r
print(result)
```

```
$flowrunId
[1] "923fb707-c76f-45cd-ba05-4a8c8d03a214"
$status
[1] "Successfully created a flow run"
```

The flow run ID means D2E accepted the run. It does not mean the analysis has finished. See [Submitting a study](guides/submitting-a-study.md) for what happens next.
