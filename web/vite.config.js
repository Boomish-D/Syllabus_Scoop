import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// IMPORTANT: change `base` to match your GitHub repo name, e.g.
// "/syllabus-viewer/" if this repo is deployed at
// https://<username>.github.io/syllabus-viewer/
// Leave it as "/" if you deploy to a custom domain or a user/org page
// (https://<username>.github.io/).
export default defineConfig({
  plugins: [react()],
  base: "/syllabus-viewer/",
  test: {
    environment: "jsdom",
    setupFiles: "./tests/setup.js",
    globals: true,
  },
});
