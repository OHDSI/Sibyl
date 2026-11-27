# rD2E user guide

rD2E connects R code in the D2E notebook to D2E. With it you can load cohort definitions from ATLAS, create new ones, and submit a Strategus analysis specification to run on a D2E dataset.

## Where it works

- In **R cells** of the D2E notebook (ATLAS → **Studies** → open or create a notebook).
- It is loaded for you. You don't need to install anything. `library(rD2E)` is accepted but not required.
- R's built-in help (`?get_cohort_definition_set`) is not available for rD2E. This guide is the reference.

## The four functions

| Function | What it does |
|---|---|
| [`get_cohort_definition_set()`](reference/get_cohort_definition_set.md) | Load cohort definitions from ATLAS by ID |
| [`create_cohort_definition()`](reference/create_cohort_definition.md) | Create a new cohort definition in ATLAS |
| [`create_options()`](reference/create_options.md) | Choose the dataset and result settings for a run |
| [`run_strategus_flow()`](reference/run_strategus_flow.md) | Submit an analysis specification to D2E |

## How they fit together

```
ATLAS cohort IDs
   → get_cohort_definition_set()      load the cohorts
   → build the analysis specification  (Strategus functions)
   → create_options()                  pick the dataset, name the results
   → run_strategus_flow()              submit; returns a flow run ID
```

## Contents

- [Getting started](getting-started.md): a complete example, start to finish
- Reference: [get_cohort_definition_set](reference/get_cohort_definition_set.md) · [create_cohort_definition](reference/create_cohort_definition.md) · [create_options](reference/create_options.md) · [run_strategus_flow](reference/run_strategus_flow.md)
- Guides: [Working with cohorts](guides/working-with-cohorts.md) · [Submitting a study](guides/submitting-a-study.md) · [Troubleshooting](guides/troubleshooting.md)
