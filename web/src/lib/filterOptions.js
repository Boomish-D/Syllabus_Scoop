/**
 * All functions here are pure (no state, no side effects) so they can be
 * unit tested directly, and reused by any component that needs to derive
 * filter options from the raw college JSON.
 */

export function getProgrammes(college) {
  if (!college) return [];
  return college.programmes ?? [];
}

export function findProgramme(college, programmeCode) {
  return getProgrammes(college).find((p) => p.code === programmeCode) ?? null;
}

export function getYears(programme) {
  if (!programme) return [];
  return [...(programme.years ?? [])].sort((a, b) => a.year - b.year);
}

export function findYear(programme, yearNumber) {
  return getYears(programme).find((y) => y.year === Number(yearNumber)) ?? null;
}

export function getSemesters(year) {
  if (!year) return [];
  return [...(year.semesters ?? [])].sort((a, b) => a.semester - b.semester);
}

export function findSemester(year, semesterNumber) {
  return getSemesters(year).find((s) => s.semester === Number(semesterNumber)) ?? null;
}

export function getSubjects(semester) {
  if (!semester) return [];
  return semester.subjects ?? [];
}

export function findSubject(semester, subjectCode) {
  return getSubjects(semester).find((s) => s.code === subjectCode) ?? null;
}

/**
 * Given the full colleges array and a partial selection, resolve as far
 * down the tree as the selection allows and return every level's
 * resolved object plus the options available at the next level.
 */
export function resolveSelection(colleges, selection) {
  const college = colleges.find((c) => c.college === selection.collegeId) ?? null;
  const programme = findProgramme(college, selection.programmeCode);
  const year = findYear(programme, selection.year);
  const semester = findSemester(year, selection.semester);
  const subject = findSubject(semester, selection.subjectCode);

  return {
    college,
    programme,
    year,
    semester,
    subject,
    options: {
      programmes: getProgrammes(college),
      years: getYears(programme),
      semesters: getSemesters(year),
      subjects: getSubjects(semester),
    },
  };
}
