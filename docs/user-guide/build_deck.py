"""Build the onboarding deck from researcher-onboarding.md.

Usage:
    python build_deck.py researcher-onboarding.md researcher-onboarding.pptx

Markdown format (see the header of researcher-onboarding.md):
  ## Title            -> new slide (the first one is the title slide)
  Subtitle: text      -> subtitle (title slide only)
  - bullet            -> bullet; **bold**, `code` and *italic* are kept
  ![caption](path)    -> screenshot (right column, or full width without bullets)
  ```r ... ```        -> code block
  | a | b |           -> table (first row is the header)
  ::: flow / - step / :::  -> left-to-right process diagram
  Notes: ...          -> speaker notes (rest of the slide)
[TO VERIFY] and [PLACEHOLDER] are highlighted so they are not presented by accident.
"""
import math
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

NAVY = RGBColor(0x14, 0x17, 0x6B)
ORANGE = RGBColor(0xE8, 0x63, 0x3A)
INK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x5B, 0x64, 0x72)
CODE_BG = RGBColor(0xF3, 0xF5, 0xF9)
CODE_BORDER = RGBColor(0xD9, 0xDE, 0xE8)
HILITE = RGBColor(0xB4, 0x53, 0x09)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TABLE_ALT = RGBColor(0xF7, 0xF8, 0xFB)

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN = 0.6
CONTENT_TOP = 1.6
CONTENT_BOTTOM = 6.85
BODY_FONT = "Calibri"
CODE_FONT = "Menlo"

INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+\*|\[TO VERIFY\]|\[PLACEHOLDER\])")


# ---------------------------------------------------------------- parsing

def parse(md_text):
    slides, cur = [], None
    mode = None  # None | "code" | "flow" | "notes"
    for raw in md_text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "subtitle": "", "blocks": [], "notes": []}
            slides.append(cur)
            mode = None
            continue
        if cur is None:
            continue
        if mode == "notes":
            if line.strip() and line.strip() != "---":
                cur["notes"].append(line.strip())
            continue
        if mode == "code":
            if line.startswith("```"):
                mode = None
            else:
                cur["blocks"][-1][1].append(line)
            continue
        if mode == "flow":
            if line.strip() == ":::":
                mode = None
            elif line.strip().startswith("- "):
                cur["blocks"][-1][1].append(line.strip()[2:])
            continue
        s = line.strip()
        if not s or s == "---":
            continue
        if s.startswith("```"):
            cur["blocks"].append(("code", []))
            mode = "code"
        elif s.startswith("::: flow"):
            cur["blocks"].append(("flow", []))
            mode = "flow"
        elif s.startswith("Notes:"):
            mode = "notes"
            rest = s[len("Notes:"):].strip()
            if rest:
                cur["notes"].append(rest)
        elif s.startswith("Subtitle:"):
            cur["subtitle"] = s[len("Subtitle:"):].strip()
        elif s.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", s)
            if m:
                cur["blocks"].append(("image", (m.group(1), m.group(2))))
        elif s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if cur["blocks"] and cur["blocks"][-1][0] == "table":
                cur["blocks"][-1][1].append(cells)
            else:
                cur["blocks"].append(("table", [cells]))
        elif s.startswith("- "):
            if cur["blocks"] and cur["blocks"][-1][0] == "bullets":
                cur["blocks"][-1][1].append(s[2:])
            else:
                cur["blocks"].append(("bullets", [s[2:]]))
        else:
            cur["blocks"].append(("text", s))
    return slides


# ---------------------------------------------------------------- text helpers

def add_runs(paragraph, text, size, color, bold=False):
    for part in INLINE.split(text):
        if not part:
            continue
        run = paragraph.add_run()
        run.font.size = Pt(size)
        run.font.name = BODY_FONT
        run.font.color.rgb = color
        run.font.bold = bold
        if part in ("[TO VERIFY]", "[PLACEHOLDER]"):
            run.text = part
            run.font.bold = True
            run.font.color.rgb = HILITE
        elif part.startswith("**") and part.endswith("**"):
            run.text = part[2:-2]
            run.font.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run.text = part[1:-1]
            run.font.name = CODE_FONT
            run.font.size = Pt(size - 2)
            run.font.color.rgb = NAVY
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            run.text = part[1:-1]
            run.font.italic = True
        else:
            run.text = part


def plain_len(text):
    return len(re.sub(r"\*\*|`|\*", "", text))


def text_lines(text, width_in, size_pt):
    chars_per_line = max(10, int(width_in / (size_pt * 0.0072)))
    return max(1, math.ceil(plain_len(text) / chars_per_line))


def frame(shape, wrap=True):
    tf = shape.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    return tf


# ---------------------------------------------------------------- block renderers

def render_bullets(slide, items, x, y, w, size):
    height = sum(text_lines(i, w - 0.35, size) * size * 0.0185 + 0.14 for i in items)
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(height))
    tf = frame(box)
    for n, item in enumerate(items):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        dot = p.add_run()
        dot.text = "●  "
        dot.font.size = Pt(size - 6)
        dot.font.color.rgb = ORANGE
        add_runs(p, item, size, INK)
    return y + height


def render_text(slide, text, x, y, w, size):
    height = text_lines(text, w, size) * size * 0.0185 + 0.1
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(height))
    add_runs(frame(box).paragraphs[0], text, size, MUTED)
    return y + height


