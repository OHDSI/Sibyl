# Notebook user guide

- `researcher-onboarding.md`: source for the researcher onboarding deck. Each `## Slide N` section is one slide, and each `Notes:` block is the speaker note.
- `researcher-onboarding.pptx`: generated deck. Regenerate it after editing the markdown.
- `build_deck.py`: builder script (requires `python-pptx`).

## Regenerate the deck

```bash
pip install python-pptx
python docs/user-guide/build_deck.py docs/user-guide/researcher-onboarding.md docs/user-guide/researcher-onboarding.pptx
```

## Review markers

- `[VERIFIED]` in the markdown: confirmed in source. These are stripped from slides.
- `[TO VERIFY]` and `[PLACEHOLDER]`: kept on slides and highlighted in amber. Resolve each one before presenting.
