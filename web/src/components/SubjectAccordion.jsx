import { useState } from "react";

export default function SubjectAccordion({ subject, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const chapters = subject.chapters ?? [];

  return (
    <article className="subject-card">
      <button
        type="button"
        className="subject-card__header"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
      >
        <span className="subject-card__code">{subject.code}</span>
        <span className="subject-card__name">{subject.name}</span>
        {subject.credits ? <span className="subject-card__credits">{subject.credits} credits</span> : null}
        <span className="subject-card__chevron" data-open={open} aria-hidden="true">
          &#9656;
        </span>
      </button>

      {open && (
        <div className="subject-card__body">
          {chapters.length === 0 ? (
            <p className="state-message">No chapter data yet for this subject.</p>
          ) : (
            chapters.map((chapter) => (
              <div className="chapter" key={chapter.unit + chapter.title}>
                <p className="chapter__title">
                  <span className="chapter__unit">{chapter.unit}</span>
                  {chapter.title}
                </p>
                <ul className="chapter__topics">
                  {(chapter.topics ?? []).map((topic) => (
                    <li key={topic}>{topic}</li>
                  ))}
                </ul>
              </div>
            ))
          )}
        </div>
      )}
    </article>
  );
}
