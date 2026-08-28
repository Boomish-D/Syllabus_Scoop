import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # make `schema`/`text_parser` importable

from text_parser import (
    normalise_unit_label,
    parse_subject_header,
    parse_subjects,
    split_topics,
)


def test_normalise_unit_label_roman():
    assert normalise_unit_label("I") == "Unit 1"
    assert normalise_unit_label("IV") == "Unit 4"


def test_normalise_unit_label_digit():
    assert normalise_unit_label("2") == "Unit 2"


def test_normalise_unit_label_unknown_passthrough():
    assert normalise_unit_label("A") == "Unit A"


def test_split_topics_semicolon_and_bullet():
    assert split_topics("Arrays; Linked Lists • Stacks") == ["Arrays", "Linked Lists", "Stacks"]


def test_split_topics_empty_string():
    assert split_topics("   ") == []


def test_parse_subject_header_with_credits():
    subject = parse_subject_header("20CS101   Problem Solving and Programming   4")
    assert subject is not None
    assert subject.code == "20CS101"
    assert subject.name == "Problem Solving and Programming"
    assert subject.credits == "4"


def test_parse_subject_header_without_credits():
    subject = parse_subject_header("CS3591 Computer Networks")
    assert subject is not None
    assert subject.code == "CS3591"
    assert subject.name == "Computer Networks"


def test_parse_subject_header_rejects_non_code_line():
    assert parse_subject_header("Course Objectives:") is None


def test_parse_subjects_builds_chapters_and_topics():
    lines = [
        "20CS101   Problem Solving and Programming   4",
        "UNIT I INTRODUCTION TO PROGRAMMING",
        "Algorithms; Flowcharts; Pseudocode",
        "Structured programming approach",
        "UNIT II C PROGRAMMING BASICS",
        "Data types; Operators; Control statements",
        "20CS102   Digital Principles and Systems Design   3",
        "UNIT I BOOLEAN ALGEBRA",
        "Logic gates; Minimization techniques",
    ]

    subjects = parse_subjects(lines)

    assert len(subjects) == 2

    first = subjects[0]
    assert first.code == "20CS101"
    assert len(first.chapters) == 2
    assert first.chapters[0].unit == "Unit 1"
    assert first.chapters[0].title == "INTRODUCTION TO PROGRAMMING"
    assert "Algorithms" in first.chapters[0].topics
    assert "Structured programming approach" in first.chapters[0].topics
    assert first.chapters[1].unit == "Unit 2"

    second = subjects[1]
    assert second.code == "20CS102"
    assert len(second.chapters) == 1
    assert "Logic gates" in second.chapters[0].topics


def test_parse_subjects_ignores_preamble_before_first_unit():
    lines = [
        "20CS101   Problem Solving and Programming   4",
        "Course Objectives: To understand basics of programming",
        "UNIT I INTRODUCTION",
        "Algorithms",
    ]
    subjects = parse_subjects(lines)
    assert len(subjects) == 1
    assert len(subjects[0].chapters) == 1  # preamble line was skipped, not made a topic


def test_parse_subjects_returns_empty_list_for_no_matches():
    assert parse_subjects(["just some unrelated text", "more text"]) == []
