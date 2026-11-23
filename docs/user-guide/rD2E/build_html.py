"""Build a single shareable HTML page from the rD2E Markdown guide.

Usage:
    pip install markdown
    python build_html.py                  # writes rD2E-user-guide.html next to this script

The Markdown files are the source of truth. This script stitches them into one page
with a sidebar, turns links between pages into in-page anchors, shows the "Checked"
column as chips, and highlights [TO VERIFY] and [PLACEHOLDER].
The output is page content for a claude.ai artifact (no <html>/<head>/<body> tags).
"""
import html
import os
import re

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "rD2E-user-guide.html")

# (file, anchor id, sidebar label, sidebar group)
PAGES = [
    ("README.md", "overview", "Overview", "Start"),
    ("getting-started.md", "getting-started", "Getting started", "Start"),
    ("reference/get_cohort_definition_set.md", "get-cohort-definition-set", "get_cohort_definition_set()", "Reference"),
    ("reference/create_cohort_definition.md", "create-cohort-definition", "create_cohort_definition()", "Reference"),
    ("reference/create_options.md", "create-options", "create_options()", "Reference"),
    ("reference/run_strategus_flow.md", "run-strategus-flow", "run_strategus_flow()", "Reference"),
    ("guides/working-with-cohorts.md", "working-with-cohorts", "Working with cohorts", "Guides"),
    ("guides/submitting-a-study.md", "submitting-a-study", "Submitting a study", "Guides"),
    ("guides/troubleshooting.md", "troubleshooting", "Troubleshooting", "Guides"),
]
ANCHOR_BY_STEM = {os.path.splitext(os.path.basename(f))[0]: a for f, a, _, _ in PAGES}
ANCHOR_BY_STEM["README"] = "overview"

CSS = """
/* Layout: sticky sidebar of pages on the left, one reading column on the right; stacks on phones. */
:root {
  --bg: #fbfbfd; --surface: #ffffff; --fg: #1b1f2e; --muted: #5a6074; --line: #e3e5ee;
  --accent: #23268f; --accent-soft: #eceefb; --code-bg: #f3f4f9;
  --ok: #1f6f43; --ok-bg: #e4f3ea; --src: #4a5170; --src-bg: #eceef4;
  --flag: #8a4b06; --flag-bg: #fdf0d9;
  --font-body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #12131c; --surface: #191b26; --fg: #e6e8f2; --muted: #a0a6bd; --line: #2b2e3e;
  --accent: #a9adff; --accent-soft: #23264a; --code-bg: #1f2130;
  --ok: #7fd3a1; --ok-bg: #173225; --src: #b6bcd6; --src-bg: #262a3b;
  --flag: #f5c27a; --flag-bg: #3a2a12; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #12131c; --surface: #191b26; --fg: #e6e8f2; --muted: #a0a6bd; --line: #2b2e3e;
  --accent: #a9adff; --accent-soft: #23264a; --code-bg: #1f2130;
  --ok: #7fd3a1; --ok-bg: #173225; --src: #b6bcd6; --src-bg: #262a3b;
  --flag: #f5c27a; --flag-bg: #3a2a12; color-scheme: dark }

body { background: var(--bg); color: var(--fg); font: 16px/1.6 var(--font-body); }
.shell { display: grid; grid-template-columns: 17rem minmax(0, 1fr); gap: 3rem; max-width: 76rem; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 2.5rem 4rem; }
nav.toc { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 1.5rem); align-self: start; max-height: calc(100vh - 3rem); overflow-y: auto; }
.brand { font-weight: 600; font-size: 1.15rem; color: var(--fg); margin: 0 0 .25rem; }
.brand code { font-family: var(--font-mono); color: var(--accent); background: none; padding: 0; font-size: 1em; }
.tagline { color: var(--muted); font-size: .85rem; margin: 0 0 1.5rem; }
.toc h2 { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 1.25rem 0 .4rem; }
.toc ul { list-style: none; margin: 0; padding: 0; display: grid; gap: .1rem; }
.toc a { display: block; padding: .3rem .6rem; border-radius: 6px; color: var(--fg); text-decoration: none; font-size: .92rem; }
.toc a.fn { font-family: var(--font-mono); font-size: .84rem; }
.toc a:hover, .toc a:focus-visible { background: var(--accent-soft); color: var(--accent); outline: none; }
main { min-width: 0; max-width: 46rem; }
section.page { padding-bottom: 2.5rem; margin-bottom: 2.5rem; border-bottom: 1px solid var(--line); scroll-margin-top: 1.5rem; }
section.page:last-child { border-bottom: 0; }
.kicker { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 .3rem; }
h1, h2, h3, h4 { text-wrap: balance; line-height: 1.25; }
section.page > h2 { font-size: 1.9rem; margin: 0 0 1rem; font-weight: 600; }
section.page h2 code { font-size: .92em; color: var(--accent); background: none; padding: 0; }
h3 { font-size: 1.2rem; margin: 2rem 0 .6rem; font-weight: 600; }
h4 { font-size: 1rem; margin: 1.5rem 0 .5rem; }
p, li { max-width: 65ch; }
a { color: var(--accent); }
code { font-family: var(--font-mono); font-size: .88em; background: var(--code-bg); padding: .1em .35em; border-radius: 4px; }
pre { background: var(--code-bg); border: 1px solid var(--line); border-radius: 8px; padding: .9rem 1rem; overflow-x: auto; line-height: 1.5; }
pre code { background: none; padding: 0; font-size: .85rem; }
.table-wrap { overflow-x: auto; margin: 1rem 0; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: .92rem; }
th, td { text-align: left; vertical-align: top; padding: .55rem .8rem; border-bottom: 1px solid var(--line); }
th { font-weight: 600; color: var(--muted); font-size: .78rem; letter-spacing: .04em; text-transform: uppercase; background: var(--bg); }
tr:last-child td { border-bottom: 0; }
td code { white-space: nowrap; }
td:first-child code { white-space: normal; }
.chip { display: inline-block; font-size: .72rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; padding: .15rem .5rem; border-radius: 999px; white-space: nowrap; }
.chip-host { color: var(--ok); background: var(--ok-bg); }
.chip-source { color: var(--src); background: var(--src-bg); }
mark.flag { color: var(--flag); background: var(--flag-bg); font-weight: 600; font-size: .85em; padding: .05em .4em; border-radius: 4px; white-space: nowrap; }
blockquote { margin: 1rem 0; padding: .8rem 1rem; border-left: 3px solid var(--flag); background: var(--flag-bg); border-radius: 0 8px 8px 0; }
blockquote p { margin: 0; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2rem 0 1rem; }
hr + p { color: var(--muted); font-size: .85rem; }
.legend { display: flex; flex-wrap: wrap; gap: .5rem 1rem; align-items: center; color: var(--muted); font-size: .85rem; margin: 1rem 0 0; }
@media (max-width: 860px) {
  .shell { grid-template-columns: minmax(0, 1fr); gap: 1.5rem; padding-block: 1.5rem 3rem; }
  nav.toc { position: static; max-height: none; border-bottom: 1px solid var(--line); padding-bottom: 1rem; }
  .toc ul { grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr)); }
  section.page > h2 { font-size: 1.6rem; }
}
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
"""


