import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// IMPORTANT: change `base` to match your GitHub repo name, e.g.
// "/Syllabus-Scoop/" if this repo is deployed at
// https://<username>.github.io/Syllabus-Scoop/
// Leave it as "/" if you deploy to a custom domain or a user/org page
// (https://<username>.github.io/).
export default defineConfig({
  plugins: [react()],
  base: "/Syllabus_Scoop/",
  test: {
    environment: "jsdom",
    setupFiles: "./tests/setup.js",
    globals: true,
  },
});
