import { useMemo, useState } from "react";
import FilterBar from "./components/FilterBar.jsx";
import SyllabusView from "./components/SyllabusView.jsx";
import { useSyllabusData } from "./hooks/useSyllabusData.js";
import { resolveSelection } from "./lib/filterOptions.js";

const EMPTY_SELECTION = {
  collegeId: "",
  programmeCode: "",
  year: "",
  semester: "",
  subjectCode: "",
};

export default function App() {
  const { colleges, loading, error } = useSyllabusData();
  const [selection, setSelection] = useState(EMPTY_SELECTION);

  const resolved = useMemo(() => resolveSelection(colleges, selection), [colleges, selection]);

  return (
    <div className="app">
      <header className="app-header">
        <p className="app-header__eyebrow">Curriculum &amp; Syllabus</p>
        <h1 className="app-header__title">Curriculum Board</h1>
        <p className="app-header__subtitle">
          Filter by college, course, year and semester to browse chapter-wise topics for each subject.
        </p>
      </header>

      {loading && <p className="state-message">Loading syllabus data…</p>}

      {error && (
        <p className="state-message state-message--error">
          Could not load syllabus data ({error.message}). Check that the JSON files exist under
          public/data/.
        </p>
      )}

      {!loading && !error && (
        <>
          <FilterBar
            selection={selection}
            onChange={setSelection}
            options={resolved.options}
            colleges={colleges}
          />
          <SyllabusView selection={selection} resolved={resolved} />
        </>
      )}

      <footer className="app-footer">
        Built as a learning project · data curated from public college curriculum pages
      </footer>
    </div>
  );
}
