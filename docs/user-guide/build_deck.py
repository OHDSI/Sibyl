"""Build the onboarding .pptx from docs/user-guide/researcher-onboarding.md.

Each '## Slide N: title' section becomes one slide. Bullets, fenced code, and
pipe tables are rendered; 'Notes:' blocks become speaker notes. Internal source
citations and [VERIFIED] markers are stripped from slide text. [TO VERIFY] and
[PLACEHOLDER] markers are kept and highlighted so they cannot be presented by accident.
"""
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

SRC, OUT = sys.argv[1], sys.argv[2]

TEAL = RGBColor(0x0F, 0x4C, 0x5C)
INK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x55, 0x60, 0x6E)
AMBER = RGBColor(0xB4, 0x53, 0x09)
CODE_BG = RGBColor(0xF1, 0xF5, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def clean(text):
    """Strip internal citations and markdown emphasis, keep review flags."""
    text = text.replace("**[VERIFIED]**", "")
    text = re.sub(r"\s*\(\*\*\[VERIFIED\]\*\*[^()]*\)", "", text)
    text = re.sub(r"\s*\([^()]*(?:/|\.ts|\.vue|\.R\b|\.md|\.py|\.json|VERIFIED)[^()]*\)", "", text)
    text = re.sub(r"\s*\[VERIFIED\]", "", text)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    text = re.sub(r"\.\.(?!\.)", ".", text)
    return text.strip()


def parse(md):
    slides = []
    current = None
    in_code = False
    for line in md.splitlines():
        if line.startswith("## Slide "):
            current = {"title": line.split(":", 1)[1].strip(), "blocks": [], "notes": []}
            slides.append(current)
            continue
        if current is None:
            continue
        if line.strip() == "---":
            continue
        if line.startswith("```"):
            in_code = not in_code
            current["blocks"].append(("code_end" if not in_code else "code_start", None))
            continue
        if in_code:
            current["blocks"].append(("code", line))
            continue
        if line.startswith("Notes:"):
            current["notes"].append(line[len("Notes:"):].strip())
            current["_notes_mode"] = True
            continue
        if current.get("_notes_mode"):
            if line.strip():
                current["notes"].append(line.strip())
            continue
        if line.startswith("### "):
            current["blocks"].append(("sub", line[4:].strip()))
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            current["blocks"].append(("row", cells))
        elif re.match(r"^\s*- ", line):
            indent = (len(line) - len(line.lstrip())) // 2
            current["blocks"].append(("bullet", (indent, line.strip()[2:])))
        elif re.match(r"^\s*\d+\. ", line):
            current["blocks"].append(("bullet", (0, re.sub(r"^\s*\d+\. ", "", line).strip())))
        elif line.strip():
            current["blocks"].append(("text", line.strip()))
    return slides


def add_flag_runs(paragraph, text, size, color):
    """Add a text run, highlighting [TO VERIFY] and [PLACEHOLDER] tags in amber."""
    parts = re.split(r"(\[TO VERIFY\]|\[PLACEHOLDER\])", text)
    for part in parts:
        if not part:
            continue
        run = paragraph.add_run()
        run.text = part
        run.font.size = Pt(size)
        if part in ("[TO VERIFY]", "[PLACEHOLDER]"):
            run.font.bold = True
            run.font.color.rgb = AMBER
        else:
            run.font.color.rgb = color


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

for idx, s in enumerate(parse(open(SRC, encoding="utf-8").read()), start=1):
    slide = prs.slides.add_slide(blank)

    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.3))
    band.fill.solid()
    band.fill.fore_color.rgb = TEAL
    band.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(12), Inches(0.9))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    add_flag_runs(p, clean(s["title"]), 30, WHITE)
    for run in p.runs:
        run.font.bold = True

    body = slide.shapes.add_textbox(Inches(0.6), Inches(1.6), Inches(12.1), Inches(5.5))
    btf = body.text_frame
    btf.word_wrap = True
    first = True
    code_lines = []
    table_rows = []

    def new_para():
        global first
        if first:
            first = False
            return btf.paragraphs[0]
        return btf.add_paragraph()

    def flush_code():
        if not code_lines:
            return
        p = new_para()
        p.space_before = Pt(6)
        r = p.add_run()
        r.text = "\n".join(code_lines)
        r.font.name = "Menlo"
        r.font.size = Pt(13)
        r.font.color.rgb = INK
        code_lines.clear()

    def flush_table():
        if not table_rows:
            return
        rows, cols = len(table_rows), len(table_rows[0])
        n_text = 0 if first else len(btf.paragraphs)
        top = Inches(1.6) + Inches(0.6) * n_text
        tbl_shape = slide.shapes.add_table(rows, cols, Inches(0.6), top, Inches(12.1), Inches(0.45 * rows))
        tbl = tbl_shape.table
        for r_i, row in enumerate(table_rows):
            for c_i, val in enumerate(row):
                cell = tbl.cell(r_i, c_i)
                cell.text = ""
                para = cell.text_frame.paragraphs[0]
                add_flag_runs(para, clean(val), 13, WHITE if r_i == 0 else INK)
                if r_i == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = TEAL
                    for run in para.runs:
                        run.font.bold = True
        table_rows.clear()

    btf_top = [Inches(1.6)]
    for kind, val in s["blocks"]:
        if kind != "row" and table_rows:
            flush_table()
            btf_top[0] = Inches(1.6)
        if kind == "code":
            code_lines.append(val)
            continue
        if kind in ("code_end", "code_start"):
            flush_code()
            continue
        if kind == "row":
            table_rows.append(val)
            continue
        if kind == "sub":
            p = new_para()
            p.space_before = Pt(10)
            add_flag_runs(p, clean(val), 18, TEAL)
            for run in p.runs:
                run.font.bold = True
        elif kind == "bullet":
            indent, text = val
            p = new_para()
            p.level = min(indent, 4)
            p.space_before = Pt(6)
            add_flag_runs(p, "• " + clean(text) if indent == 0 else "– " + clean(text), 20 - 2 * indent, INK)
        elif kind == "text":
            p = new_para()
            p.space_before = Pt(8)
            add_flag_runs(p, clean(val), 18, MUTED)
    flush_code()
    flush_table()

    footer = slide.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12), Inches(0.35))
    fp = footer.text_frame.paragraphs[0]
    add_flag_runs(fp, f"Notebook onboarding  ·  {idx}", 10, MUTED)

    notes = " ".join(n for n in s["notes"] if n)
    if notes:
        slide.notes_slide.notes_text_frame.text = clean(notes)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
