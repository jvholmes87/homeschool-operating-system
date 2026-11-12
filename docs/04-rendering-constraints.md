# 04 — Rendering constraints (WeasyPrint → A4 PDF)

Discovered by building several hundred pages. Not in the obvious documentation.

## Layout

**Flexbox overflows unpredictably.** Use `display: inline-block`, or `display: table` with
`table-cell` children, for anything that must sit in a row.

**Multi-column blocks need `display: table`.** Inline-block percentages wrap and collapse
into a single column at unpredictable widths.

**`table-layout: fixed` requires widths on `th` as well as `td`.** A selector of `td.qn`
leaves the header cell unconstrained and the whole column collapses. Use a bare class
selector so it reaches both:

```css
.qn { width: 9mm; }          /* reaches th.qn and td.qn */
td.qn { width: 9mm; }        /* header is unconstrained - column collapses */
```

**`break-inside: avoid` moves the whole block.** A large unbreakable element jumps to the
next page and leaves a hole. For a big block that must stay intact, push it to a page of
its own deliberately:

```css
@media print { .key { break-before: always; } }
```

**Two adjacent empty cells render as one continuous rule.** The student sees one long line
where two writing spaces were intended. Insert a spacer column with no border.

## Typography

**Korean needs an explicit CJK font**, or every glyph renders as tofu:

```css
.ko { font-family: "Noto Sans CJK KR", sans-serif; }
```

`/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc`, index 1.

**Symbols fall back badly.** A star renders as tofu in Liberation Sans. Draw it from a font
you have verified, or use an SVG.

## Verification

**Always rasterize and look at the output.**

```bash
pdftoppm -r 62 -png -f 5 -l 6 packet.pdf page
```

A successful build is not a correct document. Two failures only visible by eye:

- A near-empty final page, where one orphaned item flowed past a break
- Writing lines technically present but too small for the actual handwriting

Measure page fill by pixel density per page to catch the first automatically. The second
needs a human, or a known handwriting size written into the spec.

## Generator hygiene

**Assert on unverified content.** Any value transcribed from a source that has not been
confirmed carries a marker, and the generator refuses to build:

```python
assert not [w for w in WORDS if "?" in w], "unverified word on a study sheet"
```

**Assert the arithmetic.** If a sheet totals to 100 points, make the generator prove it:

```python
N = sum(len(items) for _, _, items in SECTIONS)
assert N == 20 and 100 % N == 0
PTS = 100 // N
```

A scoring sheet that does not sum correctly is worse than no sheet, because it will be
trusted.

**Separate data from layout.** Content lives in plain lists at the top of each generator;
the rendering code below never changes. Updating a day is editing data, not markup.
