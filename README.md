# Homeschool Operating System

**A systems-engineering approach to running an accredited homeschool program as a compliance operation.**

Built and operated for **Abeka Academy Grade 4 Accredited Video**, 2026–27. This
repository documents the operating model, the document-generation pipeline and the
spreadsheet automation — the method, not the coursework.

The curriculum is named because that is a fact about this programme and because other
Abeka families should be able to find this. **None of Abeka's content is reproduced
here** — no word lists, quiz items, answer keys, grading tables or lesson text. Those are
Pensacola Christian College's and are deliberately absent. Naming a curriculum you use and
reproducing it are different things.

> **This case study does not claim better academic outcomes than conventional school.**
> One student, no control group, no counterfactual. The research literature does not
> support that claim either — including, explicitly, the field's leading pro-homeschooling
> research body. What is claimed, and why the narrower claim is the stronger one, is set
> out in [`docs/07-claims-and-limits.md`](docs/07-claims-and-limits.md).

> **No curriculum content is in this repository.** Word lists, quiz items, answer keys,
> grading tables and lesson text belong to the curriculum publisher and are not reproduced
> here. Every example uses an invented student and an invented word list. Student records
> live in a separate private repository.

---

## The problem

An accredited homeschool is not a teaching problem. It is a **compliance operation that
happens to involve teaching.**

The program has hard requirements, and the consequences of missing them are not academic:

| Requirement | Failure mode |
|---|---|
| Every video lesson watched | Credit withheld |
| Grading periods shipped by fixed dates | Grades do not post |
| Tests opened, proctored and stored by the home teacher only | Accreditation integrity |
| No retakes, ever | A bad score is permanent |
| Home teacher signs a verification statement each period | The signature is the audit |
| Minimum programme length | Finishing early banks nothing |

One parent is simultaneously **teacher, proctor, registrar and QA**, usually while holding
a job. The default tooling is a paper planner and memory, and it fails in a specific way:
the work gets done but the *evidence* and *sequencing* drift, and nobody notices until a
grading period is due.

This system exists to make the drift visible early and the paperwork automatic.

---

## The operating model

### Three roles, not one

The single most consequential design decision is that **the person supervising the school
day and the person marking the work are different people**, and in this household they do
not share a first language.

That one fact drives the whole document architecture:

- The **supervisor** needs instructions, not judgment. She never assigns a grade.
- The **marker** needs the evidence, in order, with the rules attached.
- The **student** needs a single sheet she can work straight down.

Anything that must be *heard* to be graded — oral reading, recitation — is either done with
the marker present or recorded and sent to him. A supervisor never guesses at a grade.

### The week, not just the school day

The programme is not the whole of the student's week, and a model that ignores the rest of
it is not describing anything real. Reported as **hours by category** — never as days,
times, named organisations or locations, because this is a public document about a child:

| | Hours per week |
|---|---|
| Core instruction, 5 days | 19.6 – 26.7 |
| Academic tutoring (mathematics, second language), 3×/week | 9 – 12 |
| Scouting, one meeting | 1.5 – 2 |
| Sports club | 1.5 – 2 |
| Youth sports, 2 practices + 1 game, seasonal | 3 – 4.5 |

Core instruction is **logged daily**. Enrichment hours are **estimates** until logged the
same way — labelled as such wherever they appear.

Against a US public elementary benchmark of **32.1 hours in school per week, of which 21.8
is core instruction.** Core load is comparable; the recovered time is the third of the
public week that is not instruction. Full working in
[`docs/06-time-and-coverage.md`](docs/06-time-and-coverage.md).

### Three documents a day

| Document | Audience | Language | Why separate |
|---|---|---|---|
| Student packet | The student | English | She works down it unaided; no answer keys, ever |
| Supervisor sheet | Whoever runs the day | **Bilingual** | Operating document, not a courtesy translation |
| Standing rules card | Supervisor | Bilingual | Printed **once**, laminated — nothing on it changes |

