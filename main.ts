// news-image-20261124 — deterministic entry writer.
//
// The poster image (entry.png) is baked into this repository: it was
// composed offline from six generated editorial illustrations plus real
// rendered text, so no network or image generation is needed at run time.
// This program simply copies the baked-in PNG to /output/entry.png, which
// makes the output byte-identical on every run.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = join(__dirname, "entry.png");
const out = "/output/entry.png";

if (!existsSync(src)) {
  console.error(`entry.png not found next to main.ts (${src})`);
  process.exit(1);
}

mkdirSync(dirname(out), { recursive: true });
copyFileSync(src, out);
console.log(`Wrote ${out}`);
