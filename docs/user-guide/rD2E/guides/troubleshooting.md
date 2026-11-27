# Troubleshooting

Every message rD2E can show, with what to do.

## Signed out

| You see | What to do |
|---|---|
| ATLAS shows *Your session has expired. Please sign in again.* | Sign in again. Then run your cells again from the top: the notebook's R session starts fresh. |

Long sessions also expire. If rD2E calls start failing after the notebook has been open a long time, sign in again (reload the page if needed) and re-run your cells.

## get_cohort_definition_set()

| Message | What to do |
|---|---|
| `Fetching cohortId: <id>` (red) | Nothing. It's a progress message. |
| `Must provide a non-zero length cohortIds vector.` | Pass at least one cohort ID |
| `HTTP GET failed with status <code>: <details>` | Check the ID exists in ATLAS → Cohort Definitions. If you were signed out, sign in again and re-run. |

## create_cohort_definition()

| Message | What to do |
|---|---|
| `Name must be provided and cannot be empty.` | Give the cohort a name |
| `Description must be provided and cannot be empty.` | Add a description |
| `Cohort definition must be provided and cannot be empty.` | Pass the definition |
| `cohort_definition must be a list or a JSON string.` | Pass a list or JSON text |
| `Cohort definition JSON must contain an 'expression' field.` | Use a complete ATLAS export |
| `Error occurred while creating cohort definition for cohort: <name>` | Sign in again and retry; if it persists, contact the platform team with the status code shown above it |

## create_options()

| Message | What to do |
|---|---|
| `analysis_results_name must be a single string` | Pass one piece of text |
| `analysis_results_name must not contain control characters` | Remove line breaks and tabs |
| `analysis_results_name must be at most 255 characters` | Shorten the name |

## run_strategus_flow()

| Message | What to do |
|---|---|
| `options must be provided; use create_options() to build them` | Pass `options = create_options(...)`. Nothing was submitted. |
| `Request failed with status code <code>` | Sign in again, re-run your cells, then submit again. If it persists, contact the platform team with the code. |

## Not an rD2E message, but common

| You see | What to do |
|---|---|
| `Requested package <name> not found in webR binary repo.` | The package isn't available in the notebook. Contact the platform team. |
| `object 'cohortDefinitionSet' not found` (or another name) [TO VERIFY] exact wording | A cell above wasn't run. Run the cells from the top. |