Pulling the unchanging rules onto a laminated card is what keeps the daily sheet at two
pages instead of four. The daily sheet then carries only what is true *today*.

### The rule that protects the accreditation

House rules and curriculum rules are **printed differently and never mixed.**

The household has its own standards — units written on every measurement answer, for
instance. Those shape practice. They are printed in a red-ruled box and explicitly labelled
as house rules, with the instruction **not to deduct for them on a graded paper.**

Only the publisher's own deduction table may move a recorded score. A supervisor who
applies a house rule to an accredited grade has corrupted the record, and the error is
invisible afterwards. This separation is the single most important line in the system.

---

## What is in here

```
docs/
  01-operating-model.md       roles, document split, the house-rule boundary
  02-packet-architecture.md   what a daily packet contains and why
  03-tracker-automation.md    Apps Script patterns, and the bugs that taught them
  04-rendering-constraints.md WeasyPrint behaviour discovered the hard way
  05-metrics.md               tracked-but-not-graded measures, and honest flags
  06-time-and-coverage.md     measured hours against a public elementary benchmark
  07-claims-and-limits.md     what this claims, what it does not, and what gets reported
  08-privacy-rules.md         binding rules - the student is never identified
tools/
  coverage-benchmark.html     "are we doing enough hours?" - self-contained, sends nothing
generators/
  style.css                   shared stylesheet: page, type, subject colour system
  packet.py                   student packet -> A4 PDF
  teacher_sheet.py            bilingual supervisor sheet -> A4 PDF
  sample_data.py              INVENTED student and word list
apps-script/
  redate.gs                   calendar re-baseline
  reading_speed.gs            a tracked-not-graded metric, end to end
  guards.gs                   locate-by-name helpers; refuse-before-write
samples/
  rendered output from sample_data.py
```

Stack: **Python + WeasyPrint** for documents, **Google Sheets + Apps Script** for the
record, **Noto Sans CJK KR** for the Korean half of the supervisor sheets.

---

## Engineering lessons

The parts worth reading even if you never run an accredited homeschool.

### 1. A guard that refuses to write is worth more than a script that succeeds

Every script here locates its targets **by name** — header text, row labels — and aborts
without writing anything if it cannot find them. This is not defensive padding. It caught
a real failure: a script assumed a status band sat in columns D–F. It sat in F–H. The guard
refused, named what it actually saw, and nothing was corrupted. The fix took one iteration
because the error message carried the evidence.

The pattern is in `apps-script/guards.gs`: find by name, verify, then write.

### 2. Exported spreadsheets lie in two different ways

Reading a Google Sheet by exporting it to ODS is convenient and wrong twice over:

- **Formula cells carry cached values.** A computed cell may report what it said at some
  earlier point, not what it says now.
- **Empty cells collapse.** Column positions inferred from the export can be shifted from
  the live sheet, silently.

Both bit this project. Treat an export as a source of *raw typed values only*, and read
anything computed — or any column position you intend to write to — from the live sheet.

### 3. Hardcoded date anchors rot quietly

A projection read:

```
WORKDAY(DATE(2026,11,5), drift + 1)
```

`2026-11-05` was the original planned ship date. After two re-plans it was simply wrong, and
the status band had been reporting a projected ship date **in the past** — displayed in the
headline summary, where it was read most often and questioned least. It also overstated the
remaining slack by seven days.

Nothing errored. A wrong constant produces a confident wrong answer forever.

The fix: the projection now reads the final day's planned date out of the schedule itself,
so re-dating the schedule moves the projection. **Derive anchors, never type them.**

### 4. An indicator must not assert a cause it cannot support

A reading-speed tracker flagged `Too fast — comprehension slipping` whenever speed was high
and the score low. It looked reasonable. Then two data points arrived:

| | Rate | Score |
|---|---|---|
| Reading 1 | 175 wpm | 90 |
| Reading 2 | 177 wpm | 80 |

