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
| `executionSettings` | | `NULL` | Leave as `NULL`, as in all the team's notebooks. |
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

## Messages you'll see

```
Strategus flow run triggered successfully with id: 923fb707-c76f-45cd-ba05-4a8c8d03a214
```

## Important

- **Every call submits a new run.** Running the cell twice submits the study twice.
- **Run All** in the notebook runs this cell too. Keep the submit cell last, and run it on purpose.

## Errors

| Message | Cause | Fix | Checked |
|---|---|---|---|
| `options must be provided; use create_options() to build them` | `options` was not given | Pass `options = create_options(...)`. Nothing was submitted. | host |
| `Request failed with status code <code>` | D2E did not accept the run, for example because your session expired | Sign in again, re-run your cells, then submit again. If it persists, contact the platform team with the status code. | source |

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

---

Checked on internal.d2e.sg, 2026-11-23, against trex-notebook `242febe`. The success output is the real output saved in the GUSTO notebook from an earlier run; the submit cell was not re-run for this page.
