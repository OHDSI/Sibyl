# Notebook onboarding for researchers

Source for the onboarding deck. Each `## Slide` section becomes one slide. The `Notes:` block under each slide is the speaker note.

Status markers used in this document:
- **[VERIFIED]**: confirmed in source on `origin/develop` (commit 242febe).
- **[TO VERIFY]**: not confirmed from source. Check before presenting.
- **[PLACEHOLDER]**: waiting on information from the D2E backend.

---

## Slide 1: Notebook onboarding for Strategus analysis design

Subtitle: Design Strategus analysis specifications in the notebook, and submit them to d2e.

Notes: This session covers the notebook, the R helpers for cohorts and specifications, and how to submit a run. The results viewer is a separate follow-up session.

---

## Slide 2: Who this is for, and what you need

- Data science team members working on OHDSI studies
- R-first: examples in this session are R. Python is covered only where it differs.
- Working knowledge of OHDSI concepts (cohorts, outcomes, time-at-risk) helps, but is not required for the basics.
- **[PLACEHOLDER] Access:** access to the notebook is granted on request. Insert the request process and who approves it once the D2E backend details are confirmed.
- What you can do with access: view, build and run notebooks.

Notes: Access is by request. Do not describe the approval mechanism until it is confirmed.

---

## Slide 3: What the notebook is

- A notebook is a list of cells. Each cell is either **code** or **markdown**. **[VERIFIED]** (`plugins/notebook/README.md`)
- Code cells run in your browser. R code runs in the WebR kernel, which is R compiled to WebAssembly. Python runs in the Pyodide kernel. **[VERIFIED]** (`plugins/notebook/src/kernels/webr/WebRKernel.ts`, `plugins/notebook/src/kernels/pyodide/PyodideKernel.ts`)
- Nothing runs on a server while you edit. Only the submission step (`run_strategus_flow`) calls the d2e backend. **[VERIFIED]** (`plugins/notebook-plugin/src/kernels/rD2E.R`)
- Run a cell with Shift+Enter, or use **Run All** in the toolbar. **[VERIFIED]** (`plugins/notebook/README.md`, `NotebookToolbar.vue`)

Notes: The main point is that editing and building the spec happen in the browser. Only submission needs the backend.

---

## Slide 4: Anatomy of the screen

- **Toolbar:** Run All, Undo and Redo, and the kernel status indicator. **[VERIFIED]** (`plugins/notebook/src/components/notebook/NotebookToolbar.vue`)
- **Kernel status:** shows whether the kernel is starting, ready, busy (running), or in error. **[VERIFIED]** (`NotebookToolbar.vue`: "Running…", error text "The kernel could not start. Run a cell to try again.")
- **Cells:** code cells with syntax highlighting, and rendered markdown cells.
- **Save state:** a "Saved" chip appears when the notebook matches the last saved version. **[TO VERIFY]** This is on the feature branch `SantanM/internal-3570_fix-notebook-state` and is not yet on `develop`. Confirm it is merged before presenting.

Notes: The Saved chip comes from work still in review on the feature branch. Say "when it is available" or confirm it is merged first.

---

## Slide 5: Saving, unsaved changes, and import/export

- Notebooks are saved to the notebook service, which stores them in Postgres. **[VERIFIED]** (`plugins/notebook-plugin/src/api/notebookGit.ts`, comment on the mirror setting; `graphqlClient.ts` carries the requests)
- If you leave the page or switch notebooks with unsaved edits, the editor asks you to confirm and warns that the edits will be lost. **[VERIFIED]** (`plugins/notebook-plugin/src/views/NotebookEditorView.vue`)
- Import and export use the Jupyter `.ipynb` format. **[VERIFIED]** (`plugins/notebook/src/utils/serialization.ts`)
- The optional Git mirror is currently **off**, so pushing to a Git repository is not available yet. **[VERIFIED]** (`plugins/notebook-plugin/src/api/notebookGit.ts`, `GIT_MIRROR_ENABLED = false`)

Notes: Save before you leave the page. Do not present the Git mirror as available.

---

## Slide 6: Kernels and R packages

### What is available in the R kernel

