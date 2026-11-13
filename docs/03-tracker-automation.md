---
layout: default
title: Tracker automation
---

# 03 — Tracker automation (Google Apps Script)

The spreadsheet is the record of account. Scripts maintain it. Every one of them is
written on the assumption that **it will be run against a sheet that has moved since the
script was written**, because it will be.

## Rules

### 1. Named functions

An IIFE gives the Run dropdown nothing to select. Obvious once it has cost you a round
trip with someone who is not at a keyboard with you.

```javascript
function redateSchedule() { ... }   // yes
(function () { ... })();            // the Run menu is empty
```

### 2. Build dates at noon

```javascript
function noon(y, m, d) { return new Date(y, m, d, 12, 0, 0); }
```

Midnight plus a timezone difference silently becomes the previous day. Noon survives every
offset a spreadsheet will apply.

### 3. Locate by name, never by coordinate

Hardcoded `D7` is a time bomb. Someone inserts a column and the script writes authoritative
nonsense into the wrong cell, with no error.

```javascript
function findExact(grid, want) {      // header text, exact match
  want = want.toUpperCase();
  for (var r = 0; r < grid.length; r++)
    for (var c = 0; c < grid[r].length; c++)
      if (String(grid[r][c]).trim().toUpperCase() === want)
        return { r: r + 1, c: c + 1 };
  return null;
}
```

**Exact match, not "contains."** A contains-match for `PLANNED` matched prose elsewhere on
the sheet — *"planned ship Thu 19 Nov 2026"* — several rows above the actual column header.
The projection would have anchored to the wrong column and produced plausible wrong numbers
indefinitely. Caught in test, not in production, and only because the test used the real
sheet's text.

### 4. Refuse before you write

Verify every landmark first. If anything is missing, **throw before the first write** and
put what you actually saw in the message:

```javascript
if (!hit) {
  throw new Error('Could not find "WHERE WE STAND" - nothing was changed.\n' +
                  'Row ' + row + ' reads: ' + grid[row - 1].join(' | '));
}
```

This is the highest-value pattern here. A real run refused because a status band was
assumed at D6:F6 and actually sat at F6:H6. Nothing was corrupted, and the error text
carried the evidence needed to fix it in one iteration.

### 5. Idempotent

Assume it runs twice. Writes should be formulas and values that can be laid down repeatedly
without compounding.

### 6. Ship a read-only diagnostic alongside

```javascript
function whereIsEverything() { /* writes nothing, reports addresses */ }
```

When a guard fires, this answers "so where *is* it?" without another code change.

### 7. Never widen the blast radius

Scripts that add observability write **only** to columns outside the graded range, and the
test asserts it:

```
writes into columns A-H (must be 0): 0
```

A metric script that can reach a grade column will eventually reach one.

## Testing Apps Script without a spreadsheet

Apps Script has no local runner. A ~40-line Node mock of `SpreadsheetApp` — `getRange`,
`getValues`, `setValue`, `setFormula` recording to an array — runs the real `.gs` file via
`eval` and asserts:

- which cells were written, and that no forbidden column was touched
- that every date is at noon
- that the guard throws when the layout is perturbed
- that a second run is clean

Build the mock from the **live sheet's actual text**, not from what you believe the layout
to be. The mock that would have caught the D6/F6 error was the one built from real values.

## The bug class worth naming: silent constant rot

```javascript
WORKDAY(DATE(2026,11,5), drift + 1)    // the original ship date
```

Correct when written. After two re-plans, the headline projection read a date **in the
past** and overstated remaining slack by seven days. No error, no warning — it appeared in
the summary band, which is read most often and questioned least.

Replaced by a reference to the schedule's own final planned date, so re-dating the schedule
moves the projection.

**Derive your anchors. A typed constant is a fact that was true once.**
