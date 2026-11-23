# Submitting a study

## Before you submit

- [ ] All cells above the submit cell have run without errors
- [ ] The cohort IDs you loaded match the ones used in your modules
- [ ] The Cohort Generator module comes before your analysis modules
- [ ] `source_token_study_code` names the dataset you mean to run on
- [ ] `analysis_results_name` describes this run, so you can tell it apart later
- [ ] The notebook is saved

## Choose the options

```r
options <- create_options(
  upload_results          = FALSE,
  source_token_study_code = "gusto_v3",
  analysis_results_name   = "gusto_t2d_outcome_source"
)
```

See [create_options()](../reference/create_options.md) for every argument. Most studies only need these two settings plus `upload_results = FALSE`, as in the team's notebooks.

## Submit once

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

Each run of this cell submits a new study run. Don't re-run it to "check" something, and be careful with **Run All**.

## What the result means

| You see | It means |
|---|---|
| `flowrunId` | D2E created a run with this ID |
| `status: "Successfully created a flow run"` | D2E accepted the run |

It does **not** mean the analysis finished or succeeded. Runs take time, and progress is tracked by the platform team. To ask about a run, send them the `flowrunId`.

## What happens next

- Results are reviewed in ATLAS → **Studies** → **Results**. That is covered in a separate guide.
- To change something, edit the cells, re-run them, and submit again. This creates a new run with a new ID.

## See also

- [run_strategus_flow()](../reference/run_strategus_flow.md)
- [Troubleshooting](troubleshooting.md)
