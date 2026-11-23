/** @OnlyCurrentDoc */
/**
 * redate.gs - re-baseline a schedule after it slips.
 *
 * Two jobs, and the second is the one people forget:
 *   1. Set future days to the new plan.
 *   2. Set PAST days' planned date to the date the work was actually done.
 *
 * Without (2) a tracker reports drift that is already history. Most of a
 * "three school days behind" figure turned out to be a stale planning column,
 * not real slippage - and a false alarm erodes trust in every real one.
 *
 * Run: redateSchedule()
 */
function redateSchedule() {
  var ss = SpreadsheetApp.getActive();

  // month is 0-based. Dates are built at NOON: midnight plus a timezone
  // offset silently becomes the previous day.
  var PLAN = {
    15: [2026, 10,  2], 16: [2026, 10,  3], 17: [2026, 10,  5],
    18: [2026, 10,  9], 19: [2026, 10, 10], 20: [2026, 10, 11],
    21: [2026, 10, 12], 22: [2026, 10, 13], 23: [2026, 10, 16],
    24: [2026, 10, 17], 25: [2026, 10, 18], 26: [2026, 10, 19]
  };

  var DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  var MONS = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec'];

  function noon(a) { return new Date(a[0], a[1], a[2], 12, 0, 0); }
  function pretty(d) {
    var dd = d.getDate() < 10 ? '0' + d.getDate() : '' + d.getDate();
    return DAYS[d.getDay()] + ' · ' + dd + ' ' + MONS[d.getMonth()] +
           ' ' + d.getFullYear();
  }

  var ov = ss.getSheetByName('Overview');
  if (!ov) { throw new Error('Overview tab not found - nothing was changed.'); }

  var dates = 0, titles = 0;
  for (var d in PLAN) {
    var when = noon(PLAN[d]);
    var sh = ss.getSheetByName('Day ' + (d < 10 ? '0' + d : d));
    if (!sh) { continue; }

    sh.getRange('A6').setValue(when);
    dates++;

    // Re-date the tab's own title line too, or it keeps showing a date that
    // contradicts the cell underneath it.
    var cur  = String(sh.getRange('A1').getValue() || '');
    var head = cur.split(' - ')[0] || ('Day ' + d);
    sh.getRange('A1').setValue(head + ' - ' + pretty(when));
    titles++;

    ov.getRange(10 + Number(d), 2).setValue(when);
  }

  SpreadsheetApp.getUi().alert(
    'Re-date complete\n\nDates: ' + dates + '\nTitles: ' + titles);
}
