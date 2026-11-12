/** @OnlyCurrentDoc */
/**
 * reading_speed.gs - a metric that is TRACKED and NEVER GRADED.
 *
 * Reading rate diagnoses; it does not assess. A student who knows speed is
 * graded reads faster and comprehends less - trading away the thing that IS
 * graded for the thing that is merely measured.
 *
 * So the metric lives in columns OUTSIDE the graded range, deliberately, and
 * the test for this script asserts it writes nothing into the grade columns.
 *
 * Two typed inputs, everything else a formula:
 *   I  Words      <- typed
 *   J  Time (min) <- typed
 *   K  wpm         = Words / Time
 *   L  Pace        = band
 *   M  vs. last    = change since the previous reading
 *   N  Note        <- typed; the condition a bare number cannot carry
 *
 * Run: setUpReadingSpeed()
 */
function setUpReadingSpeed() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName('Grades');
  if (!sh) { throw new Error('Grades tab not found - nothing was changed.'); }

  // Find the rows by NAME, so new ones work without editing this file.
  var labels = sh.getRange(1, 2, sh.getLastRow(), 1).getValues();
  var rows = [];
  for (var i = 0; i < labels.length; i++)
    if (/^Timed Quiz\b/i.test(String(labels[i][0]).trim())) rows.push(i + 1);
  if (!rows.length) {
    throw new Error('No "Timed Quiz" rows found - nothing was changed.');
  }

  var hdr = rows[0] - 1;
  sh.getRange(hdr, 9, 1, 6).setValues(
    [['Words', 'Time (min)', 'wpm', 'Pace', 'vs. last', 'Note']]);
  sh.getRange(hdr, 9, 1, 6).setFontWeight('bold').setBackground('#f2f2f2');

  var prev = null;
  rows.forEach(function (r) {
    sh.getRange(r, 11).setFormula(
      '=IFERROR(IF(OR($I' + r + '="",$J' + r + '=""),"",' +
      'ROUND($I' + r + '/$J' + r + ')),"")');

    // Bands anchor to the publisher's OWN printed benchmarks - the floor on
    // the student's progress graph, the rate the teacher's notes allow, the
    // top of that graph's scale. A threshold you cannot source is a standard
    // you invented and attached authority to.
    //
    // NOTE THE WORDING. An earlier version read "Too fast - comprehension
    // slipping". Two data points killed that claim: 175 wpm scored 90,
    // 177 wpm scored 80. Rate moved 2, score moved 10 - the student was
    // tired, which no formula can see. A flag must not assert a cause it
    // cannot support, so it now reports the facts and leaves why to column N.
    sh.getRange(r, 12).setFormula(
      '=IF($K' + r + '="","",' +
      'IF(AND($K' + r + '>=130,N($E' + r + ')>0,$E' + r + '<=80),' +
      '"Check - fast pace, "&ROUND((100-$E' + r + ')/10)&" missed",' +
      'IF($K' + r + '<90,"Building - below graph floor",' +
      'IF($K' + r + '<100,"Ready for takeoff",' +
      'IF($K' + r + '<130,"On pace",' +
      'IF($K' + r + '<170,"Strong","Very fast - check comprehension"))))))');

    // Trend. A single reading is noise; the expectation is improvement over
    // a year, not a number on a day.
    if (prev === null) {
      sh.getRange(r, 13).setValue('—');
    } else {
      sh.getRange(r, 13).setFormula(
        '=IF(OR($K' + r + '="",$K' + prev + '=""),"",' +
        'TEXT($K' + r + '-$K' + prev + ',"+0;-0;0")&" wpm")');
    }
    prev = r;
  });

  SpreadsheetApp.getUi().alert(
    'Reading speed ready\n\nRows: ' + rows.join(', ') +
    '\nType Words and Time. Everything else is a formula.' +
    '\n\nSpeed is tracked, not graded.');
}
