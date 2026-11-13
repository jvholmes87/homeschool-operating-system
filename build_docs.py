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
<meta name="description" content="{blurb}">
<link rel="canonical" href="https://homeschoolhubweekly.com/docs/{slug}.html">
<meta name="author" content="Jason V. Holmes">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1c5f7a">

<meta property="og:site_name" content="Homeschool Hub Weekly">
<meta property="og:type" content="article">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="https://homeschoolhubweekly.com/docs/{slug}.html">
<meta property="og:title" content="{title} &mdash; Homeschool Hub Weekly">
<meta property="og:description" content="{blurb}">
<meta property="og:image" content="https://homeschoolhubweekly.com/assets/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Homeschool Hub Weekly">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} &mdash; Homeschool Hub Weekly">
<meta name="twitter:description" content="{blurb}">
<meta name="twitter:image" content="https://homeschoolhubweekly.com/assets/og-card.png">

<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='13' fill='%231c5f7a'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-size='36' font-weight='bold' fill='%23fdfbf7' text-anchor='middle'%3EH%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="../assets/site.css">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"TechArticle",
 "headline":"{title}",
 "description":"{blurb}",
 "url":"https://homeschoolhubweekly.com/docs/{slug}.html",
 "inLanguage":"en-US",
 "author":{{"@type":"Person","name":"Jason V. Holmes","url":"https://homeschoolhubweekly.com/about.html"}},
 "publisher":{{"@type":"Organization","name":"Homeschool Hub Weekly","url":"https://homeschoolhubweekly.com/"}},
 "isPartOf":{{"@type":"WebSite","name":"Homeschool Hub Weekly","url":"https://homeschoolhubweekly.com/"}},
 "license":"https://opensource.org/licenses/MIT"}}
</script>
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="brand" href="../">Homeschool Hub <span>Weekly</span></a>
    <nav>
      <a href="../tools/coverage-benchmark.html">Hours check</a>
      <a href="../about.html">Who we are</a>
      <a href="../#method">The method</a>
    </nav>
  </div>
</header>

<main class="wrap">
<p class="crumb"><a href="../#method">&larr; All of the method</a></p>
<article class="doc">
{body}
</article>
</main>

<footer>
  <div class="wrap">
    <p>Part of <a href="../">an open operating model for accredited homeschooling</a> &mdash;
    free to copy and adapt, source on
    <a href="https://github.com/jvholmes87/homeschool-operating-system">GitHub</a>.</p>
    <p>The student in this programme is never identified &mdash; see
    <a href="08-privacy-rules.html">the privacy rules</a>.
    No analytics, no cookies, no trackers, no third-party scripts.</p>
  </div>
</footer>

</body>
</html>
"""

# One-line description per page, for search results and link previews.
# Generic boilerplate is what makes a site look abandoned, so each page says
# what is actually on it.
BLURBS = {
    "01-operating-model":
        "How an accredited video curriculum, a fixed ship date and a one-adult "
        "household are run as a single operating model, with the rules written down.",
    "02-packet-architecture":
        "Why the school day is printed as one numbered running order - breaks "
        "included - and how each day's packet is generated rather than assembled.",
    "03-tracker-automation":
        "The conventions behind the Apps Script that maintains the grade and pace "
        "tracker: locate by name, refuse before writing, batch the writes.",
    "04-rendering-constraints":
        "What actually breaks when you generate a child's worksheets as HTML and "
        "print them - handwriting space, page breaks, bilingual type.",
    "05-metrics":
        "Reading speed, pace and coverage are measured every week and never allowed "
        "to touch a grade. Why that separation is deliberate.",
    "06-time-and-coverage":
        "A public-school student's week is 32.1 hours, of which 21.8 are core "
        "instruction. Here is how a homeschool day compares, and the arithmetic.",
    "07-claims-and-limits":
        "What this programme does not claim. The homeschool outcome research is too "
        "weak to support a better-outcomes argument, including the research in its favour.",
    "08-privacy-rules":
        "The rules that keep a ten-year-old out of a public repository, and the "
        "build step that enforces them instead of trusting anyone to remember.",
}

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
    blurb = BLURBS.get(slug)
    if not blurb:
        problems.append(slug + ": no BLURB - page would ship a generic description")
        blurb = title + ". Part of an open operating model for accredited homeschooling."
    blurb = blurb.replace('"', "&quot;")

    out = DOCS / (slug + ".html")
    out.write_text(TEMPLATE.format(title=title, slug=slug, body=body, blurb=blurb))
    built += 1

    if "{{" in body or "{%" in body:
        problems.append(slug + ": template syntax leaked into output")
    if re.search(r"PRIVATE_RULE_REMOVED", body):
        problems.append(slug + ": STUDENT NAME IN OUTPUT")

print("built %d doc pages" % built)
if problems:
    print("PROBLEMS:"); [print("  " + p) for p in problems]; sys.exit(1)
print("no problems found")