- The R kernel (WebR) starts with the Strategus spec builder already loaded, so the `create_*` and `set*` helpers are available without installing anything. **[VERIFIED]** (`WebRKernel.ts` sources `StrategusSpecBuilder.R` on connect)
- The spec builder needs `checkmate`, which the kernel installs on startup. **[VERIFIED]**
- The rD2E helpers (`get_cohort_definition_set`, `create_cohort_definition`, `create_options`, `run_strategus_flow`) are loaded on top of the R kernel. **[VERIFIED]** (`rD2EBootstrap.ts`)
- Strategus package names (`Strategus`, `CohortMethod`, `Characterization`, `PatientLevelPrediction` and others) are treated as already loaded. `library(Characterization)` succeeds without installing anything. **[VERIFIED]** (`WebRKernel.ts` shim list)

### Installing a package that is not available

- Add a line such as `library(ggplot2)` to a cell. If the package is missing, the kernel tries to install it with `webr::install()` and then loads it. **[VERIFIED]** (`WebRKernel.ts`, the `library` shim)
- A package can also be listed for preloading when the kernel connects, and the kernel then runs `webr::install()` for each one. **[VERIFIED]** (`WebRKernel.ts`, `preloadPackages`). Researchers cannot set this list; it is configured by the platform.
- Install from the WebR package repository. Whether the repository is a mirror and which packages it carries is **[TO VERIFY]**.

### Checking what is installed

- **[TO VERIFY]** No helper for listing installed packages was found in source. Confirm with a plain R call such as `installed.packages()[, "Package"]` in a cell, and confirm that it works in the notebook session.

### Known limitations

- **Session loss on page refresh.** The R session runs in the browser tab, so refreshing the page is expected to start a new session and lose objects in memory. **[TO VERIFY]** Not yet confirmed in source; test it in the notebook before presenting.
- **Long sessions and expired tokens.** Environment variables are set once, when the kernel connects. A session left open longer than the login token's lifetime can start failing submissions. Refresh the page and run again. **[VERIFIED]** (`docs/follow-ups/stale-token-on-long-webr-session.md`, status OPEN)
- **Memory and speed.** WebR runs in the browser, so large data and heavy computation are limited by the browser. **[TO VERIFY]** Confirm limits with the team.
- **Threads.** WebR runs single-threaded. **[TO VERIFY]**
- **Network.** Packages install from the WebR repository, so a blocked network stops installs. **[TO VERIFY]**

Notes: Mark each TO VERIFY item before presenting. Do not present them as facts.

---

## Slide 7: rD2E at a glance

- rD2E is the helper library that connects the notebook to the d2e backend. It is loaded for you; you do not install it.
- Its helpers fall into three groups:
  1. **Cohorts:** `get_cohort_definition_set`, `create_cohort_definition`
  2. **Run options:** `create_options`
  3. **Submission:** `run_strategus_flow`
- Helpers that call the backend need you to be signed in to d2e. You do not set any credentials in the notebook.

Notes: Do not show environment variables or authentication internals. These are part of the platform and not user-managed.

---

## Slide 8: Cohort definitions

### Find cohorts: `get_cohort_definition_set(cohortIds, generateStats = FALSE)`

- Takes one or more cohort IDs and returns a cohort definition set.
- `generateStats = TRUE` also asks for cohort statistics. **[VERIFIED]** (`rD2E.R`)
- Errors if the ID vector is empty. **[VERIFIED]**

```r
cohorts <- get_cohort_definition_set(c(1234, 5678))
```

### Create a cohort: `create_cohort_definition(name, description, cohort_definition)`

- Creates a new cohort definition on the backend. Needs a name, a description, and the cohort definition itself. **[VERIFIED]** (`rD2E.R`)
- Creation calls the backend, so it needs d2e access.

**[TO VERIFY]** the exact format of `cohort_definition` (Atlas JSON or a list) and the ID returned. Confirm with a test cohort before the session.

Notes: Use IDs from your own study. Replace the example IDs in the session.

---

## Slide 9: What a Strategus analysis specification is

- A Strategus analysis specification is the full description of a study: the shared cohorts, plus the modules (analyses) to run on them.
- It has two parts. **Shared resources** hold the cohorts. **Module specifications** hold each analysis (cohort generation, characterization, and so on). **[VERIFIED]** (`StrategusSpecBuilder.R`: `createEmptyAnalysisSpecifications`, `addSharedResources`, `addModuleSpecifications`)
- You build it with helpers in the notebook. Nothing is submitted until you call `run_strategus_flow`.

Notes: Keep this slide short. The next slides show the building steps.

---

## Slide 10: Building a spec with StrategusSpecBuilder

The builder has three kinds of helper:

- Analyses with other module types (CohortMethod, SCCS, PatientLevelPrediction) follow the same pattern. Their `create*ModuleSpecifications` helpers exist in `StrategusSpecBuilder.R`. **[VERIFIED]**
- Helpers check their inputs and raise an error with a clear message if an input is wrong. **[VERIFIED]** (uses `checkmate` assertions)

