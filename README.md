# Curriculum Board

A static site for browsing college curricula and syllabi, filterable by
college, course, year, semester and subject, with chapter-wise topics shown
in a collapsible view. Built as a learning project covering:

- A Python CLI that converts curriculum PDFs into structured JSON
- A React (Vite) front end that reads that JSON and renders filters + an
  accordion, with no backend required
- GitHub Pages hosting via GitHub Actions

```
syllabus-viewer/
├── parser/              Python: PDF -> JSON
│   ├── pdf_to_json.py    CLI entrypoint
│   ├── text_parser.py    regex/heuristic parsing logic (pure, testable)
│   ├── schema.py          shared data classes
│   ├── requirements.txt
│   └── tests/
├── web/                 React (Vite): the site itself
│   ├── public/data/       *.json syllabus files consumed by the app
│   ├── src/
│   └── tests/
└── .github/workflows/deploy.yml   GitHub Pages CI
```

## 1. Parser: turning a PDF into syllabus JSON

```bash
cd parser
pip install -r requirements.txt --break-system-packages   # or use a venv
python pdf_to_json.py path/to/CSE.pdf \
  --college "PSG Tech" \
  --programme-code CSE \
  --programme-name "B.E. Computer Science and Engineering" \
  --year 1 --semester 1 \
  --out ../web/public/data/psgtech.json \
  --merge
```

Curriculum PDFs bundle every year/semester into one file, and every
institution lays them out differently, so this script deliberately handles
**one (year, semester) slice per run** and merges it into the target JSON
with `--merge`. Run it once per semester you want to add.

The parser looks for two line shapes: a course-code header
(`20CS101   Problem Solving and Programming   4`) and a unit header
(`UNIT I INTRODUCTION TO PROGRAMMING`), and folds everything else under
the current unit into a topic list. Real PDFs will need you to inspect the
raw extracted text and tune the regexes in `text_parser.py` — that's the
point of keeping the parsing rules in one small, readable file.

Run the tests:

```bash
cd parser
python -m pytest tests/ -v
```

## 2. Web app: browsing the JSON

```bash
cd web
npm install
npm run dev        # http://localhost:5173
```

Two sample JSON files are already in `public/data/` (PSG Tech and PSG
iTech, both with a CSE programme) so the app works out of the box before
you've run the parser on a real PDF.

Run the tests:

```bash
cd web
npm run test
```

### Adding a new college or programme

1. Generate/merge its JSON with the parser (see above), or hand-edit a
   file under `public/data/` following the existing shape.
2. Register the file in `src/hooks/useSyllabusData.js`'s `DATA_SOURCES`
   list if it's a new college.

## 3. Deploying to GitHub Pages

1. Create a GitHub repo and push this project to it.
2. In `web/vite.config.js`, set `base` to `/<your-repo-name>/`.
3. In the repo's **Settings → Pages**, set the source to **GitHub
   Actions**.
4. Push to `main` — `.github/workflows/deploy.yml` builds and deploys
   `web/` automatically.

To deploy manually instead:

```bash
cd web
npm run build
npx gh-pages -d dist
```

## Data model

Every college JSON file follows this shape:

```
College { college, programmes: [
  Programme { code, name, years: [
    Year { year, semesters: [
      Semester { semester, subjects: [
        Subject { code, name, credits, chapters: [
          Chapter { unit, title, topics: [] }
        ]}
      ]}
    ]}
  ]}
]}
```

## Notes on the source data

Sample data in this repo was hand-curated for demo purposes and is
**not** a verbatim copy of any PDF — treat it as a starting structure,
not authoritative syllabus content. Always cross-check against the
official PDFs linked from your institution's site before relying on it.