Speed moved 2 wpm. The score moved 10 points. **Speed was not the variable** — the student
was tired for the second one. The flag would have aimed every future reader of that sheet
at the wrong explanation, permanently and with confidence.

It now reads `Check — fast pace, 2 missed`: same trigger, no causal claim, and a **Note
column beside it** for the condition. A number without its context becomes a misleading
number the moment everyone forgets. In three months nobody remembers she was tired; all
that survives is an 80 that looks like a reading problem.

### 5. Measure the thing you refuse to grade

Reading speed is recorded on every timed quiz and is **never allowed to touch a score.** It
lives in columns deliberately outside the graded range so no average can pick it up, and the
student's own sheet tells her so in plain words — otherwise she races the clock and trades
away the comprehension that *is* graded.

Observability and assessment are different jobs. Mixing them corrupts both.

### 6. Rendering: the constraints are not where you expect

Full detail in `docs/04-rendering-constraints.md`. The short version for WeasyPrint:

- Flexbox overflows unpredictably — use `inline-block` or `display:table`
- `table-layout:fixed` needs widths on **`th` as well as `td`**, or the column collapses
- `break-inside:avoid` moves a whole block rather than splitting it, leaving holes
- Two adjacent empty cells render as one continuous rule — add a spacer column
- **Always rasterize and look at the output.** Page-fill measured in pixels catches the
  near-empty final page that a successful build will not.

### 7. Size the artifact to the human

An upper-elementary student with large handwriting cannot fit *"to focus thoughts and efforts on one
thing"* on a 40 mm blank. The build succeeded; the sheet was unusable. Writing space is now
specified against observed handwriting — 10.5 mm ruled lines, three per definition, one word
per block — not against what fits the page.

The same applies to the day itself: breaks are **printed as numbered items in the running
order**, because a child who cannot see a break coming experiences the day as
unbroken work. And the day is quoted at both working time and start-to-finish time, since
the second is the honest number.

---

## Outcomes

**Operational** outcomes over the first grading period. These are facts about running the
programme, not evidence that the model produces better learning — see
[`docs/07-claims-and-limits.md`](docs/07-claims-and-limits.md).

- A grading period that had slipped roughly two weeks was re-baselined and brought back
  inside its due date with buffer to spare, without adding school days beyond one weekend
  make-up day.
- A reconciliation of watched-lesson state against recorded grades surfaced three lessons
  marked complete by grade but never actually viewed — the one inconsistency visible to the
  accrediting body from their side, and invisible from a paper planner.
- A recurring arithmetic error was identified as a single cross-subject gap rather than
  three unrelated mistakes, drilled once, and cleared on the next assessment.
- Reported schedule drift fell to zero once the planned dates were corrected to the dates
  work was actually done — most of the "behind plan" figure was an artifact of a stale
  planning column, not real slippage.

Academic results are third-party graded by the accrediting body and reported each grading
period **whether or not they are good**. The measures were fixed in advance, so there is
nothing to select afterwards; the list is in `07-claims-and-limits.md`.

---

## For other homeschooling families

**[tools/coverage-benchmark.html](tools/coverage-benchmark.html)** answers the question most
often asked and least often answered: *are we doing enough hours?* Enter your week, see it
against the federal grades 1-4 figures, and find the subject that quietly stopped happening.

It runs entirely in the browser. No analytics, no form posts, no storage, no third-party
scripts - the only external link in the file is back to this repository. A parent checking
whether they are doing enough should not have to trust anyone with the answer.

It measures coverage, not learning. More hours is not better; it is just more hours.

## Reuse

The generators and Apps Script patterns are curriculum-agnostic. `sample_data.py` is the
only file that knows what a lesson contains; point it at your own structure and the pipeline
follows.

What you will have to supply yourself: your curriculum's grading rules, its deduction table,
and its calendar. Those are the publisher's, and deliberately absent here.

## License

Code and documentation: MIT, see `LICENSE`.
No curriculum publisher's content is included or licensed by this repository.
