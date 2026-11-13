#!/usr/bin/env python3
"""
Generate docs/*.html from docs/*.md.

The site is plain static files: no Jekyll, no theme, no build step on
GitHub's side that can fail. A .nojekyll file at the root tells GitHub Pages
to serve what is committed and nothing else.

Run after editing any doc:    python3 build_docs.py
"""
import pathlib, re, sys
import markdown

HERE = pathlib.Path(__file__).parent
DOCS = HERE / "docs"

TITLES = {
    "01-operating-model":       "Operating model",
    "02-packet-architecture":   "Daily packet architecture",
    "03-tracker-automation":    "Tracker automation",
    "04-rendering-constraints": "Rendering constraints",
    "05-metrics":               "Metrics that are tracked but never graded",
    "06-time-and-coverage":     "Time and coverage",
    "07-claims-and-limits":     "Claims and limits",
    "08-privacy-rules":         "Privacy rules",
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; Homeschool Hub Weekly</title>
<meta name="description" content="{title}. Part of an open operating model for accredited homeschooling.">
<link rel="canonical" href="https://homeschoolhubweekly.com/docs/{slug}.html">
<style>
  :root {{ --ink:#1d2228; --muted:#5d6672; --line:#d8dde3; --bg:#fbfcfd; --accent:#1c4f8f; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:0 18px 72px; background:var(--bg); color:var(--ink);
         font:16.5px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  main {{ max-width:760px; margin:0 auto; }}
  nav {{ padding:22px 0 0; font-size:14.5px; }}
  nav a {{ color:var(--muted); text-decoration:none; }}
  nav a:hover {{ color:var(--accent); text-decoration:underline; }}
  h1 {{ font-size:31px; line-height:1.18; margin:18px 0 18px; letter-spacing:-0.3px; }}
  h2 {{ font-size:21px; margin:38px 0 10px; padding-bottom:6px; border-bottom:2px solid var(--line); }}
  h3 {{ font-size:17.5px; margin:26px 0 6px; }}
  a {{ color:var(--accent); }}
  table {{ width:100%; border-collapse:collapse; margin:14px 0; }}
  th,td {{ text-align:left; padding:8px 9px; border-bottom:1px solid var(--line); font-size:15.5px;
          vertical-align:top; }}
  th {{ color:var(--muted); font-weight:600; }}
  code {{ background:#eef1f4; padding:1.5px 5px; border-radius:4px; font-size:14.5px; }}
  pre {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:14px 16px;
        overflow-x:auto; }}
  pre code {{ background:none; padding:0; font-size:14px; line-height:1.5; }}
  blockquote {{ margin:16px 0; padding:12px 18px; border-left:4px solid var(--accent);
               background:#fff; border-radius:0 8px 8px 0; color:var(--muted); }}
  blockquote p {{ margin:0 0 8px; }} blockquote p:last-child {{ margin:0; }}
  ul,ol {{ padding-left:22px; }} li {{ margin-bottom:7px; }}
  hr {{ border:0; border-top:1px solid var(--line); margin:34px 0; }}
  footer {{ margin-top:52px; padding-top:18px; border-top:1px solid var(--line);
           font-size:14px; color:var(--muted); }}
</style>
</head>
<body>
<main>
<nav><a href="../">&larr; Homeschool Hub Weekly</a></nav>
{body}
<footer>
<p>Part of <a href="../">an open operating model for accredited homeschooling</a> &mdash;
source on <a href="https://github.com/jvholmes87/homeschool-operating-system">GitHub</a>.
The student in this programme is never identified; see
<a href="08-privacy-rules.html">the privacy rules</a>.</p>
<p>No analytics, no cookies, no trackers.</p>
</footer>
</main>
</body>
</html>
"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])

built, problems = 0, []
for src in sorted(DOCS.glob("*.md")):
    slug = src.stem
    text = src.read_text()

    # strip any leftover YAML front matter - we are not using Jekyll
    text = re.sub(r"\A---\n.*?\n---\n+", "", text, flags=re.S)

    # cross-links between docs point at the generated html
    text = re.sub(r"\]\((\d\d-[a-z0-9-]+)\.md\)", r"](\1.html)", text)

    md.reset()
    body = md.convert(text)

    # Cross-references written as inline code - `07-claims-and-limits.md` -
    # read as dead filenames on the website. Turn them into real links to the
    # generated page, titled, so a reader can follow them.
    def linkify(m):
        ref = m.group(1)
        label = TITLES.get(ref, ref.replace("-", " "))
        return '<a href="%s.html">%s</a>' % (ref, label)
    body = re.sub(r"<code>(?:docs/)?(\d\d-[a-z0-9-]+)\.md</code>", linkify, body)

    title = TITLES.get(slug, slug.replace("-", " "))

    out = DOCS / (slug + ".html")
    out.write_text(TEMPLATE.format(title=title, slug=slug, body=body))
    built += 1

    if "{{" in body or "{%" in body:
        problems.append(slug + ": template syntax leaked into output")
    if re.search(r"(?i)\bjamie\b", body):
        problems.append(slug + ": STUDENT NAME IN OUTPUT")

print("built %d doc pages" % built)
if problems:
    print("PROBLEMS:"); [print("  " + p) for p in problems]; sys.exit(1)
print("no problems found")
