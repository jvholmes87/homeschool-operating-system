# -*- coding: utf-8 -*-
"""
Sample data. Everything here is INVENTED.

No curriculum publisher's content appears in this repository. The student is
fictional, the word list was written for this example, and the lesson numbers
are illustrative. Point this file at your own structure and the generators
follow.
"""

STUDENT = "Robin A. Carter"          # fictional
DAY_NUMBER = 22
DAY_LABEL = "Friday, 13 November 2026"
DATE_SLUG = "13NOV2026"

# --- a word list in the common 20 spelling + 5 vocabulary shape -------------
GROUPS = [
    ("Spelling Rule",
     "When a root word ends in a consonant and <i>y</i>, change the <i>y</i> "
     "to <i>i</i> before adding a suffix unless the suffix begins with <i>i</i>.",
     [(1, "journey"), (2, "bravely"), (3, "kindness"),
      (4, "happiest"), (5, "gardener")]),
    ("Phonics Focus",
     "The long <i>oo</i> sound can also be spelled with a single <i>u</i>.",
     [(6, "prudent"), (7, "solely"), (8, "loyalty"),
      (9, "balloon"), (10, "beauty")]),
    ("Challenge Words", "",
     [(11, "Oregon (OR)"), (12, "Nevada (NV)"), (13, "quietly"),
      (14, "blanket"), (15, "charity"), (16, "patience"),
      (17, "forgettable"), (18, "wonderful"), (19, "moisture"),
      (20, "confident")]),
]

VOCAB = [
    (21, "diligent",   "working hard and carefully"),
    (22, "abundant",   "more than enough"),
    (23, "summit",     "the highest point of something"),
    (24, "resolve",    "to decide firmly to do something"),
    (25, "vivid",      "very bright and clear"),
]

# --- the running order of the day ------------------------------------------
# kind: "work" | "break" | "lunch".  graded items carry star=True.
SCHEDULE = [
    dict(kind="work",  subject="Arithmetic", title="Lesson 21",
         mins=25, note="Watch the video, then the speed drill.", star=False),
    dict(kind="work",  subject="Arithmetic", title="Lesson 22 &middot; <b>Quiz 4</b>",
         mins=30, star=True,
         note="The video gives the directions, then <b>turn the video off</b>. "
              "Desk clear. Show your work."),
    dict(kind="break", mins=15, note="Stand up, move around. No screens."),
    dict(kind="work",  subject="Spelling", title="Lessons 35 and 36",
         mins=45, star=False,
         note="Workbook pages. Classwork, done inside the lesson."),
    dict(kind="break", mins=15, note="Shake your writing hand out."),
    dict(kind="work",  subject="Spelling", title="Lesson 37 &middot; <b>Trial Test</b>",
         mins=25, star=True,
         note="<b>100 means you skip the graded test.</b>"),
    dict(kind="lunch", mins=45, note="Eat properly and get away from the desk."),
    dict(kind="work",  subject="Reading", title="Lessons 37 to 39 &middot; <b>Quiz 2</b>",
         mins=85, star=True,
         note="Your teacher times your reading. When you finish, "
              "<b>close the book &mdash; you cannot open it again.</b> "
              "<b>Your reading speed is not part of your grade.</b>"),
]

MATERIALS = ("Quizzes and drills book &middot; word list book &middot; reader "
             "&middot; notebook paper &middot; scrap paper")

RECITATION = ("60 seconds = 1 minute &middot; 60 minutes = 1 hour &middot; "
              "24 hours = 1 day &middot; 7 days = 1 week &middot; "
              "12 months = 1 year")

# --- bilingual supervisor sheet --------------------------------------------
# (english, korean) pairs. Replace with your own second language, or drop
# the second element to render monolingual.
SUPERVISOR = [
    ("spell", "Before she starts", "시작 전", [
        ("Lay the materials out before she sits down.",
         "아이가 앉기 전에 준비물을 꺼내 두세요."),
        ("<b>Take the test page out of the book</b> and put every study page "
         "out of sight.",
         "<b>시험지를 교재에서 분리하고</b> 공부용 페이지는 모두 보이지 않게 치워 주세요."),
    ]),
    ("read", "Check, do not grade", "확인만, 채점 안 함", [
        ("Workbook pages and the ungraded drill. Mark them with her, record nothing.",
         "워크북 페이지와 채점하지 않는 드릴. 함께 확인하되 점수는 기록하지 마세요."),
    ]),
    ("bible", "Be in the room", "옆에 있어 주세요", [
        ("Every graded item. Desk clear, nothing looked up.",
         "모든 채점 대상 항목. 책상을 치우고, 찾아보지 않게 해 주세요."),
        ("Time the reading and hold up a card each minute.",
         "읽기 시간을 재고 1분마다 숫자 카드를 들어 주세요."),
    ]),
    ("hist", "Record and file", "기록 및 보관", [
        ("Write the number on the paper, then on <b>both</b> report copies.",
         "시험지에 점수를 적고, <b>두 개의</b> 성적표 사본에 모두 기록해 주세요."),
        ("<b>Reading speed is recorded, never graded.</b> A slow time changes nothing.",
         "<b>읽기 속도는 기록만 하고 채점하지 않습니다.</b> 속도가 느려도 점수는 달라지지 않습니다."),
    ]),
]

GRADED_TODAY = [
    ("Arithmetic Quiz 4", "산수 퀴즈 4", "/ 100"),
    ("Spelling Trial Test", "철자 예비 시험", "/ 100"),
    ("Reading Quiz 2", "읽기 퀴즈 2", "/ 100"),
]

HOUSE_RULES = [
    ("Units must be written on every measurement answer.",
     "모든 측정 답에는 단위를 써야 합니다.",
     "<b>Do not deduct for a missing unit on a graded paper.</b>",
     "<b>채점 대상 시험지에서는 단위 누락으로 감점하지 마세요.</b>"),
]
