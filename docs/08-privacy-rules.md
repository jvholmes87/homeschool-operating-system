# 08 — Privacy rules for this repository

Binding on every file here and on anything published from it. The student in our homeschool
is a minor. These rules are not editorial preference.

## The student is never identified

- **No name.** Not full, not first, not initials. She is "the student".
- **No age or date of birth.** "Upper elementary" is the limit — not the year, not the
  birthday, not "she turns ten this month".
- **No photographs**, of her or of her work in her handwriting.
- **No school-issued identifiers** — account numbers, student IDs, enrollment numbers.

Her grades and hours are published. Her identity is not. The practical effect is that her
record never surfaces in a search for her name, which is the part that follows her into
adulthood.

**This is thin cover, and it is meant to be.** The repository author is named, and anyone
who knows him can work out who the student is. The rule is not anonymity against someone
who already knows her; it is that nothing here is indexed against her name.

## Schedules are never publishable. Region is.

What locates a child is not a place on its own. It is a **place plus a time plus a way to
recognize her**. Any two of those three are inert; all three together are the safety
problem, however ordinary the activity.

So the rule is drawn around the combination, not around the word "location":

| Never publish | Publish instead |
|---|---|
| Days, times, or recurring schedule of any activity | hours per week |
| Named organizations, troop or unit numbers | the category: "scouting", "a Korean sports club" |
| Addresses, specific facilities, the academy or club she attends | the region, and the category of place |
| Her name or photograph alongside *any* of the above | neither, ever |

**Region is published deliberately** — the country, and the installation whose community
this family is part of. That was a considered change, not a slip. The program's entire
shape is a consequence of being an overseas military family: the ship-by-mail deadlines,
the time-zone gap with the school, the *hagwon* in the middle of a school week, the base
scouting and youth-sports infrastructure doing the socialisation work. Strip the region out
and the case study stops being useful to the families most likely to need it, who are
disproportionately military and overseas.

What that costs is accepted honestly: it narrows the pool. What it does not do is produce a
findable child, because the schedule and the name — the other two legs — are absent and stay
absent.

"Scouting, one meeting per week, 1.5–2 hrs, on base" makes exactly the same argument as
naming the troop and the night, and tells a stranger nothing actionable.

### Date of birth

Her **date of birth is never published**, which is a change worth stating explicitly
because birthdays are the detail families leak most casually — a cake photo, a "she turns
ten today" post. DOB plus region plus a surname is enough to start matching records. It
lives in the private operating files only, where it is needed to set the school calendar.

## Curriculum content

No publisher's content is reproduced here: no word lists, quiz items, answer keys, grading
tables or lesson text. Naming a curriculum you use is factual and fine. Reproducing it is
not. The two are easy to confuse under deadline — when in doubt, describe the structure and
omit the content.

## Tools published from this repository

Anything interactive — the coverage benchmark, any calculator — **collects nothing and
sends nothing.** No analytics, no form posts, no third-party scripts, no storage. A family
checking whether they do enough hours should not have to trust anyone with the answer.

If that ever changes, it needs a written data policy first, and it must not be bundled
quietly into a release.

## Before any commit

1. Does any file carry her name, date of birth, photograph or a school identifier?
2. Does any file put a child at a place **on a given day or at a given time**?
3. Does any file name the troop, academy or club?
4. Is any publisher content reproduced rather than described?
5. Does any new interactive page call out to the network?

The leak scan covers (1) and (4) mechanically — the docs build exits non-zero if her name
appears in generated output, so a slip fails the publish rather than shipping. (2), (3) and
(5) need a human.
