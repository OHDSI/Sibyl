# create_options()

Choose which dataset a study runs on and how its results are named, before you submit it with [run_strategus_flow()](run_strategus_flow.md).

## Usage

```r
create_options(
  token_study_code        = "",
  source_token_study_code,
  upload_results          = FALSE,
  update_results_schema   = TRUE,
  run_table1              = FALSE,
  analysis_results_name   = NULL
)
```

## Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `source_token_study_code` | text | the current session's dataset | The dataset to run on, for example `"gusto_v3"`. [TO VERIFY] which dataset is used when you leave it out, and where researchers find a dataset's code. |
| `analysis_results_name` | text | none | A name for this set of results, for example `"gusto_t2d_outcome_source"`. One string, at most 255 characters, no control characters. Spaces at either end are removed; an empty name is ignored. |
| `upload_results` | `TRUE` / `FALSE` | `FALSE` | Whether to upload the results. The team's notebooks use `FALSE`. [TO VERIFY] what changes with `TRUE`. |
| `token_study_code` | text | `""` | Leave empty. [TO VERIFY] when it is needed. |
| `update_results_schema` | `TRUE` / `FALSE` | `TRUE` | Leave at the default. [TO VERIFY] its effect. |
| `run_table1` | `TRUE` / `FALSE` | `FALSE` | Leave at the default. [TO VERIFY] its effect. |

Most studies only need `source_token_study_code` and `analysis_results_name`.

## Value

A list of run options to pass as `options` to [run_strategus_flow()](run_strategus_flow.md). Nothing is sent to D2E by this function.

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

`datasetId` is the code you passed as `source_token_study_code`.

## Messages you'll see

None.

## Errors

These are checked before anything is submitted, so a bad name fails here and not halfway through a run.

| Message | Cause | Fix | Checked |
|---|---|---|---|
| `analysis_results_name must be a single string` | More than one name, a number, or `NA` | Pass one piece of text | source |
| `analysis_results_name must not contain control characters` | The name contains a line break, tab or similar | Remove them | source |
| `analysis_results_name must be at most 255 characters` | The name is too long | Shorten it | source |

## See also

- [run_strategus_flow()](run_strategus_flow.md)
- [Submitting a study](../guides/submitting-a-study.md)

---

Checked on internal.d2e.sg, 2026-11-23, against trex-notebook `242febe`. The example output is from a live run.
