// Builds the site from src/trip.html.
//   node src/build.mjs [fragment-out]
// - puts Leaflet (src/vendor) inline in place of its CDN <script src>, so a slow CDN can't hold up the page
// - writes index.html (the full page) at the repo root
// - optionally also writes the inlined fragment to fragment-out (the claude.ai artifact copy)
// - syntax-checks every inline <script>
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>';

const src = readFileSync(join(here, "trip.html"), "utf8");
if (!src.includes(CDN)) throw new Error("Leaflet <script src> not found in trip.html");
const leaflet = readFileSync(join(here, "vendor/leaflet-1.9.4.js"), "utf8");
if (/<\/script/i.test(leaflet)) throw new Error("vendor/leaflet-1.9.4.js contains </script");

const frag = src.replace(CDN, () => "<script>\n" + leaflet.trim() + "\n</script>");
const page =
  '<!doctype html>\n<html lang="zh-Hant">\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  '<link rel="icon" href="data:,">\n' + frag + "\n</html>\n";

const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)];
scripts.forEach(([, js]) => new Function(js));

writeFileSync(join(here, "../index.html"), page);
if (process.argv[2]) writeFileSync(process.argv[2], frag);
console.log(`build ok: index.html ${Buffer.byteLength(page)} bytes, ${scripts.length} inline scripts parse`);