def rewrite_links(md_text):
    def repl(m):
        target = m.group(2)
        if target.startswith(("http://", "https://", "#")):
            return m.group(0)
        stem = os.path.splitext(os.path.basename(target.split("#")[0]))[0]
        anchor = ANCHOR_BY_STEM.get(stem)
        return f"[{m.group(1)}](#{anchor})" if anchor else m.group(0)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md_text)


def to_html(md_text):
    body = markdown.markdown(rewrite_links(md_text), extensions=["tables", "fenced_code"])
    # One level down: the page title becomes h2, its sections h3, and so on.
    for level in (4, 3, 2, 1):
        body = re.sub(rf"<(/?)h{level}>", rf"<\1h{level + 1}>", body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = re.sub(r"<td>host</td>", '<td><span class="chip chip-host">host</span></td>', body)
    body = re.sub(r"<td>source</td>", '<td><span class="chip chip-source">source</span></td>', body)
    body = re.sub(r"\[(TO VERIFY|PLACEHOLDER)\]", r'<mark class="flag">\1</mark>', body)
    body = body.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')
    return body


def main():
    sections, groups = [], {}
    for path, anchor, label, group in PAGES:
        with open(os.path.join(HERE, path), encoding="utf-8") as f:
            md_text = f.read()
        kicker = {"Reference": "Function reference", "Guides": "Guide"}.get(group, "")
        kicker_html = f'<p class="kicker">{kicker}</p>' if kicker else ""
        sections.append(f'<section class="page" id="{anchor}">{kicker_html}{to_html(md_text)}</section>')
        cls = ' class="fn"' if group == "Reference" else ""
        groups.setdefault(group, []).append(f'<li><a{cls} href="#{anchor}">{html.escape(label)}</a></li>')

    nav = "".join(f"<h2>{g}</h2><ul>{''.join(items)}</ul>" for g, items in groups.items())
    page = f"""<title>rD2E User Guide</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="shell">
  <nav class="toc" aria-label="Contents">
    <p class="brand"><code>rD2E</code> user guide</p>
    <p class="tagline">Cohorts and Strategus runs from the D2E notebook</p>
    {nav}
    <div class="legend"><span class="chip chip-host">host</span> checked on the test host
      <span class="chip chip-source">source</span> from the code
      <mark class="flag">TO VERIFY</mark> not yet confirmed</div>
  </nav>
  <main>
    {''.join(sections)}
  </main>
</div>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {OUT} ({len(page)} bytes, {len(PAGES)} pages)")


if __name__ == "__main__":
    main()
