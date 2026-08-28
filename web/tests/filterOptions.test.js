import { describe, expect, it } from "vitest";
import { resolveSelection, getProgrammes, getYears } from "../src/lib/filterOptions.js";

const sampleColleges = [
  {
    college: "PSG Tech",
    programmes: [
      {
        code: "CSE",
        name: "B.E. CSE",
        years: [
          {
            year: 1,
            semesters: [
              {
                semester: 1,
                subjects: [
                  { code: "20CS101", name: "Programming", chapters: [] },
                  { code: "20MA101", name: "Maths", chapters: [] },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
];

describe("getProgrammes", () => {
  it("returns empty array for null college", () => {
    expect(getProgrammes(null)).toEqual([]);
  });

  it("returns the programmes list for a college", () => {
    expect(getProgrammes(sampleColleges[0])).toHaveLength(1);
  });
});

describe("getYears", () => {
  it("sorts years ascending", () => {
    const programme = {
      years: [{ year: 3, semesters: [] }, { year: 1, semesters: [] }, { year: 2, semesters: [] }],
    };
    expect(getYears(programme).map((y) => y.year)).toEqual([1, 2, 3]);
  });
});

describe("resolveSelection", () => {
  it("resolves nothing when selection is empty", () => {
    const result = resolveSelection(sampleColleges, {
      collegeId: "",
      programmeCode: "",
      year: "",
      semester: "",
      subjectCode: "",
    });
    expect(result.college).toBeNull();
    expect(result.options.programmes).toEqual([]);
  });

  it("resolves the full chain when a full selection is given", () => {
    const result = resolveSelection(sampleColleges, {
      collegeId: "PSG Tech",
      programmeCode: "CSE",
      year: "1",
      semester: "1",
      subjectCode: "20CS101",
    });
    expect(result.college.college).toBe("PSG Tech");
    expect(result.programme.code).toBe("CSE");
    expect(result.year.year).toBe(1);
    expect(result.semester.semester).toBe(1);
    expect(result.subject.code).toBe("20CS101");
    expect(result.options.subjects).toHaveLength(2);
  });

  it("returns null subject when subjectCode does not match", () => {
    const result = resolveSelection(sampleColleges, {
      collegeId: "PSG Tech",
      programmeCode: "CSE",
      year: "1",
      semester: "1",
      subjectCode: "does-not-exist",
    });
    expect(result.subject).toBeNull();
  });
});
