import SubjectAccordion from "./SubjectAccordion.jsx";

export default function SyllabusView({ selection, resolved }) {
  const { semester, subject, options } = resolved;

  if (!selection.collegeId) {
    return <p className="state-message">Pick a college to begin.</p>;
  }
  if (!selection.programmeCode) {
    return <p className="state-message">Pick a course to see its curriculum.</p>;
  }
  if (!selection.year || !selection.semester) {
    return <p className="state-message">Pick a year and semester to see subjects.</p>;
  }
  if (!semester || options.subjects.length === 0) {
    return <p className="state-message">No subjects recorded yet for this semester.</p>;
  }

  const subjectsToShow = selection.subjectCode ? (subject ? [subject] : []) : options.subjects;

  return (
    <div className="subject-list">
      {subjectsToShow.map((s, index) => (
        <SubjectAccordion key={s.code} subject={s} defaultOpen={subjectsToShow.length === 1 || index === 0} />
      ))}
    </div>
  );
}
