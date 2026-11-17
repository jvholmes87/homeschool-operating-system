"""
Inline-SVG charts for the site.

No library, no CDN, no JavaScript - same constraint as everything else here:
the page must work saved to disk with the network off.

Form choice follows the data's job. The cost comparison is an EMPHASIS chart:
one bar is the point, the rest are context. One accent hue plus a de-emphasis
gray, never a rainbow of categories.

Palette validated against the site surface #fdfbf7:
  CVD separation dE 14.4 (protan) / 17.7 (tritan), normal-vision dE 18.2,
  both marks >= 3:1 contrast. The chroma-floor check does not apply - the gray
  is meant to read as gray.
"""

ACCENT = "#1c5f7a"   # the bar that is the point
GRAY   = "#8a8378"   # context bars
INK    = "#23201c"
MUTED  = "#6b665e"
LINE   = "#e4ddd2"

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def bars(rows, caption, note="", unit="$", width=720, bar_h=22, gap=16,
         label_w=250, value_w=74):
    """
    rows: list of (label, value, emphasis: bool)
    Ranked in the order given. Bars <=24px, 4px rounded data-end, square at the
    baseline, hairline recessive gridlines, values direct-labelled, all text in
    text tokens rather than the series color.
    """
    plot_w = width - label_w - value_w
    vmax = max(v for _, v, _ in rows)
    # clean axis top
    step = 10 ** (len(str(int(vmax))) - 1)
    top = ((int(vmax) // step) + 1) * step
    n = len(rows)
    head_h, foot_h = 8, 34
    height = head_h + n * (bar_h + gap) + foot_h

    def x(v): return label_w + (v / top) * plot_w

    out = []
    out.append(
        f'<figure class="chart">'
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'role="img" aria-label="{esc(caption)}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">'
    )
    # gridlines - hairline, solid, recessive, behind the marks
    ticks = 4
    for i in range(ticks + 1):
        v = top * i / ticks
        gx = x(v)
        out.append(f'<line x1="{gx:.1f}" y1="{head_h}" x2="{gx:.1f}" '
                   f'y2="{head_h + n*(bar_h+gap) - gap + 6}" stroke="{LINE}" stroke-width="1"/>')
        lbl = f'{unit}{int(v):,}' if v else '0'
        out.append(f'<text x="{gx:.1f}" y="{height - 14}" fill="{MUTED}" font-size="11.5" '
                   f'text-anchor="middle">{lbl}</text>')

    for i, (label, value, emph) in enumerate(rows):
        y = head_h + i * (bar_h + gap)
        w = max(2.0, (value / top) * plot_w)
        color = ACCENT if emph else GRAY
        r = 4
        # square at the baseline, 4px rounded at the data end
        d = (f'M{label_w},{y} H{label_w + w - r} a{r},{r} 0 0 1 {r},{r} '
             f'V{y + bar_h - r} a{r},{r} 0 0 1 -{r},{r} H{label_w} Z')
        out.append(f'<path d="{d}" fill="{color}"><title>{esc(label)}: {unit}{value:,}</title></path>')
        weight = "700" if emph else "400"
        out.append(f'<text x="{label_w - 12}" y="{y + bar_h*0.72:.1f}" fill="{INK}" '
                   f'font-size="13" font-weight="{weight}" text-anchor="end">{esc(label)}</text>')
        out.append(f'<text x="{label_w + w + 9:.1f}" y="{y + bar_h*0.72:.1f}" fill="{INK}" '
                   f'font-size="13" font-weight="{weight}">{unit}{value:,}</text>')
    out.append('</svg>')
    out.append(f'<figcaption>{esc(caption)}'
               + (f' <span class="cnote">{esc(note)}</span>' if note else '')
               + '</figcaption></figure>')
    return "\n".join(out)
