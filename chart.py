"""
Inline-SVG charts for the site.

No library, no CDN, no JavaScript - same constraint as everything else here:
the page must work saved to disk with the network off.

Form choice follows the data's job. The cost comparison is an EMPHASIS chart:
one bar is the point, the rest are context. One accent hue plus a de-emphasis
gray, never a rainbow of categories.

Palette (2026-11 redesign) against the site surface #f9f9f7:
  accent #24552f 8.2:1, context gray #73716a 4.6:1; white bar labels on
  either mark >= 4.5:1. Accent and gray differ in lightness, not hue alone,
  so the emphasis bar survives greyscale and colorblindness.
"""

ACCENT = "#24552f"   # the bar that is the point
GRAY   = "#73716a"   # context bars
INK    = "#1a1a1a"
MUTED  = "#5f5f58"
LINE   = "#d9d7cf"

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
    # clean axis top: pick a round step size that puts 3-6 gridlines on the
    # plot, so the axis ends near the longest bar instead of far past it.
    mag = 10 ** (len(str(int(vmax))) - 1)
    step = mag
    for cand in (mag / 4, mag / 2, mag, mag * 2, mag * 2.5, mag * 5, mag * 10):
        if 3 <= vmax / cand <= 6:
            step = cand
            break
    ticks = int(-(-vmax // step))          # ceil
    top = step * ticks
    n = len(rows)
    head_h, foot_h = 8, 34
    height = head_h + n * (bar_h + gap) + foot_h

    def x(v): return label_w + (v / top) * plot_w

    out = []
    out.append(
        f'<figure class="chart">'
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'role="img" aria-label="{esc(caption)}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="\'Source Sans 3\',-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">'
    )
    # gridlines - hairline, solid, recessive, behind the marks
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


def segmented(parts, caption, note="", width=720, bar_h=28, unit=""):
    """
    One whole split into parts. Tall segmented bar: 28px and never more, each
    part its own block with 4px corners, a 2px surface gap doing the
    separating, its share printed inside at the leading edge. No baseline, so
    no end is square. The legend names the parts in block order.

    parts: list of (label, value, color)
    """
    total = sum(v for _, v, _ in parts)
    gap = 2
    legend_h = 30
    height = bar_h + legend_h + 14
    inner = width - gap * (len(parts) - 1)

    out = [f'<figure class="chart">'
           f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
           f'role="img" aria-label="{esc(caption)}" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="\'Source Sans 3\',-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">']
    x = 0.0
    for label, value, color in parts:
        w = inner * value / total
        share = 100.0 * value / total
        out.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{bar_h}" rx="4" '
                   f'fill="{color}"><title>{esc(label)}: {value}{unit} ({share:.0f}%)</title></rect>')
        txt = f'{value}{unit}'
        # only print inside when it genuinely fits with padding on both sides
        if w > len(txt) * 8.2 + 20:
            out.append(f'<text x="{x + 11:.1f}" y="{bar_h*0.69:.1f}" fill="#ffffff" '
                       f'font-size="13.5" font-weight="700">{txt}</text>')
        x += w + gap

    # legend, block order, naming what the blocks are
    lx = 0.0
    for label, value, color in parts:
        out.append(f'<rect x="{lx:.1f}" y="{bar_h + 17}" width="10" height="10" rx="2" fill="{color}"/>')
        out.append(f'<text x="{lx + 16:.1f}" y="{bar_h + 26}" fill="{INK}" font-size="13">'
                   f'{esc(label)}</text>')
        lx += 16 + len(label) * 7.1 + 28
    out.append('</svg>')
    out.append(f'<figcaption>{esc(caption)}'
               + (f' <span class="cnote">{esc(note)}</span>' if note else '')
               + '</figcaption></figure>')
    return "\n".join(out)
