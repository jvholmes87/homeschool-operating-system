# -*- coding: utf-8 -*-
"""
Student packet -> A4 PDF.

    python3 packet.py [outdir]

Reads everything from sample_data.py. Layout code below never changes;
updating a school day is editing data, not markup.
"""
import pathlib, sys
from weasyprint import HTML, CSS
import sample_data as D

HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "samples")
OUT.mkdir(parents=True, exist_ok=True)

ALL_WORDS = [w for _, _, ws in D.GROUPS for _, w in ws] + [w for _, w, _ in D.VOCAB]
assert len(ALL_WORDS) == 25, "expected 20 spelling + 5 vocabulary"
assert not [w for w in ALL_WORDS if "?" in w], "unverified word on a study sheet"

SUBJ_CLASS = {"Arithmetic": "math", "Spelling": "spell", "Reading": "read",
              "Bible": "bible", "Writing": "write", "History": "hist"}


def shape_rows():
    out = ""
    for s in D.SCHEDULE:
        if s["kind"] == "work":
            out += ('<tr><td>%s &middot; %s</td><td class="m">%d min</td></tr>'
                    % (s["subject"], s["title"], s["mins"]))
        else:
            label = "LUNCH" if s["kind"] == "lunch" else "BREAK"
            out += ('<tr class="b"><td>%s</td><td class="m">%d min</td></tr>'
                    % (label, s["mins"]))
    return out


def blocks():
    out, seen = "", None
    for s in D.SCHEDULE:
        if s["kind"] != "work":
            label = "Lunch" if s["kind"] == "lunch" else "Break"
            out += ('<div class="brk"><div><div class="ttl">%s</div>'
                    '<div class="small">%s</div></div>'
                    '<div class="mins">%d min</div></div>'
                    % (label, s["note"], s["mins"]))
            continue
        if s["subject"] != seen:
            seen = s["subject"]
            out += ('<h2 class="%s">%s</h2>'
                    % (SUBJ_CLASS.get(seen, "hist"), seen))
        star = '<span class="star">&#9733;</span> ' if s["star"] else ""
        out += ('<ul class="task"><li>%s<b>%s</b><br>'
                '<span class="note">%d min. %s</span></li></ul>'
                % (star, s["title"], s["mins"], s["note"]))
    return out


def study_pages():
    rows = ""
    for title, rule, words in D.GROUPS:
        rules = ' &mdash; <span>%s</span>' % rule if rule else ""
        rows += '<p class="grp">%s%s</p><table class="sl">' % (title, rules)
        for n, w in words:
            rows += '<tr><td class="n">%d.</td><td class="w">%s</td><td></td></tr>' % (n, w)
        rows += "</table>"
    voc = "".join('<li><b>%d. %s</b> &mdash; %s</li>' % v for v in D.VOCAB)

    # Vocabulary gets its own page with room sized to real handwriting.
    vb = ""
    for n, w, d in D.VOCAB:
        vb += ('<div class="vblock">'
               '<p class="vhead"><b>%d. %s</b> &nbsp;<span class="note">&mdash; %s</span></p>'
               '<p class="vlab">Write the word twice</p>'
               '<div class="wline"><div></div><div class="sp"></div><div></div></div>'
               '<p class="vlab">Write what it means, in your own words</p>'
               '<div class="dline"></div><div class="dline"></div>'
               '<div class="dline"></div></div>' % (n, w, d))

    return """
<div class="studypage">
<h1>Word List</h1>
<p class="sub">%s &middot; Day %d &middot; study page &mdash; remove before any test</p>
<div class="banner warn"><b>Study page.</b> Read the rule at the top of each group before
its words. Hand this page to your teacher before any test.</div>
%s
<p class="grp">Vocabulary Words</p>
<ul class="task" style="list-style:none">%s</ul>
</div>

<div class="studypage">
<h1>Vocabulary</h1>
<p class="sub">%s &middot; Day %d &middot; words 21&ndash;25</p>
<div class="banner warn"><b>These five are different.</b> On the test you write the word
<i>and</i> what it means. Put the meaning in your own words &mdash; it does not have to
match mine word for word.</div>
%s
</div>""" % (D.STUDENT, D.DAY_NUMBER, rows, voc, D.STUDENT, D.DAY_NUMBER, vb)


work = sum(s["mins"] for s in D.SCHEDULE if s["kind"] == "work")
rest = sum(s["mins"] for s in D.SCHEDULE if s["kind"] != "work")
graded = sum(1 for s in D.SCHEDULE if s.get("star"))


def hm(m):
    return "%d hr %02d min" % (m // 60, m % 60)


html = """<!doctype html><html><head><meta charset="utf-8">
<title>%(name)s - Day %(day)d</title></head><body>
<h1>Day %(day)d</h1>
<p class="sub">%(label)s</p>

<div class="name"><div>
  <div class="nm">%(name)s</div>
  <div class="small">Sign your name in cursive:
    <span class="blank">______________________________</span></div>
 </div>
 <div style="text-align:right"><div><b>Day %(day)d</b></div>
  <div class="small">%(graded)d graded today</div></div>
</div>

<div class="box"><h3>Say it out loud &mdash; three times, then tick</h3>
<p style="margin:0 0 1.5mm">%(recite)s</p>
<ul class="task" style="margin:0"><li>First time</li><li>Second time</li>
<li>Third time, without looking</li></ul></div>

<div class="box"><h3>Books and things you need today</h3>
<p style="margin:0">%(mats)s</p></div>

<div class="box"><h3>Today&rsquo;s shape &mdash; this is where your breaks are</h3>
<table class="shape">%(shape)s</table>
<p class="small" style="margin:2mm 0 0"><b>Your breaks are yours.</b> You do not have to
earn them and you do not lose them for working slowly. If you need one sooner, say so.</p>
</div>

%(blocks)s

<div class="box"><h3>How long today should take</h3>
<table class="log">
<tr><th style="width:55%%">Work time</th><td class="tot">%(work)s</td></tr>
<tr><th>Breaks and lunch</th><td class="tot">%(rest)s</td></tr>
<tr><th>Start to finish</th><td class="tot">about %(total)s</td></tr>
</table></div>

<div class="box"><h3>Pacing log &mdash; write the time as you go</h3>
<table class="log">
<tr><th>Started the day</th><td class="blank">__________</td>
    <th>Finished the day</th><td class="blank">__________</td></tr>
</table></div>

%(study)s
</body></html>""" % dict(
    name=D.STUDENT, day=D.DAY_NUMBER, label=D.DAY_LABEL, graded=graded,
    recite=D.RECITATION, mats=D.MATERIALS, shape=shape_rows(), blocks=blocks(),
    work=hm(work), rest=hm(rest), total=hm(work + rest), study=study_pages())

dest = OUT / ("sample-packet-day%d-%s.pdf" % (D.DAY_NUMBER, D.DATE_SLUG))
HTML(string=html).write_pdf(dest, stylesheets=[CSS(filename=str(HERE / "style.css"))])
print("wrote %s  (work %s, start to finish %s)" % (dest, hm(work), hm(work + rest)))
