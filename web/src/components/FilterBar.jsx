export default function FilterBar({ selection, onChange, options, colleges }) {
  function set(field, value) {
    // Changing an upstream field clears everything downstream of it,
    // since the old year/semester/subject may no longer exist for the
    // newly picked college/programme.
    const order = ["collegeId", "programmeCode", "year", "semester", "subjectCode"];
    const next = { ...selection, [field]: value };
    const changedIndex = order.indexOf(field);
    order.slice(changedIndex + 1).forEach((key) => {
      next[key] = "";
    });
    onChange(next);
  }

  return (
    <div className="filter-bar" role="group" aria-label="Syllabus filters">
      <div className="filter-field">
        <label htmlFor="filter-college">College</label>
        <select
          id="filter-college"
          value={selection.collegeId}
          onChange={(e) => set("collegeId", e.target.value)}
        >
          <option value="">Select college</option>
          {colleges.map((c) => (
            <option key={c.college} value={c.college}>
              {c.college}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label htmlFor="filter-programme">Course</label>
        <select
          id="filter-programme"
          value={selection.programmeCode}
          onChange={(e) => set("programmeCode", e.target.value)}
          disabled={!selection.collegeId}
        >
          <option value="">Select course</option>
          {options.programmes.map((p) => (
            <option key={p.code} value={p.code}>
              {p.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label htmlFor="filter-year">Year</label>
        <select
          id="filter-year"
          value={selection.year}
          onChange={(e) => set("year", e.target.value)}
          disabled={!selection.programmeCode}
        >
          <option value="">Select year</option>
          {options.years.map((y) => (
            <option key={y.year} value={y.year}>
              Year {y.year}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label htmlFor="filter-semester">Semester</label>
        <select
          id="filter-semester"
          value={selection.semester}
          onChange={(e) => set("semester", e.target.value)}
          disabled={!selection.year}
        >
          <option value="">Select semester</option>
          {options.semesters.map((s) => (
            <option key={s.semester} value={s.semester}>
              Semester {s.semester}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label htmlFor="filter-subject">Subject</label>
        <select
          id="filter-subject"
          value={selection.subjectCode}
          onChange={(e) => set("subjectCode", e.target.value)}
          disabled={!selection.semester}
        >
          <option value="">All subjects</option>
          {options.subjects.map((s) => (
            <option key={s.code} value={s.code}>
              {s.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
