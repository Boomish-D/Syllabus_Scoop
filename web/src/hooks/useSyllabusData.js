import { useEffect, useState } from "react";

// Add a new entry here whenever a new college JSON file is added under
// public/data/ - this is the one place that lists what's available.
const DATA_SOURCES = [
  { id: "psgtech", label: "PSG Tech", file: "psgtech.json" },
  { id: "psgitech", label: "PSG iTech", file: "psgitech.json" },
];

/**
 * Loads every college JSON file listed in DATA_SOURCES.
 * Returns { colleges, loading, error } where `colleges` is an array of
 * the raw parsed JSON objects (one per college), in DATA_SOURCES order.
 */
export function useSyllabusData() {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function loadAll() {
      try {
        const base = import.meta.env.BASE_URL || "/";
        const results = await Promise.all(
          DATA_SOURCES.map(async (source) => {
            const response = await fetch(`${base}data/${source.file}`);
            if (!response.ok) {
              throw new Error(`Failed to load ${source.file}: ${response.status}`);
            }
            return response.json();
          })
        );
        if (!cancelled) {
          setColleges(results);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
          setLoading(false);
        }
      }
    }

    loadAll();
    return () => {
      cancelled = true;
    };
  }, []);

  return { colleges, loading, error };
}

export { DATA_SOURCES };
