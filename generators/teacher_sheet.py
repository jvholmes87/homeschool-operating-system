# -*- coding: utf-8 -*-
"""
Bilingual supervisor sheet -> A4 PDF.

    python3 teacher_sheet.py [outdir]

Every line appears in both languages. This is the operating document for
whoever runs the school day, not a courtesy translation, so nothing is
summarised in the second language.

Korean needs Noto Sans CJK KR installed, or every glyph renders as tofu:
  /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
"""
import pathlib, sys
from weasyprint import HTML, CSS
import sample_data as D

HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "samples")
OUT.mkdir(parents=True, exist_ok=True)

work = sum(s["mins"] for s in D.SCHEDULE if s["kind"] == "work")
rest = sum(s["mins"] for s in D.SCHEDULE if s["kind"] != "work")


def hm(m):
    return "%d hr %02d min" % (m // 60, m % 60)


def block(cls, en, ko, items):
    rows = "".join('<li>%s<span class="ko">%s</span></li>' % (e, k)
                   for e, k in items)
    return ('<h2 class="%s">%s <span class="t ko">%s</span></h2>'
            '<ul class="task">%s</ul>' % (cls, en, ko, rows))


graded = "".join(
    '<tr><td><b>%s</b><span class="ko">%s</span></td>'
    '<td class="sc"><span class="blank">______</span> %s</td></tr>' % g
    for g in D.GRADED_TODAY)

house = "".join(
    '<li>%s<span class="ko">%s</span><br>%s<span class="ko">%s</span></li>' % h
    for h in D.HOUSE_RULES)

html = """<!doctype html><html><head><meta charset="utf-8">
<title>Day %(day)d supervisor sheet</title></head><body>
<h1>Day %(day)d &mdash; Supervisor Sheet</h1>
<p class="sub">%(name)s &middot; %(label)s
<span class="ko">감독자용 시트</span></p>

<h2 class="hist">Time log <span class="t ko">시간 기록</span></h2>
<table class="g">
<tr><th style="width:34%%">Estimated <span class="ko">예상 시간</span></th>
    <td class="tot">%(work)s work &middot; about %(total)s start to finish</td></tr>
<tr><th>Day started <span class="ko">시작 시각</span></th>
    <td class="blank">________________</td></tr>
<tr><th>Day finished <span class="ko">종료 시각</span></th>
    <td class="blank">________________</td></tr>
</table>

%(sections)s

<h2 class="exam">Graded today <span class="t ko">오늘 채점</span></h2>
<table class="g">
<tr><th>Item <span class="ko">항목</span></th>
    <th class="sc">Score <span class="ko">점수</span></th></tr>
%(graded)s
</table>

<div class="banner warn">
<b>HOUSE RULES &mdash; not the publisher&rsquo;s.</b> These shape practice. They must never
move a graded score.
<span class="ko"><b>가정 규칙 &mdash; 출판사 규칙이 아닙니다.</b> 연습에만 적용되며,
채점 점수를 바꾸어서는 안 됩니다.</span>
<ul class="task" style="margin:2mm 0 0">%(house)s</ul>
</div>

<table class="g">
<tr><th style="width:50%%">Videos all watched <span class="ko">영상 전부 시청</span></th>
    <th>Graded work unassisted <span class="ko">도움 없이 수행</span></th></tr>
<tr><td class="blank" style="height:14mm">______</td><td class="blank">______</td></tr>
</table>

<div class="banner warn" style="margin-top:4mm">
<b>If something goes wrong, stop and call the marker.</b> Do not guess at a grade, do not
allow a re-do, and do not allow anything to be looked up during a test.
<span class="ko"><b>문제가 생기면 멈추고 채점자에게 연락해 주세요.</b> 점수를 임의로
추정하지 마시고, 다시 풀게 하지 마시고, 시험 중에 무엇이든 찾아보지 않게 해 주세요.</span>
</div>
</body></html>""" % dict(
    day=D.DAY_NUMBER, name=D.STUDENT, label=D.DAY_LABEL,
    work=hm(work), total=hm(work + rest),
    sections="".join(block(*s) for s in D.SUPERVISOR),
    graded=graded, house=house)

dest = OUT / ("sample-supervisor-day%d-%s.pdf" % (D.DAY_NUMBER, D.DATE_SLUG))
HTML(string=html).write_pdf(dest, stylesheets=[CSS(filename=str(HERE / "style.css"))])
print("wrote %s" % dest)
