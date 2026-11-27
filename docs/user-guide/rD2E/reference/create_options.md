# create_options()

Choose which dataset a study runs on and how its results are named, before you submit it with [run_strategus_flow()](run_strategus_flow.md).

## Usage

```r
create_options(source_token_study_code, analysis_results_name = NULL)
```

## Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `source_token_study_code` | text | the current session's dataset | The code of the dataset to run on, for example `"my_dataset"`. [TO VERIFY] which dataset is used when you leave it out, and where researchers find a dataset's code. |
| `analysis_results_name` | text | none | A name for this set of results, for example `"t2d_incidence_v1"`. One string, at most 255 characters, no control characters. Spaces at either end are removed; an empty name is ignored. |

## Value

A list of run options to pass as `options` to [run_strategus_flow()](run_strategus_flow.md). Nothing is sent to D2E by this function.

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

`datasetId` is the code you passed as `source_token_study_code`.

## See also

- [run_strategus_flow()](run_strategus_flow.md)
- [Submitting a study](../guides/submitting-a-study.md)
