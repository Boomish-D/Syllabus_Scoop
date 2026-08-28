import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

pdfplumber = pytest.importorskip("pdfplumber")
reportlab_canvas = pytest.importorskip("reportlab.pdfgen.canvas")

from pdf_to_json import build_college_json, extract_lines_from_pdf, merge_college_dicts


def _make_sample_pdf(path: Path) -> None:
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(path))
    lines = [
        "20CS101   Problem Solving and Programming   4",
        "UNIT I INTRODUCTION TO PROGRAMMING",
        "Algorithms; Flowcharts; Pseudocode",
        "UNIT II C PROGRAMMING BASICS",
        "Data types; Operators",
    ]
    y = 800
    for line in lines:
        c.drawString(50, y, line)
        y -= 20
    c.save()


def test_extract_lines_from_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    _make_sample_pdf(pdf_path)

    lines = extract_lines_from_pdf(pdf_path, first_page=None, last_page=None)

    assert any("20CS101" in line for line in lines)
    assert any("UNIT I" in line for line in lines)


def test_build_college_json_end_to_end(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    _make_sample_pdf(pdf_path)
    lines = extract_lines_from_pdf(pdf_path, None, None)

    result = build_college_json(
        college_name="PSG Tech",
        programme_code="CSE",
        programme_name="B.E. Computer Science and Engineering",
        year=1,
        semester=1,
        lines=lines,
    )

    assert result["college"] == "PSG Tech"
    subjects = result["programmes"][0]["years"][0]["semesters"][0]["subjects"]
    assert len(subjects) == 1
    assert subjects[0]["code"] == "20CS101"
    assert len(subjects[0]["chapters"]) == 2


def test_merge_college_dicts_adds_new_semester():
    base = {
        "college": "PSG Tech",
        "programmes": [
            {
                "code": "CSE",
                "name": "B.E. CSE",
                "years": [{"year": 1, "semesters": [{"semester": 1, "subjects": [{"code": "A"}]}]}],
            }
        ],
    }
    incoming = {
        "college": "PSG Tech",
        "programmes": [
            {
                "code": "CSE",
                "name": "B.E. CSE",
                "years": [{"year": 1, "semesters": [{"semester": 2, "subjects": [{"code": "B"}]}]}],
            }
        ],
    }

    merged = merge_college_dicts(base, incoming)

    semesters = merged["programmes"][0]["years"][0]["semesters"]
    assert {s["semester"] for s in semesters} == {1, 2}


def test_merge_college_dicts_rejects_different_colleges():
    base = {"college": "PSG Tech", "programmes": []}
    incoming = {"college": "PSG iTech", "programmes": []}
    with pytest.raises(ValueError):
        merge_college_dicts(base, incoming)
