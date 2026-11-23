# Getting started

This walkthrough follows a real study from the notebook *GUSTO-incidence-strategus_v1* on the test host: the incidence of postpartum type 2 diabetes in pregnancies with and without gestational diabetes (GDM). It runs on the `gusto_v3` dataset.

## 1. Find your cohort IDs

In ATLAS, open **Cohort Definitions**. The **ID** column is the number you use in R. This example uses:

| ID | Cohort |
|---|---|
| 44 | GDM Cohort |
| 49 | gusto_nongdm_cohort |
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
2       49           gusto_nongdm_cohort          TRUE
3       50 Postpartum T2D Outcome Cohort          TRUE
```

## 3. Build the analysis specification

Building the specification uses Strategus functions, not rD2E. See the [Strategus documentation](https://ohdsi.github.io/Strategus/) for the modules and their settings. In this study:

```r
# The analysis: incidence of cohort 50 in cohorts 44 and 49 (see the notebook for irDesign)
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
  upload_results          = FALSE,
  source_token_study_code = "gusto_v3",
  analysis_results_name   = "gusto_t2d_outcome_source"
)
print(options)
```

```
$mode
[1] "kernel"
$datasetId
[1] "gusto_v3"
$uploadResults
[1] FALSE
$updateResultsSchema
[1] TRUE
$tokenStudyCode
[1] ""
$runTable1
[1] FALSE
$analysisResultsName
[1] "gusto_t2d_outcome_source"
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

---

Checked on internal.d2e.sg, 2026-11-23, against trex-notebook `242febe`. Steps 1–4 were run live. Step 5 shows the real output saved in the notebook from an earlier run; it was not re-run for this guide.
