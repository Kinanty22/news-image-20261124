# World in One Day — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)

A program that draws one newspaper front page summing up the world news
of **Tuesday 24 November 2026** — and writes it to `entry.png`.

## The day, in five stories

1. **Jets scrambled off Korea** — Russian military planes entered
   South Korea's air defence zone near Ulleung Island on Tuesday
   morning; Seoul scrambled fighter jets and briefly told islanders
   to take shelter. No airspace violation; Seoul will protest to
   Moscow.
2. **Nvidia comeback lifts Asia** — Nvidia reinstated Jensen Huang
   as chief executive on Monday; shares rose 33%, Nasdaq +6%,
   S and P +4%. On Tuesday Asia followed: Kospi +7.4%, Taiwan +9%;
   the dollar sat near a 20-month high.
3. **Ukraine sinks Russian warship in Libya** — Zelensky confirmed
   on Monday that seven sea drones sank the corvette Merkury at
   Benghazi and hit the cargo ship MV Angara. A second Russian
   cargo ship was hit in the Baltic Sea.
4. **Trump to Iran: deal by New Year or strikes** — President Trump
   said the US could resume strikes on Iran in 2027 if no nuclear
   deal is reached, and ships breaking the US naval blockade would
   be sunk. Tehran says the blockade must be broken.
5. **COP31 ends with no deal** — climate talks in Antalya, Turkiye
   closed after record overtime with no agreement; the EU and 130
   nations rejected a draft with no mention of fossil fuels.
6. **Plus:** Indonesia, 24 dead and about 30 missing after a candy
   factory fire in Cikande, Banten; Bangladesh to vaccinate 50
   million children against typhoid; Thai-Cambodia border fighting
   on hold after a truce.

Sources: Reuters, BBC, CNN, AP, WSJ, The Times — 24 November 2026.
Every fact was checked against reporting published on the day; where
a story broke earlier, the image dates it (confirmed Monday, Sunday).

## How it works

`main.py` is pure Python 3 standard library — no packages, no network.
It draws the front page with its own rasteriser (rectangles, lines,
circles, polygons and a built-in 5×7 bitmap font) and encodes the PNG
by hand with `zlib`, so two runs produce byte-identical output.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: `out/entry.png`, 1024×1024 PNG, about 24 KB (limit: 1 MiB).

## Entry

- Competition: [news-image-20261124](https://make.fun/c/news-image-20261124)
  — "Sum up 24 November's world news in one image"
- Entrypoint: `main.py` (Python 3.13, standard library only)
- License: MIT (see `LICENSE`)

## Note for the submitter

The repository-specific make.fun rank/reward badges
(`https://make.fun/badge/news-image-20261124/<owner>/<repo>/rank.svg`
and `.../reward.svg`) and the GitHub About (website on make.fun, topic
`makefun`) still need to be added once the repository exists, before
submitting. Do not edit this README outside the recorded builder
session to add them — use the GitHub web UI instead, or accept the
transcript-gate risk explicitly.
