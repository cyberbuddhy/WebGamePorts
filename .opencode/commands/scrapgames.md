---
description: Scrape internet for new WASM browser game ports not yet tracked
agent: general
subtask: true
---

# /scrapgames — WebGamePorts scraper

Goal: find NEW playable WebAssembly browser game ports (full-engine ports: real engine compiled to WASM, runs locally, not cloud streaming) that are NOT already in `LISTS.md` or `data/games.json` / `GAMES_EXTRA.md`, then append them with proof.

## 0. Load context

- Read `@README.md`, `@LISTS.md`, `@GAMES_EXTRA.md`, `@data/games.json`.
- Build a dedupe set: all `play_url` + `repo_url` + normalized titles already tracked, plus all 19 lists in `LISTS.md` (esp. Ultimate 474, genizy/web-ports, web-ports org, midzer, wasm.rip, webport.ing, quenq, dos.zone, gn-math, RetroPlay).

## 1. Search (use websearch + webfetch, livecrawl preferred)

Run ALL of these, 2025-2026 biased, current year 2026:

1. `site:github.com WebAssembly web port game playable browser Emscripten`
2. `playable in browser WebAssembly WebGPU port 2026 -cloud -streaming`
3. `Hacker News Show HN WASM game browser port`
4. `Reddit r/WebGames OR r/Emulation wasm browser port playable`
5. `itch.io OR gn-math OR wasm.rip OR webport.ing new web port`
6. `slqnt OR genizy OR web-ports OR midzer OR Virtastic OR wasm.ltd new port`
7. Re-check known movers: `GTA V browser mirror`, `hl2.slqnt.dev update`, `shar-wasm update`, `gunz.sigr.io update`, `Generals-WebAssembly update`, `openmw-web update`

For each candidate, fetch the Play URL + repo README. Extract:

- title, play_url (must load without login), repo_url (must have Emscripten/CMake/Makefile + `*.wasm` or build script)
- engine (e.g. Source leak, RAGE, reVC, ioquake3, OpenMW, Blitz3D, Stracciatella)
- tech path: `C/C++ → Emscripten → WASM`, renderer translation (`D3D8/9/11 → WebGL2/WebGPU`, `GLES → WebGL2`, `OpenAL → WebAudio`), threads (`pthreads/SharedArrayBuffer`), FS (`OPFS/IDBFS/MEMFS`), headers (`COOP/COEP`), MP (`WebRTC/MQTT`)
- needs_own_files? (BYO DAT/WAD/pk3/BIG or fully bundled)
- status: live / demo-live / repo-live / taken-down
- proof: 1-2 links (HN, Reddit, news, dev blog, commit)

## 2. Verify (reject if fail)

- Play URL returns 200 + serves `*.wasm`/`*.js`/`*.data` (or boots game canvas). Note if domain is parked / DMCA'd / offline.
- Repo builds or has prebuilt release + build docs (emsdk version pinned?). Reject pure JS remakes, Unity asset flips with no engine port, cloud-streaming sites (GeForce Now etc), fake "play" pages.
- Check against ALL lists in `LISTS.md` — fetch Ultimate README + genizy/web-ports + midzer.de/games + wasm.rip if needed. Only keep if Play+repo combo is genuinely new. If partial (e.g. Ultimate has repo but no Play URL, or vice versa), mark `in_lists: ["ultimate-partial-..."]` and still add with missing piece.

## 3. Write

- Append to `data/games.json` (`games[]`): `{title, play_url, repo_url, engine, tech, status, last_verified: YYYY-MM-DD, in_lists[], needs_own_files, notes}`. Bump `meta.last_scrape`, `meta.total_extra_not_in_any_list`.
- Append section to `GAMES_EXTRA.md`: `## N. Title` with bullets Play/Source/Tech/Needs/Proof/In-lists? (same style as existing).
- If a NEW list/hub found (not in `LISTS.md`), append row to `LISTS.md`.
- Every new game needs a card image: run `python3 scripts/fetch_images.py --embed` after editing data (resolves Steam capsule → GitHub repo preview; whatever is still imageless stays on the gradient placeholder and must be listed in the report). Never invent `img`/`pic` URLs by hand — only verified ones.
- Run `python3 scripts/validate.py` (checks JSON schema + duplicate play/repo URLs). Fix until clean.

## 4. Report back (single message)

- Added: N games (title — play_url — why new)
- New lists: N (or none)
- Dead/changed: any tracked Play URLs now offline (e.g. taken-down mirrors)
- Files changed: `data/games.json`, `GAMES_EXTRA.md`, `LISTS.md` (if applicable)
- Next scrape suggestions (queries that had signal)

Rules: facts only, no hallucinating Play URLs. If unsure a game runs locally vs streams, say so. Never commit secrets. `$ARGUMENTS` = optional focus (e.g. `/scrapgames fps` or `/scrapgames 2026-10`).
