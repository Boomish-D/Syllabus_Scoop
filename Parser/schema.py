"""
Data model for the syllabus JSON files.

This mirrors the shape consumed by the React app in web/src, so any change
here must be mirrored in web/src/hooks/useSyllabusData.js's expectations.

    College
      -> Programme (e.g. "B.E. Computer Science and Engineering")
          -> Year (1-4)
              -> Semester (1-2)
                  -> Subject (code, name, credits)
                      -> Chapter / Unit (title, topics[])
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Chapter:
    unit: str
    title: str
    topics: List[str] = field(default_factory=list)


@dataclass
class Subject:
    code: str
    name: str
    credits: str = ""
    chapters: List[Chapter] = field(default_factory=list)


@dataclass
class Semester:
    semester: int
    subjects: List[Subject] = field(default_factory=list)


@dataclass
class Year:
    year: int
    semesters: List[Semester] = field(default_factory=list)


@dataclass
class Programme:
    code: str
    name: str
    years: List[Year] = field(default_factory=list)


@dataclass
class College:
    college: str
    programmes: List[Programme] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
