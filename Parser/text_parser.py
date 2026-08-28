"""
Turns raw text (already extracted from a PDF page) into structured
Subject / Chapter objects.

College curriculum PDFs are not consistent between institutions, so this
module deliberately works off a small set of regex patterns rather than
trying to be a universal PDF-layout parser. When a new PDF format does not
match, `parse_subjects` simply returns fewer/blank results rather than
raising - the intent is you inspect the output and adjust PATTERNS, not
that every PDF works perfectly on the first try.

Recognised line shapes (case-insensitive):
    Subject header   : "20CS101   Problem Solving and Programming   4"
                        (course code, name, optional trailing credit number)
    Unit / chapter    : "UNIT I   INTRODUCTION TO PROGRAMMING   9"
                         "Unit 1 - Introduction to Programming"
    Topic line        : anything else, folded into the current chapter's
                         topic list, split on common delimiters (; , )
"""
from __future__ import annotations

import re
from typing import List, Optional

from schema import Chapter, Subject

# A course code: 2-4 letters/digits prefix, then letters+digits, e.g.
# "20CS101", "CS3591", "GE3151". Deliberately permissive.
SUBJECT_CODE_RE = re.compile(r"^\s*([A-Z]{2}\d{2}[A-Z]{0,4}\d{2,4}|[0-9]{2}[A-Z]{2,4}\d{2,4})\b")

# "UNIT I", "UNIT 1", "Unit-2", "UNIT IV:" ... followed by a title
UNIT_RE = re.compile(
    r"^\s*UNIT\s*[-:]?\s*([IVX]+|\d+)\s*[:\-–]?\s*(.*)$",
    re.IGNORECASE,
)

ROMAN_MAP = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8}

TOPIC_SPLIT_RE = re.compile(r"\s*[;•]\s*|\s{2,}")


def _clean(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def normalise_unit_label(raw: str) -> str:
    """Turn 'I' / '1' / 'IV' into a consistent 'Unit N' label."""
    raw = raw.strip().upper()
    if raw in ROMAN_MAP:
        return f"Unit {ROMAN_MAP[raw]}"
    if raw.isdigit():
        return f"Unit {int(raw)}"
    return f"Unit {raw}"


def split_topics(text: str) -> List[str]:
    """Split a comma/semicolon/bullet separated blob of topics into a list."""
    text = _clean(text)
    if not text:
        return []
    parts = re.split(r"[;•]|(?<!\d),\s*(?=[A-Z])", text)
    parts = [p.strip(" .,") for p in parts if p.strip(" .,")]
    return parts or [text]


def parse_subject_header(line: str) -> Optional[Subject]:
    """Return a Subject if this line looks like a course-code header row."""
    match = SUBJECT_CODE_RE.match(line)
    if not match:
        return None
    code = match.group(1)
    rest = _clean(line[match.end():])

    credits = ""
    credit_match = re.search(r"(\d(?:\.\d)?)\s*$", rest)
    name = rest
    if credit_match and len(rest) - credit_match.start() <= 4:
        credits = credit_match.group(1)
        name = rest[: credit_match.start()].strip(" -")

    if not name:
        return None
    return Subject(code=code, name=name, credits=credits)


def parse_subjects(lines: List[str]) -> List[Subject]:
    """
    Walk a list of text lines (one syllabus / one course's pages) and build
    a list of Subject objects, each with its Chapter/Unit breakdown.

    A new Subject starts whenever a line matches a course-code header.
    A new Chapter starts whenever a line matches "UNIT <n>".
    Any other non-empty line is treated as topic content for the current
    chapter (or ignored if no chapter has started yet).
    """
    subjects: List[Subject] = []
    current_subject: Optional[Subject] = None
    current_chapter: Optional[Chapter] = None

    for raw_line in lines:
        line = _clean(raw_line)
        if not line:
            continue

        subject = parse_subject_header(line)
        if subject:
            current_subject = subject
            current_chapter = None
            subjects.append(current_subject)
            continue

        unit_match = UNIT_RE.match(line)
        if unit_match and current_subject is not None:
            label = normalise_unit_label(unit_match.group(1))
            title = _clean(unit_match.group(2)) or label
            current_chapter = Chapter(unit=label, title=title, topics=[])
            current_subject.chapters.append(current_chapter)
            continue

        if current_chapter is not None:
            current_chapter.topics.extend(split_topics(line))
        # Lines before any UNIT/subject (course objectives, outcomes,
        # textbook lists, etc.) are intentionally skipped - keep the JSON
        # focused on chapter/topic content for the UI.

    return subjects