| Kind | Examples | Purpose |
|---|---|---|
| Create a container | `createEmptyAnalysisSpecifications()` | Start an empty spec |
| Create a part | `createCohortSharedResourceSpecifications()`, `createCohortGeneratorModuleSpecifications()`, `createCharacterizationModuleSpecifications()` | Build one shared resource or one module |
| Add a part | `addSharedResources()`, `addModuleSpecifications()` | Attach the part to the spec |

Notes: Show the table, then go straight to the worked example.

---

## Slide 11: Worked example: Characterization

Goal: characterize two cohorts (one target, one outcome) with the default settings, and submit the spec.

```r
# 1. Start an empty spec
spec <- createEmptyAnalysisSpecifications()

# 2. Load the cohorts used in the study
cohortSet <- get_cohort_definition_set(c(1234, 5678))  # replace with your IDs

# 3. Add the cohorts as shared resources
spec <- addSharedResources(spec, createCohortSharedResourceSpecifications(cohortSet))

# 4. Add the cohort generator module, so cohorts are built before analysis
spec <- addModuleSpecifications(spec, createCohortGeneratorModuleSpecifications(generateStats = TRUE))

# 5. Add the characterization module: target 1234, outcome 5678
spec <- addModuleSpecifications(spec,
  createCharacterizationModuleSpecifications(targetIds = c(1234), outcomeIds = c(5678)))
```

Then build the options and submit:

```r
runOptions <- create_options(source_token_study_code = "YOUR_SOURCE_CODE",
                             upload_results = FALSE)
flow <- run_strategus_flow(spec, options = runOptions)
```

- `targetIds` and `outcomeIds` must match cohort IDs in the set. **[TO VERIFY]** the cohort IDs in `cohortSet` must include the target and outcome IDs passed to the module.
- `run_strategus_flow` returns the flow run ID as `flow$flowrunId`. **[VERIFIED]** (`rD2E.R`, the success message)
- **[PLACEHOLDER]** Insert the source study code and the upload options your study uses.

Notes: Run cell by cell. If a step fails, the error message comes from the helper, so read it first.

---

## Slide 12: `create_options` and `run_strategus_flow`

- `create_options(...)` builds the run options: which dataset to use, whether to upload results, and whether to update the results schema. **[VERIFIED]** (`rD2E.R`)
- Defaults: `upload_results = FALSE`, `update_results_schema = TRUE`, `run_table1 = FALSE`. **[VERIFIED]**
- `run_strategus_flow(spec, executionSettings = NULL, options = ...)` submits the spec. `options` is required. **[VERIFIED]**
- A successful submission returns a flow run ID. Run status is handled by the platform team, not in this session.

Notes: Do not teach run status checks for researchers. Admin-only.

---

## Slide 13: Common errors and troubleshooting

| What you see | What to do |
|---|---|
| `options must be provided; use create_options() to build them` | Pass the result of `create_options()` as `options`. **[VERIFIED]** |
| `Request failed with status code ...` | The submission was rejected. Check that you are still signed in, then refresh and run again. **[TO VERIFY]** the common causes with the platform team. |
| `Must provide a non-zero length cohortIds vector.` | Pass at least one cohort ID to `get_cohort_definition_set`. **[VERIFIED]** |
| Cohort or module assertion error from `checkmate` | Read the message: it names the argument that failed. **[VERIFIED]** |
| Submissions fail after a long time open | Refresh the page to start a new session, then run again. **[VERIFIED]** (stale-token follow-up; the refresh step is **[TO VERIFY]**) |
| `library(X)` fails | The kernel tries to install X. If it still fails, the package may not be in the WebR repository. **[TO VERIFY]** |

Notes: The "long session" row is the most common cause of confusing failures. Stress it.

---

## Slide 14: Known limitations and what is coming

- Session state lives in the browser. Refreshing starts a new session. **[TO VERIFY]**
- Expired-token failures in long sessions are a known open issue. **[VERIFIED]**
- Pushing notebooks to a Git repository is off. **[VERIFIED]**
- **Coming later:** the results viewer, in a follow-up session.

---

## Slide 15: Where to get help, and where these docs live

- Maintained guide: `docs/user-guide/researcher-onboarding.md` in the trex-notebook repository.
- Notebook README: `plugins/notebook/README.md`
- **[PLACEHOLDER]** Support channel and contact.
- **[PLACEHOLDER]** Access request process.
