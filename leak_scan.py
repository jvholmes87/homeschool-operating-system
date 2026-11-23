#!/usr/bin/env python3
"""Privacy checks without publishing identity-specific deny rules.

PRIVATE_DENY_PATTERNS_JSON must be supplied from a private environment or secret
store. It is a JSON array of regular-expression strings. Never commit its value.
The checker fails closed if these private rules are missing or invalid.
"""
import json, os, pathlib, re, sys

CHECKS = [("student's age in output - 'upper elementary' is the limit", '(?i)\\b(?:she|her|the student)\\b[^.]{0,40}\\b(?:turns|turned|is|was|aged)\\s+(?:nine|ten|eleven|9|10|11)\\b', 'prose'), ("student's age in output - bare age reference", '(?i)\\b(?:(?:at|aged|age)\\s+(?:nine|ten|eleven)|(?:nine|ten|eleven)[- ]year[- ]old)\\b', 'prose'), ('named troop or unit number in output', '(?i)\\b(?:troop|OCMT)\\s*#?\\s*\\d{2,4}\\b', 'prose'), ('school-issued identifier in output', '(?i)\\b(?:student|enrol?ment|account)\\s*(?:id|number|no\\.?|#)\\s*[:#]?\\s*\\d{4,}', 'prose'), ('private tracker URL in output', 'docs\\.google\\.com|spreadsheets/d/', 'raw')]
SHIPPED = ["index.html", "about.html", "record.html", "record.template.html",
           "README.md", "tools/*.html", "docs/*.html", "docs/*.md"]

def private_checks():
    try:
        raw = os.environ.get("PRIVATE_DENY_PATTERNS_JSON", "")
        patterns = json.loads(raw)
        if not isinstance(patterns, list) or not patterns or not all(isinstance(p, str) and p for p in patterns):
            raise ValueError()
        return [re.compile(p, re.I) for p in patterns]
    except (ValueError, TypeError, re.error):
        raise RuntimeError("Private privacy rules are missing or invalid; refusing publication scan.") from None

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
    hits = []
    # Validate private configuration before any apparently successful result.
    if any(pattern.search(text) for pattern in private_checks()):
        hits.append("PRIVATE DENY RULE MATCH — value withheld")
    prose = None
    for label, pattern, scope in CHECKS:
        if scope == "prose" and prose is None:
            prose = strip_quoted(text)
        if re.search(pattern, prose if scope == "prose" else text):
            hits.append(label)
    return hits

def main():
    try:
        private_checks()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2
    here = pathlib.Path(__file__).parent
    bad = 0
    files = sorted({f for pattern in SHIPPED for f in here.glob(pattern)})
    for path in files:
        hits = scan(path.read_text(errors="replace"))
        print(("FAIL  " if hits else "ok    ") + str(path.relative_to(here)))
        if hits:
            bad += 1
            for label in hits:
                print("        " + label)
    print("scanned %d files" % len(files))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
