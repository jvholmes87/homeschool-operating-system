# 07 — What this case study claims, and what it does not

This repository is written by someone who thinks homeschooling is a good option and wants
more families to have a workable model for it. That is a reason to be *more* careful with
the claims, not less. An advocacy document that overclaims gets dismissed in one sentence,
and takes everything else in the repository with it.

---

## What this does not claim

**It does not claim better academic outcomes than conventional school.** One student, one
programme, no control group, no counterfactual. Nothing here can distinguish the effect of
the method from the effect of the family, and a sample of one cannot support a causal claim
about anything.

**It does not claim the research literature supports homeschooling's superiority**, because
it does not. The most comprehensive review of the field — Kunzman and Gaither's survey —
finds no clear evidence of aggregate achievement gains or losses attributable to
homeschooling, and no evidence of help or harm on socialization. Their reason is not
hostility to the practice; it is that the available studies are too weak to conclude
anything in either direction.

That assessment is not confined to critics. **NHERI — the National Home Education Research
Institute, the field's leading pro-homeschooling research body — states in its own fact
sheet that research designs to date do not conclusively show that homeschooling *causes*
the positive outcomes it reports**, and that one hypothesis is that the findings reflect the
demographics of the families who choose it.

The reason the headline achievement studies get discounted is specific and worth
understanding before citing any of them: the five large studies conducted under HSLDA
sponsorship between 1990 and 2010 relied on samples of homeschoolers **recruited for the
purpose, with volunteers submitting their own test scores.** No random sampling, no controls
for family background. Anyone arguing the other side knows this. Citing those numbers
uncritically is the fastest way to lose a reader who was otherwise persuadable.

## What this does claim

Four things, all of them checkable:

1. **A single parent can run an accredited programme to a documented standard.** The method
   is here. The failure modes are here. Someone else can run it.
2. **Core instructional load is comparable to a public elementary school's, in a shorter
   day.** Measured, not estimated — see `06-time-and-coverage.md`.
3. **The scheduling objection does not describe this programme.** Roughly 7 hours a week of
   structured peer activity plus three classroom sessions a week. That is a claim about a
   calendar, not about social development.
4. **Assessment is third-party.** The accrediting body grades the tests. The parent does not
   mark the work that determines the record.

Point 4 is the one that matters most, and it is the one the literature keeps asking for.

## Why this is worth publishing

Every critique of homeschool research names the same four defects:

| Defect | This programme |
|---|---|
| Self-selected samples | Still true. N=1, and the family chose this. **Unresolved.** |
| Self-reported test scores | **Resolved.** An accrediting body grades and records. |
| Method not transparent | **Resolved.** The whole operating model is published. |
| No controls for family background | Still true. **Unresolved.** |

Two of four, which is two more than most published accounts.

### The externally comparable number

Everything else here is internal: hours we logged, grades the accrediting body assigned
against its own curriculum. None of it can be set beside a public-school cohort.

A **norm-referenced standardized test** can. Abeka supplies the Stanford 10 and the Iowa
Tests, and accredited enrolment includes one free test per enrolment year. Either reports a
percentile against a national sample, which is the only figure in this entire project that
means anything to someone outside it.

**This programme uses Iowa Form E**, and the reason is the comparison group rather than the
test's reputation. Iowa's 2024 norms are built from roughly 4.6 million student records
weighted to federal enrolment data — constructed to represent US students generally.
Stanford 10's 2018 re-norming drew more heavily on private schools, where earlier editions
had used mostly public school scores.

That distinction decides what the published number can be used to say. A percentile means
nothing without knowing who is in the denominator. Against Iowa's sample the claim is "this
student, against American students." Against Stanford's it is "this student, against
private-school students" — a narrower claim, and not the one being tested here.

It will be sat once a year and **the percentile published whichever way it falls.** A
programme that reports its own grades and quietly skips the external test is reporting
nothing. One data point a year is still N=1 and still proves nothing general — but it is
checkable by a stranger, and almost nothing else here is.

Worth noting what it is being measured against: Abeka's own marketing publishes no outcome
statistics at all — the "Why Abeka" page offers that students "have competed in the
Olympics" and a parent testimonial, and names no accrediting body. The publisher does not
fill this gap either. The point of this repository
is not to settle the question. It is to be the kind of account that could be checked.

## Reported in advance

Stated before the results exist, so there is nothing to select afterwards:

| Measure | Source | When |
|---|---|---|
| Grading-period averages, all eight subjects | Accrediting body's report card | Each period |
| Scores shipped vs scores returned | Both report copies | Each period |
| Working hours per school day | Daily pacing log | Continuous |
| Reading rate against comprehension | Timed quizzes | Each timed quiz |
| Schedule slip: planned date vs actual | Tracker | Daily |
| **Iowa Form E** — percentile against a national sample | Riverside, through the accrediting body | Once per enrolment year, each spring |

**Scores are reported whether they are good or not.** A worked example already in this
repository: a timed reading quiz returned 80, ten points below the same student's result a
week earlier at an identical reading rate. The student was tired. That is recorded next to
the number, and the automated flag was rewritten so it stopped asserting a cause the data
did not support — see `05-metrics.md`.

If this repository only ever showed good results, it would be the same artifact as the
studies above, and worth the same.

## For anyone considering this model

The honest summary is that **the research cannot tell you whether homeschooling will produce
a better outcome for your child, and anyone who tells you otherwise is selling something.**
What it can tell you is that there is no established harm, and that family background
appears to matter more than the schooling mode.

So the decision is not "is homeschooling better." It is whether *you* can run an operation
of this size — a compliance programme with hard deadlines, assessment integrity rules and a
signature attesting you followed them — alongside whatever else your life contains.

That is a question about operational capacity, which is answerable. This repository exists
so you can see the actual shape of the job before deciding.

## Sources

- Kunzman, R. & Gaither, M., *Homeschooling: An Updated Comprehensive Survey of the
  Research*, Other Education 9(1), 2020. Summarised in the Harvard Kennedy School PEPG
  conference materials, "Are homeschoolers prepared for life?"
- NHERI, "Research Facts on Homeschooling" and the responses collected at
  https://nheri.org/homeschool-students-academic-achievement-research/ — including NHERI's
  own statement on the limits of causal inference.
- Coalition for Responsible Home Education and the Kunzman/Gaither–NHERI exchange, for the
  state of the dispute. Both sides are worth reading; neither is disinterested.
- NCES Schools and Staffing Survey, for the instructional-hours benchmark in
  `06-time-and-coverage.md`.
