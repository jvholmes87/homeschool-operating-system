#!/usr/bin/env python3
"""
Mechanical half of docs/08-privacy-rules.md.

The rules in that document are only worth as much as the thing enforcing them,
and the leaks that matter are the ones a tired person makes at 11pm. So they
fail a build rather than relying on anyone remembering.

Two entry points:
    python3 leak_scan.py          scan every file that ships; non-zero on a hit
    from leak_scan import scan    used by build_docs.py on generated pages

Region is deliberately NOT checked. What locates a child is place + time + a way
to recognise her; region alone is inert, and publishing it is what makes this
case study useful to the overseas military families most likely to need it. The
other two legs are what must never appear - see the privacy doc.
"""
import pathlib, re, sys

CHECKS = [
    # The name never gets the benefit of the doubt - checked against the raw
    # text, quotes and code included.
    ("STUDENT NAME IN OUTPUT",
     r"(?i)\bjamie\b", "raw"),

    # No trailing \b: "26 Nov" sits inside "26 November", and a word boundary
    # after it meant an earlier version of this check silently never fired.
    ("DATE OF BIRTH IN OUTPUT",
     r"(?i)\b(?:26\s*nov|nov\w*\s*26(?:th)?|2016-11-26"
     r"|26[/.-]11[/.-]2016|11[/.-]26[/.-]2016)", "prose"),

    # Two shapes, because the first version caught "she is ten" and sailed past
    # "her answers, written at nine", which is the same leak wearing a hat.
    ("student's age in output - 'upper elementary' is the limit",
     r"(?i)\b(?:she|her|the student)\b[^.]{0,40}"
     r"\b(?:turns|turned|is|was|aged)\s+(?:nine|ten|eleven|9|10|11)\b", "prose"),

    ("student's age in output - bare age reference",
     r"(?i)\b(?:(?:at|aged|age)\s+(?:nine|ten|eleven)"
     r"|(?:nine|ten|eleven)[- ]year[- ]old)\b", "prose"),

    ("named troop or unit number in output",
     r"(?i)\b(?:troop|OCMT)\s*#?\s*\d{2,4}\b", "prose"),

    ("school-issued identifier in output",
     r"(?i)\b(?:student|enrol?ment|account)\s*(?:id|number|no\.?|#)\s*[:#]?\s*\d{4,}", "prose"),

    ("private tracker URL in output",
     r"docs\.google\.com|spreadsheets/d/", "raw"),
]

# Files that ship. The generated docs/*.html are covered by build_docs.py as it
# writes them, and are re-checked here so a hand-edited page cannot slip past.
SHIPPED = ["index.html", "about.html", "record.html",
           "record.template.html", "README.md",
           "tools/*.html", "docs/*.html", "docs/*.md"]


def strip_quoted(text):
    """Remove quoted and code-fenced spans before leak-checking.

    The privacy doc has to quote the leaks it forbids - it says in as many words
    not to publish "she turns ten this month". A checker that cannot tell an
    example from an assertion makes the rules unwriteable, and the first thing
    anyone does with a guard they have to write around is delete it.
    """
    text = re.sub(r"<code>.*?</code>", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"<blockquote>.*?</blockquote>", " ", text, flags=re.S)
    # A quoted example may wrap across lines once markdown is reflowed, so
    # newlines are allowed inside the span. The length bound is what keeps one
    # stray quote character from swallowing the rest of the page.
    text = re.sub(r"[\"“](?:(?!</?p|[\"”]).){0,160}[\"”]", " ",
                  text, flags=re.S)
    return text


def scan(text):
    """Return a list of violated check labels for one document."""
    prose = None
    hits = []
    for label, pattern, scope in CHECKS:
        if scope == "prose":
            if prose is None:
                prose = strip_quoted(text)
            target = prose
        else:
            target = text
        if re.search(pattern, target):
            hits.append(label)
    return hits


def main():
    here = pathlib.Path(__file__).parent
    files, bad = [], 0
    for pat in SHIPPED:
        files.extend(sorted(here.glob(pat)))

    for f in files:
        hits = scan(f.read_text(errors="replace"))
        rel = f.relative_to(here)
        if hits:
            bad += 1
            print("FAIL  %s" % rel)
            for h in hits:
                print("        %s" % h)
        else:
            print("ok    %s" % rel)

    print("\nscanned %d files" % len(files))
    if bad:
        print("%d FILE(S) WOULD LEAK - do not publish" % bad)
        return 1
    print("no leaks found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
