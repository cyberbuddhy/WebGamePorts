# WebGamePorts

Every WebAssembly browser game port in one place — like `playgta5.com` but for everything.

`playgta5.com` (Oct 2026, now taken down) proved the pattern: real PC engine compiled to `wasm64` + WebGPU, D3D calls translated in a worker, assets streamed over HTTP, runs locally — no cloud streaming. This repo tracks **every game that does the same**, plus **every list that tracks them**, plus games **not in any list yet**.

## Contents

- `README.md` — this overview + master table (start here)
- `LISTS.md` — list of every list (all known catalogs/hubs)
- `GAMES_EXTRA.md` — games NOT in any list (2025-2026 finds, with proof)
- `data/games.json` — machine-readable master data (`/scrapgames` updates this)
- `.opencode/commands/scrapgames.md` — `/scrapgames` scraper prompt for AI agents
- `scripts/` — helpers to validate links

## Master table (condensed)

Tech legend: `Emscripten`, `wasm64 + threads + SharedArrayBuffer`, `D3D8/9/11 → WebGL2/WebGPU`, `OPFS/IndexedDB`, `COOP/COEP`.

### AAA / full-engine ports (playgta5-class)

| Game | Play | Source | Tech | Status 2026-10-09 | In any list? |
|---|---|---|---|---|---|
| GTA V (RAGE) | `playgta5.com` (offline, archived `shadany7824/playgta5`) | leaked source + `game.wasm` 63MB, 91k funcs, D3D11→WebGPU | wasm64, 75 threads, 32MB ring, 4,808 WGSL shaders | Taken down Oct 6-8 | No |
| Half-Life 2 + Eps | https://hl2.slqnt.dev | slqnt + 98006, based on `weliveinhell` Portal port + `nillerusr` ToGLES | Source → Emscripten, GLES→WebGL2, per-map .data chunks, IDBFS saves | Live | Partial (Ultimate #196, demo only, no repo) |
| Portal (base for HL2) | via `weliveinhell` portal webport | `weliveinhell` / `nillerusr` Source leak fork | ToGLES → WebGL2 | Live | Partial |
| GTA: Vice City (reVC) | https://revc.wasm.ltd + https://quenq.com/apps/vice-city/ | `origami-ltd/wasm-revc` (reVC decomp) / `Lolendor/reVCDOS` | Emscripten, WebGL2, streaming assets, BYO copy | Live | Partial (Ultimate #194, repo only) |
| Simpsons: Hit & Run | https://shar-wasm.cjoseph.workers.dev/?skipmovie= | 2021 leak port, WASM+WebGL, Xbox extras, H264 FMVs | WASM + WebGL, on-demand fetch | Live | No |
| Doom 3 | https://wasm.continuation-labs.com/d3demo/ | `web-ports/doom-3` | Emscripten | Demo live | Yes (Ultimate #111) |
| Quake 3 Arena (WebRTC MP) | https://thelongestyard.link/q3a-demo/ | `JWally/web-quaker` (ioquake3 + WebRTC DataChannels) | Emscripten, WebRTC, SW cache 330MB | Live | Partial |
| Unreal Tournament | `dos.zone/mp/?lobby=ut` | dos.zone build | Emscripten | Live | No (as direct link) |
| Counter-Strike 1.6 | `dos.zone/mp/?lobby=cs16` | Xash3D / `yohimik/webxash3d-fwgs`, `Pixelsuft/hl` | Emscripten | Live | Partial (Ultimate #84-86, repo only) |
| Half-Life 1 | https://x8bitrain.github.io/webXash/ | Xash3D FWGS | Emscripten | Live | Partial |
| Diablo 1 | https://devilutionx.app | `d07RiV/diabloweb`, DevilutionX | Emscripten | Live | Partial (Ultimate #104, repo only) |
| Tomb Raider 1 (OpenLara) | http://xproger.info/projects/OpenLara/ | `XProger/OpenLara` | Emscripten + WebGL, async + IndexedDB | Live | No (as OpenLara) |
| Duke Nukem 3D | https://gawen.me/webduke | webduke / `midzer/BelgianChocolateDuke3D` | Emscripten | Live | Partial |
| C&C Generals: Zero Hour | self-host `caiiiycuk/Generals-WebAssembly` | real 2003 engine 500k LOC, D3D8→WebGL2 `d3d8webgl`, OPFS, MQTT WebRTC MP | wasm, Brotli pack, static host | Repo live, self-host | No |
| C&C Red Alert 2 | https://chronodivide.com/ | ChronoDivide | Web | Live | No |
| Morrowind (OpenMW) | https://morrowind.virtastic.app | `Virtastic/openmw-web` (OpenMW → WASM, MP, cloud locker) | wasm64, WebGL2, File System Access, Chrome 133+ | Live | No |
| Jagged Alliance 2 | https://ja2.virtastic.app | `Virtastic/ja2-web` (Stracciatella v0.22.1 → WASM) | AudioWorklet, SIMD blitters, IDBFS | Live | No (Ultimate has JA2 repo via midzer, different port) |
| GunZ: The Duel (2003) | https://gunz.sigr.io/ | `LostMyCode/d3d9-webgl` + full game, server in Worker via postMessage | D3D9→WebGL live, FMOD→WebAudio, Win32 msg bridge | Live | No |
| SCP: Containment Breach | https://q8j-dev.github.io/scpcb-web-port/ | `q8j-dev/scpcb-web-port` via `blitz3d-ng` LLVM → Emscripten | Blitz3D → WebGPU backend | Live | No |
| Arx Fatalis | demo in `gabrielcuvillier/arxwasm` | Arx Libertatis → Emscripten, Regal GL 1.x→GLES2 | WASM + WebGL, 150MB IDBFS | Demo live | No |
| GZDoom / Brutal Doom | https://uzdoom.bootnet.io/ | `abootnet/uzdoom-wasm` (UZDoom), `mungus43/tomb-engine` (GZDoom g4.11.3, JSPI, Worker+OffscreenCanvas) | WebGL2, OpenAL→WebAudio, IDBFS drag-drop | Live | No (Ultimate has Doom via PrBoom only) |
| Heroes of Might and Magic 3 | self-host `caiiiycuk/vcmi-wasm` | VCMI → WASM | Emscripten | Repo | Yes (Ultimate #205, repo only) |
| Daggerfall / other Bethesda | via OpenMW-style ports, UZDoom family | various | — | — | — |
| Touhou Eiyashou (TH08) | self-host TH08 Web (needs `th08.dat`+`thbgm.dat`) | C++ → WASM + WebGL2, Web Audio, local saves/replays | BYO DAT, Chrome rec. | Repo/demo | No |
| Dino Crisis (GOG via WINE) | via `wasm.ltd` PROTON+WINE→WASM | `wasm.ltd` initiative | WASM + Wine | Playable | No |
| Star Wars Jedi Knight: DF2 | via midzer / `quagsire23/OpenJKDF2` | OpenJKDF2 | Emscripten | Varies | Partial |

### Mid-tier / indie ports (MercuryWorkshop, genizy, web-ports families)

Celeste (`MercuryWorkshop/celeste-wasm`), Terraria (`mercuryWorkshop/terraria-wasm`), Stardew Valley (`degloved-net/stardew-wasm`), Sonic Mania/1/2/CD (`VinMannie/*`, `TWS2401/Sonic-CD-WASM`), OpenTTD, OpenXcom (`midzer/*`), Fallout 1-CE (`midzer/fallout1-ce`), Jagged Alliance 2 straw (`midzer`), Quake/Quake2 (`GMH-Code/Qwasm`), Dwasm/PrBoom (`GMH-Code/Dwasm`), webDOOM (`UstymUkhman/webDOOM`), Inscryption (`wasm.rip/files/inscryption`, `reeyuki`), etc. — see `data/games.json` and Ultimate Catalog for full 474.

Full unlisted-only deep dives: see `GAMES_EXTRA.md`.

## List of every list

See `LISTS.md` — 17 catalogs/hubs tracked, including:

- Ultimate-Catalog-Of-Web-Game-Ports (474 games, 206 demos)
- genizy/web-ports, genizy/web-port-list, gn-math
- web-ports org, webport.ing, wasm.rip, Ported2Browser
- midzer.de/games, quenq.com/directory, dos.zone, retrogamescenter.ru
- RetroPlay, webassemblygames.com, sigmonsays HN list, null.53bits list, Open Awesome Emscripten

## How to contribute / scrape new ones

Run `/scrapgames` (see `.opencode/commands/scrapgames.md`). It:

1. Searches web for new `site:github.com wasm web port playable`, `itch.io`, `Hacker News Show HN WASM game`, `Reddit r/WebGames`, etc.
2. Verifies Play URL loads (WebGL2/WebGPU, COOP/COEP, SharedArrayBuffer) + repo builds with Emscripten
3. Checks against `data/games.json` + all lists in `LISTS.md` — only adds truly new
4. Appends to `data/games.json` + `GAMES_EXTRA.md` with proof links

Schema: `data/games.json` entries: `{ title, play_url, repo_url, engine, tech, status, last_verified, in_lists[], needs_own_files, notes }`.

## Legal

Links point to third-party projects. Game data is usually NOT included — bring your own copy. Licenses/terms are defined by respective authors. PlayGTA5-style ports get DMCA'd fast (Take-Two nuked Vice City browser + GTA V Switch homebrew before).
