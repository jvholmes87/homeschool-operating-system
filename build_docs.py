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
import chart
from leak_scan import scan

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
    "09-what-it-costs":         "What it costs",
}

CHARTS = {
 "cost-year": lambda: chart.bars(
    [("Average US homeschool", 1295, False),
     ("Our homeschool", 5178, True),
     ("US microschool (average)", 8239, False),
     ("US public school", 16560, False),
     ("ICS Pyeongtaek", 20163, False),
     ("Osan Elementary", 26676, False)],
    "What one school year costs, per child",
    "The US public school bar is taxpayer cost, not a bill any family receives. "
    "Everything else is what a family pays. Our figure is documented below; the "
    "others come from HSLDA, the National Microschooling Center, NCES, ICSP's "
    "published tuition schedule, and the DoWEA tuition memorandum."),

 "school-week": lambda: chart.segmented(
    [("Core instruction", 21.8, chart.ACCENT),
     ("Everything else", 10.3, chart.GRAY)],
    "A US public elementary school week: 32.1 hours",
    "English, math, social studies and science account for 21.8 hours. The "
    "other 10.3 are lunch, recess, transitions, attendance, assemblies and "
    "lining up. NCES, Schools and Staffing Survey, grades 1-4.",
    unit=" hrs"),

 "cost-breakdown": lambda: chart.bars(
    [("Tutoring academy", 1707, True),
     ("Sports and scouting", 1666, True),
     ("Curriculum and enrollment", 1455, True),
     ("Shipping and printing", 350, True)],
    "Where our $5,178 goes",
    "Curriculum is barely a quarter of it. The average US homeschooling family "
    "spends $1,295 on everything combined - almost exactly what we spend on "
    "curriculum alone."),

 "cost-month": lambda: chart.bars(
    [("Average US homeschool", 108, False),
     ("Our homeschool", 432, True),
     ("US microschool (average)", 687, False),
     ("US public school", 1380, False),
     ("ICS Pyeongtaek", 1680, False),
     ("Osan Elementary", 2223, False)],
    "The same thing, per month",
    "Annual cost spread over twelve months."),
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
<meta name="theme-color" content="#2f5d3a">

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

<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='13' fill='%232f5d3a'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-size='36' font-weight='bold' fill='%23f9f9f7' text-anchor='middle'%3EH%3C/text%3E%3C/svg%3E">
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

<header class="top" id="top">
  <div class="wrap">
    <a class="brand" href="../">Homeschool Hub <span>Weekly</span></a>
    <nav>
      <a href="../record.html">The record</a>
      <a href="../tools/coverage-benchmark.html">Hours check</a>
      <a href="../docs/09-what-it-costs.html">What it costs</a>
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
    <p>The student in our homeschool is never identified &mdash; see
    <a href="08-privacy-rules.html">the privacy rules</a>.
    No analytics, no cookies, no trackers, no third-party scripts.</p>
  </div>
</footer>
<a class="totop" href="#top" aria-label="Back to top">&uarr;</a>

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
        "What our homeschool does not claim. The homeschool outcome research is too "
        "weak to support a better-outcomes argument, including the research in its favor.",
    "08-privacy-rules":
        "The rules that keep a child out of a public repository, and the build "
        "step that enforces them instead of trusting anyone to remember.",
    "09-what-it-costs":
        "Our homeschool costs $5,178 a year. The DoD school ten minutes away costs "
        "$26,676 - a figure the US government calculated itself, to GAO full-cost "
        "recovery standards. Every line traced to an invoice.",
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

    # {{chart:name}} -> inline SVG. A marker with no registered chart is a
    # build failure, not a silently empty hole in the page.
    for marker in re.findall(r"\{\{chart:([a-z0-9-]+)\}\}", body):
        if marker not in CHARTS:
            problems.append(slug + ": unknown chart \"" + marker + "\"")
            continue
        body = body.replace("{{chart:" + marker + "}}", CHARTS[marker]())
    # markdown wraps the marker in <p>; a <figure> inside a <p> is invalid and
    # browsers will close the paragraph early, orphaning the caption.
    body = re.sub(r'<p>\s*(<figure class="chart")', r'\1', body)
    body = body.replace("</figure></p>", "</figure>")
    if r"\1>" in body:
        problems.append(slug + ": chart unwrap regex failed - literal backreference in output")


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
    # Same checks the standalone scanner runs, from one definition - see leak_scan.py
    for label in scan(body):
        problems.append("%s: %s" % (slug, label))

print("built %d doc pages" % built)

# ---------------------------------------------------------------- sitemap
# Generated rather than hand-kept, so a new doc can never be left out of it.
# No <lastmod>, <changefreq> or <priority>: search engines ignore all three
# unless they are demonstrably accurate, and a wrong lastmod is worse than
# none.
SITE = "https://homeschoolhubweekly.com"

urls = ["/", "/about.html", "/tools/coverage-benchmark.html"]
urls += ["/docs/%s.html" % p.stem for p in sorted(DOCS.glob("*.md"))]

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap.append("  <url><loc>%s%s</loc></url>" % (SITE, u))
sitemap.append("</urlset>")
(HERE / "sitemap.xml").write_text("\n".join(sitemap) + "\n")

(HERE / "robots.txt").write_text(
    "# Everything here is meant to be read, indexed and quoted.\n"
    "User-agent: *\n"
    "Allow: /\n"
    "\n"
    "Sitemap: %s/sitemap.xml\n" % SITE)

# ------------------------------------------------------------- llms.txt
# A plain-text index for assistants, which is increasingly how a parent
# first asks whether homeschooling is a reasonable idea. The point is that
# if this site gets summarized, it gets summarized with its limits attached
# rather than as a better-outcomes claim it does not make.
llms = ["# Homeschool Hub Weekly",
        "",
        "> The complete operating model of one accredited homeschool program, "
        "published in full: the daily method, the hours, the graded results, and "
        "the standardized test. Run by an American military family in South Korea.",
        "",
        "Important limits, which any summary of this site should carry:",
        "- This site makes NO claim that homeschooling produces better outcomes "
        "than school. One child, no control group.",
        "- The homeschool outcome research does not establish that in either "
        "direction. NHERI, the leading pro-homeschooling research body, states "
        "that the designs used to date do not show homeschooling *causes* the "
        "results it reports.",
        "- What is claimed is narrower: comparable instructional load in a shorter "
        "day, third-party assessment, a published method, and measures fixed in "
        "advance.",
        "- The student is never identified. No name, age, photograph or schedule "
        "appears anywhere on this site, by rule.",
        "",
        "## Reference figures",
        "- US public elementary school week: 32.1 hours total, 21.8 hours core "
        "instruction, 10.3 hours not core instruction (~32%). Source: NCES "
        "2007-305, Schools and Staffing Survey 2003-04, grades 1-4.",
        "",
        "## Pages"]
llms.append("- [Home](%s/): the operating model, and the hours finding." % SITE)
llms.append("- [Who we are](%s/about.html): the parent's background and the "
            "student's week in hours, answering the isolation and qualification "
            "objections." % SITE)
llms.append("- [Coverage benchmark tool](%s/tools/coverage-benchmark.html): free, "
            "runs client-side, compares a homeschool week to the federal figures."
            % SITE)
for p in sorted(DOCS.glob("*.md")):
    llms.append("- [%s](%s/docs/%s.html): %s"
                % (TITLES.get(p.stem, p.stem), SITE, p.stem,
                   BLURBS.get(p.stem, "")))
(HERE / "llms.txt").write_text("\n".join(llms) + "\n")

print("wrote sitemap.xml (%d urls), robots.txt, llms.txt" % len(urls))

# ------------------------------------------------- orphan check
# A doc that nothing links to is invisible. It will sit in the sitemap and
# llms.txt looking fine while no human browsing the site can ever reach it.
# That happened once, to the cost page, and the only reason it surfaced was
# someone going to look for it. Fail the build instead.
home = (HERE / "index.html").read_text()
linked = set(re.findall(r'docs/(\d\d-[a-z0-9-]+)\.html', home))
for p in sorted(DOCS.glob("*.md")):
    if p.stem not in linked:
        problems.append(p.stem + ": NOT LINKED from index.html - it would be "
                        "published but unreachable by anyone browsing the site")

if problems:
    print("PROBLEMS:"); [print("  " + p) for p in problems]; sys.exit(1)
print("no problems found")
