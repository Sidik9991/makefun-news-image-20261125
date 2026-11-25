// The World in One Day — Wednesday 25 November 2026 (news-image-20261125).
//
// The atlas image is drawn at build time by draw.py (kept in this repo,
// with every story and its source in SOURCES.md) and shipped as
// entry.png. This program validates that image against the bounty's
// gate (a whole PNG, at most 1 MiB, at most 1024x1024) and writes it
// to the output directory, byte for byte, so both grader runs agree.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIM = 1024;

function findImage(): Buffer {
  const here = dirname(fileURLToPath(import.meta.url));
  for (const p of [join(here, "entry.png"), join(process.cwd(), "entry.png")]) {
    try {
      return readFileSync(p);
    } catch {
      // try the next candidate
    }
  }
  throw new Error("entry.png not found next to main.ts or in the working directory");
}

function main(): void {
  const png = findImage();

  // Gate checks: PNG signature, size cap, IHDR dimensions.
  const sig = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (png.length < 8 || !sig.every((b, i) => png[i] === b)) {
    throw new Error("entry.png is not a PNG");
  }
  if (png.length > MAX_BYTES) {
    throw new Error(`entry.png is ${png.length} bytes, over the ${MAX_BYTES} cap`);
  }
  const width = png.readUInt32BE(16);
  const height = png.readUInt32BE(20);
  if (width > MAX_DIM || height > MAX_DIM) {
    throw new Error(`entry.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} cap`);
  }
  // Whole image: the file must end with the IEND chunk (type + CRC).
  const tail = png.subarray(png.length - 8, png.length - 4).toString("ascii");
  if (tail !== "IEND") {
    throw new Error("entry.png does not end with an IEND chunk");
  }
  const sha = createHash("sha256").update(png).digest("hex");

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, "entry.png");
  writeFileSync(outPath, png);

  // Re-read and verify: the written file must be byte-identical.
  const back = readFileSync(outPath);
  if (!back.equals(png)) {
    throw new Error("written entry.png differs from the shipped image");
  }
  console.log(`entry.png OK: ${png.length} bytes, ${width}x${height}, sha256 ${sha}, written to ${outPath}`);
}

main();
