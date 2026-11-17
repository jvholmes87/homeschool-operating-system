#!/usr/bin/env python3
"""
Generate the three-year grade chart as inline SVG, from the data.

Source: Abeka Academy report cards, Grades 1-3, final subject grades only.
Nothing here is self-reported - every number was marked by the accrediting body.

Small multiples rather than one slope chart with eight lines: at Grade 3 four
subjects land on 89-90 and their labels would collide into mush. One panel per
subject on a SHARED y-scale keeps the comparison honest and lets a subject that
only exists in later years simply have a shorter line.

Colour carries trend direction, and never alone - every panel states its change
in text, so the chart survives greyscale, colorblindness and forced-colors.

    python3 make_record_chart.py        writes _chart.svg fragment to stdout
"""

# (subject, [Grade 1, Grade 2, Grade 3]); None = subject not taught that year
SUBJECTS = [
    ("Bible",          [87, 95, 98]),
    ("Spelling",       [None, 96, 97]),
    ("Arithmetic",     [96, 99, 96]),
    ("Reading",        [86, 90, 90]),
    ("Language",       [96, 95, 90]),
    ("History",        [None, None, 90]),
    ("Science/Health", [None, None, 89]),
    ("Writing",        [83, 80, 79]),
]

INK, MUTED, LINE = "#23201c", "#5f5a52", "#e4ddd2"
# Chart marks use a more saturated teal than the site's link color: the link
# teal measures 0.078 chroma, under the 0.10 floor, and reads grey as a mark.
# Both of these pass the palette validator against this page's surface.
RISE, FALL = "#0b6f96", "#c2410c"

YMIN, YMAX = 75, 100          # shared scale; floor sits below every data point
COLS = 4
PW, PH = 168, 128             # panel box
PX, PY = 34, 30               # plot origin inside the panel
PLW, PLH = 112, 56            # plot area


def y(v):
    return PY + PLH - (v - YMIN) / (YMAX - YMIN) * PLH


def x(i):
    return PX + i * (PLW / 2)


def panel(name, vals, ox, oy):
    pts = [(x(i), y(v), v, i) for i, v in enumerate(vals) if v is not None]
    first, last = pts[0], pts[-1]
    delta = last[2] - first[2]
    falling = delta < 0
    col = FALL if falling else RISE

    # Kept short deliberately. "no change" and "first year" spelled out collided
    # with the longer subject names at this panel width - caught by rendering it.
    if len(pts) == 1:
        label = ""                                   # a lone dot needs no trend
    elif delta > 0:
        label = "↑ +%d" % delta
    elif delta < 0:
        label = "↓ −%d" % abs(delta)       # true minus sign, not a hyphen
    else:
        label = "→ ±0"

    o = ['<g transform="translate(%g,%g)">' % (ox, oy)]
    o.append('<text x="0" y="12" class="pname">%s</text>' % name)
    if label:
        # trend stated in text, so color is never the only cue
        o.append('<text x="%g" y="12" class="ptrend %s" text-anchor="end">%s</text>'
                 % (PX + PLW, "fall" if falling else "rise", label))

    # recessive gridlines at the band edges and the A-/B- boundaries
    for gv, lab in ((100, "100"), (90, "90"), (80, "80")):
        o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" class="grid"/>'
                 % (PX, y(gv), PX + PLW, y(gv)))
        o.append('<text x="%g" y="%g" class="ytick">%s</text>'
                 % (PX - 6, y(gv) + 3.5, lab))

    if len(pts) > 1:
        d = " ".join("%s%g %g" % ("M" if n == 0 else "L", p[0], p[1])
                     for n, p in enumerate(pts))
        o.append('<path d="%s" class="ln" stroke="%s"/>' % (d, col))

    for cx, cy, v, i in pts:
        o.append('<circle cx="%g" cy="%g" r="4.5" fill="%s" class="pt">'
                 '<title>%s, Grade %d: %d</title></circle>' % (cx, cy, col, name, i + 1, v))

    # label first and last only - a number on every point is noise
    for cx, cy, v, i in ({first, last} if len(pts) > 1 else {first}):
        anchor = "start" if i == 0 and len(pts) > 1 else ("end" if i == 2 else "middle")
        dx = 8 if anchor == "start" else (-8 if anchor == "end" else 0)
        o.append('<text x="%g" y="%g" class="val" text-anchor="%s">%d</text>'
                 % (cx + dx, cy - 9, anchor, v))

    for i, lab in enumerate(("G1", "G2", "G3")):
        o.append('<text x="%g" y="%g" class="xtick">%s</text>'
                 % (x(i), PY + PLH + 17, lab))
    o.append("</g>")
    return "\n".join(o)


def chart_svg():
    rows = (len(SUBJECTS) + COLS - 1) // COLS
    W, H = COLS * PW, rows * PH
    out = ['<svg viewBox="0 0 %d %d" class="gchart" role="img" '
           'aria-labelledby="gct gcd" xmlns="http://www.w3.org/2000/svg">' % (W, H)]
    out.append('<title id="gct">Final grades by subject, Grades 1 to 3</title>')
    out.append('<desc id="gcd">Eight small line charts on a shared 75-100 scale, one '
               'per subject. Seven subjects sit at or above 89 by Grade 3. Writing '
               'declines from 83 to 79 and is the lowest. Language declines from 96 '
               'to 90. Full figures are in the table below.</desc>')
    for n, (name, vals) in enumerate(SUBJECTS):
        out.append(panel(name, vals, (n % COLS) * PW, (n // COLS) * PH))
    out.append("</svg>")
    return "\n".join(out)


def letter(v):
    """Abeka's 10-point scale, from docs - the same table the program grades on."""
    for lo, lab in ((98, "A+"), (93, "A"), (90, "A-"), (87, "B+"), (83, "B"),
                    (80, "B-"), (77, "C+"), (73, "C"), (70, "C-"), (67, "D+"),
                    (60, "D")):
        if v >= lo:
            return lab
    return "F"


def table_html():
    """The table view. Generated from the same list as the chart, so the two
    cannot drift apart - a figure corrected in one place is corrected in both."""
    o = ['<table class="grades">',
         '<thead><tr><th>Subject</th><th class="n">Grade 1</th>'
         '<th class="n">Grade 2</th><th class="n">Grade 3</th>'
         '<th class="n">Change</th></tr></thead><tbody>']
    for name, vals in SUBJECTS:
        cells = []
        for v in vals:
            cells.append('<td class="n">&mdash;</td>' if v is None
                         else '<td class="n">%d <span class="lt">%s</span></td>'
                              % (v, letter(v)))
        seen = [v for v in vals if v is not None]
        d = seen[-1] - seen[0]
        if len(seen) == 1:
            chg = '<td class="n note">first year</td>'
        elif d == 0:
            chg = '<td class="n note">no change</td>'
        else:
            chg = '<td class="n %s">%+d</td>' % ("fall" if d < 0 else "rise", d)
        o.append("<tr><th>%s</th>%s%s</tr>" % (name, "".join(cells), chg))
    o.append("</tbody></table>")
    return "\n".join(o)


def main():
    import pathlib
    here = pathlib.Path(__file__).parent
    tpl = (here / "record.template.html").read_text()
    page = tpl.replace("<!--CHART-->", chart_svg()).replace("<!--TABLE-->", table_html())
    (here / "record.html").write_text(page)
    print("wrote record.html (%d subjects, %d bytes)" % (len(SUBJECTS), len(page)))


if __name__ == "__main__":
    main()
