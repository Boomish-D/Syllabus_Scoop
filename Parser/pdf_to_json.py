#!/usr/bin/env python3
"""
pdf_to_json.py - Convert a college curriculum PDF into the structured
syllabus JSON consumed by the web viewer.

Usage:
    python pdf_to_json.py input.pdf \
        --college "PSG Tech" \
        --programme-code CSE \
        --programme-name "B.E. Computer Science and Engineering" \
        --year 2 --semester 3 \
        --out ../web/public/data/psgtech.json \
        --merge

Because curriculum PDFs are laid out differently per institution and
usually bundle every year/semester into one file, this script processes
ONE (year, semester) slice per run and merges the result into the target
JSON. Run it once per semester you want to add, pointing --out at the same
file each time with --merge.

If pdfplumber cannot be installed in your environment (see requirements.txt),
you can still exercise all the parsing logic via text_parser.py directly -
see parser/tests/test_text_parser.py for examples that need no PDF at all.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from schema import College, Programme, Semester, Year
from text_parser import parse_subjects


def extract_lines_from_pdf(pdf_path: Path, first_page: int | None, last_page: int | None) -> List[str]:
    try:
        import pdfplumber
    except ImportError as exc:  # pragma: no cover - exercised only when dep missing
        raise SystemExit(
            "pdfplumber is required to read PDFs. Install it with:\n"
            "    pip install -r requirements.txt --break-system-packages"
        ) from exc

    lines: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        if first_page or last_page:
            start = (first_page or 1) - 1
            end = last_page or len(pages)
            pages = pages[start:end]
        for page in pages:
            text = page.extract_text() or ""
            lines.extend(text.splitlines())
    return lines


def build_college_json(
    college_name: str,
    programme_code: str,
    programme_name: str,
    year: int,
    semester: int,
    lines: List[str],
) -> dict:
    subjects = parse_subjects(lines)
    programme = Programme(
        code=programme_code,
        name=programme_name,
        years=[Year(year=year, semesters=[Semester(semester=semester, subjects=subjects)])],
    )
    college = College(college=college_name, programmes=[programme])
    return college.to_dict()


def merge_college_dicts(base: dict, incoming: dict) -> dict:
    """Deep-merge `incoming` (one college/programme/year/semester slice)
    into `base`, matching on the natural keys at each level."""
    if not base:
        return incoming
    if base.get("college") != incoming.get("college"):
        raise ValueError(
            f"Refusing to merge different colleges: "
            f"{base.get('college')!r} vs {incoming.get('college')!r}"
        )

    programmes = base.setdefault("programmes", [])
    for new_prog in incoming.get("programmes", []):
        existing_prog = next((p for p in programmes if p["code"] == new_prog["code"]), None)
        if existing_prog is None:
            programmes.append(new_prog)
            continue

        years = existing_prog.setdefault("years", [])
        for new_year in new_prog.get("years", []):
            existing_year = next((y for y in years if y["year"] == new_year["year"]), None)
            if existing_year is None:
                years.append(new_year)
                continue

            semesters = existing_year.setdefault("semesters", [])
            for new_sem in new_year.get("semesters", []):
                existing_sem = next(
                    (s for s in semesters if s["semester"] == new_sem["semester"]), None
                )
                if existing_sem is None:
                    semesters.append(new_sem)
                else:
                    existing_sem["subjects"] = new_sem["subjects"]  # replace, don't dupe

    return base


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", type=Path, help="Path to the curriculum/syllabus PDF")
    parser.add_argument("--college", required=True, help='e.g. "PSG Tech" or "PSG iTech"')
    parser.add_argument("--programme-code", required=True, help='e.g. "CSE"')
    parser.add_argument("--programme-name", required=True, help='e.g. "B.E. Computer Science and Engineering"')
    parser.add_argument("--year", type=int, required=True, help="1-4")
    parser.add_argument("--semester", type=int, required=True, help="1-2 within that year, or overall 1-8")
    parser.add_argument("--first-page", type=int, default=None)
    parser.add_argument("--last-page", type=int, default=None)
    parser.add_argument("--out", type=Path, required=True, help="Output JSON path")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge into an existing --out file instead of overwriting it",
    )
    args = parser.parse_args(argv)

    if not args.pdf.exists():
        parser.error(f"PDF not found: {args.pdf}")

    lines = extract_lines_from_pdf(args.pdf, args.first_page, args.last_page)
    result = build_college_json(
        args.college, args.programme_code, args.programme_name, args.year, args.semester, lines
    )

    if args.merge and args.out.exists():
        existing = json.loads(args.out.read_text(encoding="utf-8"))
        result = merge_college_dicts(existing, result)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    subject_count = sum(
        len(sem["subjects"])
        for prog in result["programmes"]
        for yr in prog["years"]
        for sem in yr["semesters"]
    )
    print(f"Wrote {args.out} ({subject_count} subject(s) parsed for this run)")
    if subject_count == 0:
        print(
            "No subjects detected - the PDF's layout may not match the expected "
            "patterns. Inspect the extracted text and adjust parser/text_parser.py.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