def render_code(slide, lines, x, y, w, size):
    height = len(lines) * size * 0.0175 + 0.3
    bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(height))
    bg.adjustments[0] = 0.04
    bg.fill.solid()
    bg.fill.fore_color.rgb = CODE_BG
    bg.line.color.rgb = CODE_BORDER
    bg.shadow.inherit = False
    tf = frame(bg, wrap=False)
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = tf.margin_bottom = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for n, line in enumerate(lines):
        p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        code, _, comment = line.partition("#")
        r = p.add_run()
        r.text = code if code else " "
        r.font.name = CODE_FONT
        r.font.size = Pt(size)
        r.font.color.rgb = INK
        if comment or line.strip().startswith("#"):
            c = p.add_run()
            c.text = "#" + comment
            c.font.name = CODE_FONT
            c.font.size = Pt(size)
            c.font.color.rgb = MUTED
            c.font.italic = True
    return y + height


def render_table(slide, rows, x, y, w):
    n_rows, n_cols = len(rows), len(rows[0])
    row_h = 0.52
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(row_h * n_rows))
    table = shape.table
    table.columns[0].width = Inches(w * 0.48)
    for c in range(1, n_cols):
        table.columns[c].width = Inches(w * 0.52 / (n_cols - 1))
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = ""
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            header = r == 0
            add_runs(p, val, 14 if header else 13, WHITE if header else INK, bold=header)
            if not header and c == 0:
                for run in p.runs:
                    run.font.name = CODE_FONT
                    run.font.size = Pt(12)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if header else (TABLE_ALT if r % 2 == 0 else WHITE)
    return y + row_h * n_rows


def render_flow(slide, steps, x, y, w):
    gap = 0.12
    step_w = (w - gap * (len(steps) - 1)) / len(steps)
    h = 0.95
    for i, step in enumerate(steps):
        shape_type = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        shp = slide.shapes.add_shape(shape_type, Inches(x + i * (step_w + gap)), Inches(y), Inches(step_w), Inches(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = NAVY if i < len(steps) - 1 else ORANGE
        shp.line.fill.background()
        shp.shadow.inherit = False
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.35)
        tf.margin_right = Inches(0.2)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        add_runs(p, step, 15, WHITE, bold=True)
    return y + h + 0.3


def render_image(slide, path, x, y, w):
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w))
    pic.line.color.rgb = CODE_BORDER
    pic.line.width = Pt(0.75)
    return y + Emu(pic.height).inches


# ---------------------------------------------------------------- slides

def add_title(slide, title):
    box = slide.shapes.add_textbox(Inches(MARGIN), Inches(0.42), Inches(SLIDE_W - 2 * MARGIN), Inches(0.8))
    tf = frame(box)
    add_runs(tf.paragraphs[0], title, 30, NAVY, bold=True)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(MARGIN + 0.05), Inches(1.25), Inches(0.7), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()


def add_footer(slide, number):
    box = slide.shapes.add_textbox(Inches(MARGIN), Inches(7.0), Inches(SLIDE_W - 2 * MARGIN), Inches(0.3))
    p = frame(box).paragraphs[0]
    add_runs(p, f"D2E notebook onboarding   ·   {number}", 10, MUTED)


def build_title_slide(prs, s):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), prs.slide_height)
    band.fill.solid()
    band.fill.fore_color.rgb = NAVY
    band.line.fill.background()
    box = slide.shapes.add_textbox(Inches(1.2), Inches(2.4), Inches(10.5), Inches(1.8))
    tf = frame(box)
    add_runs(tf.paragraphs[0], s["title"], 44, NAVY, bold=True)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.25), Inches(4.35), Inches(1.1), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()
    if s["subtitle"]:
        sub = slide.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.5), Inches(0.6))
        add_runs(frame(sub).paragraphs[0], s["subtitle"], 22, MUTED)
    return slide


def build_content_slide(prs, s, number, base_dir):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, s["title"])
    blocks = s["blocks"]
    images = [b for b in blocks if b[0] == "image"]
    others = [b for b in blocks if b[0] != "image"]
    full_w = SLIDE_W - 2 * MARGIN

    if images and others:
        left_w, img_w = 5.15, 6.75
        img_x = SLIDE_W - MARGIN - img_w
        render_image(slide, os.path.join(base_dir, images[0][1][1]), img_x, CONTENT_TOP + 0.05, img_w)
        col_x, col_w = MARGIN, left_w
    elif images:
        img_w = 10.4
        render_image(slide, os.path.join(base_dir, images[0][1][1]), (SLIDE_W - img_w) / 2, CONTENT_TOP, img_w)
        col_x, col_w = MARGIN, full_w
    else:
        col_x, col_w = MARGIN, full_w

    narrow = bool(images)
    y = CONTENT_TOP
    for kind, val in others:
        if kind == "bullets":
            y = render_bullets(slide, val, col_x, y, col_w, 17 if narrow else 19) + 0.1
        elif kind == "text":
            y = render_text(slide, val, col_x, y, col_w, 16) + 0.05
        elif kind == "code":
            longest = max((len(line) for line in val), default=20)
            size = 11 if narrow else (12 if longest > 80 or len(val) > 14 else 14)
            y = render_code(slide, val, col_x, y, col_w, size) + 0.2
        elif kind == "table":
            y = render_table(slide, val, col_x, y, col_w) + 0.2
        elif kind == "flow":
            y = render_flow(slide, val, col_x, y + 0.05, col_w)
    if y > CONTENT_BOTTOM + 0.05:
        print(f"WARNING: slide {number} '{s['title']}' may overflow (content ends at {y:.2f}in)")
    add_footer(slide, number)
    return slide


def main(src, out):
    base_dir = os.path.dirname(os.path.abspath(src))
    slides = parse(open(src, encoding="utf-8").read())
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    for i, s in enumerate(slides, start=1):
        slide = build_title_slide(prs, s) if i == 1 else build_content_slide(prs, s, i, base_dir)
        if s["notes"]:
            slide.notes_slide.notes_text_frame.text = " ".join(s["notes"])
    prs.save(out)
    print(f"saved {out}: {len(slides)} slides")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
