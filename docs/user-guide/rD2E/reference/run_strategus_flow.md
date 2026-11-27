# run_strategus_flow()

Submit a Strategus analysis specification to D2E. D2E starts a run (a "flow run") on the dataset chosen in your options.

## Usage

```r
run_strategus_flow(analysisSpecification, executionSettings = NULL, options = list())
```

## Arguments

| Argument | Type | Default | Meaning |
|---|---|---|---|
| `analysisSpecification` | analysis specification | required | The specification you built: cohorts plus modules. |
| `executionSettings` | | `NULL` | Leave as `NULL`. |
| `options` | list | required | The result of [create_options()](create_options.md). |

## Value

A list with two elements:

| Element | Contents |
|---|---|
| `flowrunId` | The ID of the new run. Keep it: it identifies your run when you ask about it. |
| `status` | `"Successfully created a flow run"` |

```r
print(result)
```

```
$flowrunId
[1] "923fb707-c76f-45cd-ba05-4a8c8d03a214"
$status
[1] "Successfully created a flow run"
```

A flow run ID means D2E **accepted** the run. It does not mean the analysis has finished or succeeded.

## Important

- **Every call submits a new run.** Running the cell twice submits the study twice.
- **Run All** in the notebook runs this cell too. Keep the submit cell last, and run it on purpose.

## Examples

```r
result <- run_strategus_flow(
  analysisSpecification = analysisSpecifications,
  executionSettings     = NULL,
  options               = options
)

result$flowrunId   # keep this
```

## See also

- [create_options()](create_options.md)
- [Submitting a study](../guides/submitting-a-study.md)
