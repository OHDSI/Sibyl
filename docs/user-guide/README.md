# User guides

Documentation for researchers who use the D2E notebook. Each guide has a Markdown source (the one to edit) and a generated file to share.

| Guide | Source | Generated | Builder |
|---|---|---|---|
| Notebook onboarding deck | `researcher-onboarding.md` (+ screenshots in `img/`) | `researcher-onboarding.pptx` | `build_deck.py` |
| rD2E user guide | `rD2E/*.md`, `rD2E/reference/`, `rD2E/guides/` | `rD2E/rD2E-user-guide.html` | `rD2E/build_html.py` |

## Regenerate

```bash
pip install python-pptx markdown
```

```bash
python docs/user-guide/build_deck.py docs/user-guide/researcher-onboarding.md docs/user-guide/researcher-onboarding.pptx
```

```bash
python docs/user-guide/rD2E/build_html.py
```

The rD2E HTML page is also published as a claude.ai artifact. After regenerating it, republish it to the same artifact link.

## Writing rules

- Describe only what a researcher sees or types. Leave out storage, endpoints, environment variables and internal helpers.
- R only.
- Check examples and messages on the test host (`internal.d2e.sg`). Record where and when in the page footer, and in error tables mark each message `host` (reproduced) or `source` (read from the code).
- `[TO VERIFY]` and `[PLACEHOLDER]` are highlighted in both outputs. Resolve them before presenting or sharing.
- The deck's Markdown format is described at the top of `researcher-onboarding.md`.

## Keeping the rD2E guide in sync

rD2E is defined in `plugins/notebook-plugin/src/kernels/rD2E.R`. When a function's arguments, return value or messages change, update its page in `rD2E/reference/` and the table in `rD2E/guides/troubleshooting.md` in the same change.

## Git

The root `.gitignore` ignores `docs/`, so add files here with `git add -f`.
