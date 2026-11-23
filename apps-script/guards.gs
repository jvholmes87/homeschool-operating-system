/** @OnlyCurrentDoc */
/**
 * guards.gs - locate by name, verify, then write.
 *
 * The premise: this script WILL be run against a sheet that has moved since
 * it was written. Hardcoded A1 references are time bombs - someone inserts a
 * column and the script writes authoritative nonsense into the wrong cell
 * with no error at all.
 *
 * Every mutating function in this repository locates its targets by name and
 * throws BEFORE the first write if anything is missing.
 */

/** A1 notation from 1-based row/column. */
function a1(r, c) {
  var s = '';
  while (c > 0) { var m = (c - 1) % 26; s = String.fromCharCode(65 + m) + s;
                  c = (c - m - 1) / 26; }
  return s + r;
}

/**
 * First cell whose text CONTAINS `want`. Convenient, and dangerous for
 * anything that also appears in prose - see findExact.
 */
function findContains(grid, want) {
  want = want.toUpperCase();
  for (var r = 0; r < grid.length; r++)
    for (var c = 0; c < grid[r].length; c++)
      if (String(grid[r][c]).toUpperCase().indexOf(want) !== -1)
        return { r: r + 1, c: c + 1 };
  return null;
}

/**
 * First cell whose trimmed text EQUALS `want`.
 *
 * Use this for column headers. A contains-match for "PLANNED" once matched a
 * sentence several rows higher - "planned ship Thu 19 Nov 2026" - and would
 * have anchored a projection to the wrong column, producing plausible wrong
 * numbers indefinitely. Exact match for headers, always.
 */
function findExact(grid, want) {
  want = want.toUpperCase();
  for (var r = 0; r < grid.length; r++)
    for (var c = 0; c < grid[r].length; c++)
      if (String(grid[r][c]).trim().toUpperCase() === want)
        return { r: r + 1, c: c + 1 };
  return null;
}

/** Column index of `want` within one 0-based row, or 0. */
function findInRow(grid, rowIdx, want) {
  want = want.toUpperCase();
  for (var c = 0; c < grid[rowIdx].length; c++)
    if (String(grid[rowIdx][c]).toUpperCase().indexOf(want) !== -1)
      return c + 1;
  return 0;
}

/**
 * Throw with evidence. The message carries what was ACTUALLY seen, so the
 * failure can be fixed in one iteration instead of a guessing round trip.
 */
function refuse(what, grid, rowIdx) {
  var saw = (grid && rowIdx != null && grid[rowIdx])
            ? '\nRow ' + (rowIdx + 1) + ' reads: ' + grid[rowIdx].join(' | ')
            : '';
  throw new Error('Could not find ' + what + ' - nothing was changed.' + saw);
}

/**
 * Read-only. Ship one of these with every script. When a guard fires, this
 * answers "so where IS it?" without another code change.
 */
function whereIsEverything() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getActiveSheet();
  var g  = sh.getRange(1, 1, Math.min(sh.getLastRow(), 40),
                       Math.min(sh.getLastColumn(), 20)).getValues();
  var out = [];
  ['Subject', 'Planned', 'Actually done'].forEach(function (want) {
    var hit = findExact(g, want);
    out.push(want + ' -> ' + (hit ? a1(hit.r, hit.c) : 'NOT FOUND'));
  });
  SpreadsheetApp.getUi().alert('Layout scan - nothing was changed\n\n' +
                               out.join('\n'));
}
