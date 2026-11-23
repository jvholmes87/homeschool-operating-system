# 05 — Metrics that are tracked but never graded

## The principle

Some measures are worth watching and must never affect a score. Reading rate is the
canonical example: it diagnoses, it does not assess.

Mixing them corrupts both. A student who knows speed is graded reads faster and
comprehends less — trading away the thing that *is* graded for the thing that is merely
measured.

## Implementation

1. **Physical separation in the sheet.** The metric lives in columns outside the graded
   range. No average can reach it even by accident.
2. **Stated on the student's own sheet**, in plain words: *your reading speed is not part
   of your grade, we just keep track of it.*
3. **Stated on the supervisor sheet**, so nobody helpfully deducts for a slow time.
4. Two typed inputs only — word count and elapsed time. Everything else is a formula.
   Arithmetic done by hand is arithmetic done wrong eventually.

## Banding

Bands are anchored to the **publisher's own printed benchmarks**, not invented:

| Band | Source |
|---|---|
| Floor | the baseline printed on the student's own progress graph |
| Target | the rate the teacher's notes allow for the grade level |
| Ceiling | the top of that graph's scale |

If you cannot point at where a threshold came from, you have invented a standard and
attached authority to it.

## Flags must not claim causation

A flag combining two signals — high rate, low score — is useful. The wording is where it
goes wrong.

`Too fast — comprehension slipping` asserts a cause. The first two real data points
destroyed it: 175 wpm scored 90, 177 wpm scored 80. Rate moved 2; score moved 10. The
student was tired, which the numbers cannot show.

The flag now reads `Check — fast pace, N missed`. Same trigger, no claim, and a **Note
column** beside it for the condition.

**A metric without its context becomes misleading the moment everyone forgets.** Budget a
free-text column next to every automated indicator. It is the cheapest thing in the system
and the first thing omitted.

## Trend before level

A single reading is noise. The sheet shows the change since the previous one, because the
expectation is improvement over a year, not a number on a day.
