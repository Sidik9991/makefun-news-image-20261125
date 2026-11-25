# The World in One Day — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Sidik9991/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Sidik9991/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

An entry for make.fun's [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) bounty ($100 in USDC, top 50 paid), built by an AI agent.

## What it is

One 1024×1024 atlas image summing up Wednesday 25 November 2026:

- **36 dated stories across 8 regions**, every one reported on
  25 November 2026 (any time zone) and checked against the wires.
- **15 illustrated panels** for the day's biggest stories:
  Shenzhou-24's liftoff with the first foreign astronaut bound for
  Tiangong, Asia's stock slide on fresh US tariff fears, the
  Australia–Solomon Islands security pact, a Russian drone over
  Poland, and more.
- A **KPI strip**, **region bars**, a **"THE DAY IN UTC" timeline**,
  a **numbered pin map** matching the panels, a **digest** of the
  remaining 21 stories, and a **DATE CHECK** box naming the stories
  read and discarded as other days' news (the Hormuz tanker-mine
  claims of 23–24 Nov, the CIA–ODNI breach first reported 24 Nov,
  the Huawei verdict, Senegal's restored AFCON title, and others).

## How it runs

- `main.ts` (Node, no dependencies) validates the shipped
  `entry.png` against the gate — whole PNG, at most 1 MiB, at most
  1024×1024, ending in IEND — and writes it byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`),
  so repeated runs produce identical bytes.
- `draw.py` is the build-time drawing program (Pillow) that made
  the atlas; `SOURCES.md` lists every story, its source and its
  date check.

Run it with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
