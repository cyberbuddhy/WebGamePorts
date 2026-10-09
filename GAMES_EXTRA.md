# Games NOT In Any List

Verified 2026-10-09. Each entry was checked against ALL lists in `LISTS.md` (esp. Ultimate 474). "Not in any list" = no exact Play URL + repo combo found in those lists.

## 1. GTA V — playgta5.com (wasm64 + WebGPU, RAGE)

- Play: `https://playgta5.com` (offline Oct 6-8 2026, Cloudflare 1014 → food ad), mirror via `web.archive.org/web/20261006055917/https://playgta5.com/`, frontend archived `shadany7824/playgta5`
- Tech: `game.wasm` 63,201,802 bytes, ~91k funcs with names, wasm64 + 75 threads + shared memory, D3D11 → 48-opcode 32MB ring → `wgpu_worker.js` → WebGPU, 4,919 DXBC → 4,808 WGSL (72MB, 18 packs), `io_worker.js` HTTP Range + disk store, AudioWorklet, 20.9GB `data/**`, bootset 582MB / 2,918 files
- Needs: streaming assets (700MB boot), 3-16GB RAM, Chromium + WebGPU
- Proof: videocardz 2026-10-06, Tom's Hardware 2026-10-07, Gizmodo 2026-10-06, thesatyajit reverse-engineering writeup
- In lists? No. Ultimate has GTA 3 / Vice City repo-only stubs, no GTA V entry.

## 2. Half-Life 2 full campaign — hl2.slqnt.dev

- Play: https://hl2.slqnt.dev
- Source base: `weliveinhell` Portal webport (itself fork of `nillerusr` Source leak with ToGLES) → slqnt + 98006, 3 months, released 2026-06-24
- Tech: Source → Emscripten, ToGLES (GLES) → WebGL2, VPKs unpacked → per-map `.data` chunks streamed, IDBFS saves, Source console, 100+ FPS on desktop, mobile limited
- Issues: no eye shaders, no Bink video, needs `steam_legacy` assets
- In lists? Partial: Ultimate #196 has demo link only, no repo. Not in genizy/midzer/wasm.rip. Editorial lists (#14 #15) link it.

## 3. The Simpsons: Hit & Run — WASM/WebGL

- Play: https://shar-wasm.cjoseph.workers.dev/?skipmovie=
- Source: 2021 PC leak → full PC→WASM+WebGL port, native res, on-demand fetch, Xbox lens flares/widescreen/Frink refraction, FMVs → H264 MP4 `<video>` overlay. Runs on Pixel 10, Firefox macOS stuttery.
- Proof: Hacker News `item?id=47783061`, ScreenRant 2026-09-08, quenq directory
- In lists? No (Ultimate has no SHAR entry; only editorial #15 mentions it).

## 4. GunZ: The Duel (2003) — gunz.sigr.io

- Play: https://gunz.sigr.io/
- Source: `LostMyCode/d3d9-webgl` translation layer, original C++ untouched, server also compiled to WASM + Worker + `postMessage`, SQLite+IDBFS saves, FMOD→WebAudio (1260 lines, PannerNode), browser→Win32 (`WM_KEYDOWN` etc), Pointer Lock, `.mrs` streaming + Cache API, <10s boot
- Author writeups: dev.to `whiplash` 2026-03-11 / 2026-06-21, Claude + Antigravity AI-assisted
- In lists? No.

## 5. C&C Generals: Zero Hour — real 2003 engine in browser

- Repo: https://github.com/caiiiycuk/Generals-WebAssembly
- Tech: ~500k LOC C++ → Emscripten, custom `d3d8webgl` D3D8-fixed-function → WebGL2, OPFS permanent cache (IDBFS fallback), `GAXD` 64MB Brotli-parallel pack (`brotli-wasm` worker, ~130MB peak), static host + SW-injected COOP/COEP, MQTT-over-WS signaling + WebRTC mesh MP, Go server optional
- Build: `cmake --preset emscripten`, `scripts/web/pack-assets.sh`, BYO `*.big`
- In lists? No (Ultimate has C&C via Vanilla-Conquer, different game).

## 6. Morrowind — OpenMW Web

- Play: https://morrowind.virtastic.app
- Repo: https://github.com/Virtastic/openmw-web
- Tech: OpenMW → WASM, client-side, BYO `Data Files` (File System Access, nothing uploaded), example world included, MP (1.1.0, up to 32, experimental), admin dashboard (1.2.0), Chrome/Edge 133+ MEMORY64 + SAB + threads + WebGL2 + `EXT_clip_control`
- In lists? No.

## 7. Jagged Alliance 2 — JA2 Stracciatella Web

- Play: https://ja2.virtastic.app
- Repo: https://github.com/Virtastic/ja2-web (tracks Stracciatella v0.22.1 + `__EMSCRIPTEN__` patches: threading/main-loop, AudioWorklet, SIMD blitters, IDBFS, FS Access)
- Build: Emscripten 6.0.1 + Rust nightly pin, `-fexceptions -pthread -msimd128`, 8MB stack, nginx COOP/COEP, desktop Chrome only
- In lists? No (Ultimate has `midzer` JA2-adjacent, different port).

## 8. Vice City reVC Web (wasm.ltd preservation base)

- Play: https://revc.wasm.ltd
- Repo: https://github.com/origami-ltd/wasm-revc (part of wasm.com.br / wasm.ltd initiative: shared streaming asset layer + sync worker + SAB file bridge + page shell)
- Tech: reVC decomp → Emscripten, WebGL2, streaming archives (no repack), BYO install, IndexedDB saves, Gamepad API. Same base also runs Dino Crisis (GOG) via PROTON+WINE→WASM.
- In lists? Partial: Ultimate #194 is `Lolendor/reVCDOS` (DOS), not this Web+WebGPU BYO-disk port.

## 9. Quake 3 WebRTC multiplayer — web-quaker

- Repo: https://github.com/JWally/web-quaker (ioquake3 → Emscripten, `NA_WEBRTC`, `webrtc.js` + REST signaling + 4-char room codes, SW cache ~330MB pk3s, 60+ maps, host-is-server P2P)
- In lists? Partial: Ultimate has Quake 3 single-player demos, not this WebRTC MP fork.

## 10. SCP: Containment Breach — Blitz3D → WebGPU

- Play: https://q8j-dev.github.io/scpcb-web-port/
- Repo: https://github.com/q8j-dev/scpcb-web-port via `blitz3d-ng` LLVM → Emscripten, custom `graphics.webgpu` backend, unmodified `.bb` source, menus/saves/audio/subtitles work
- In lists? No.

## 11. Arx Fatalis — arxwasm

- Repo: https://github.com/gabrielcuvillier/arxwasm (Arx Libertatis → Emscripten, Regal GL 1.x→GLES2, demo data auto-fetch, 150MB IDBFS, Firefox/Chrome/Safari/Edge desktop playable, mobile loads but unplayable)
- In lists? No.

## 12. GZDoom / UZDoom modern Doom mods in browser

- Play: https://uzdoom.bootnet.io/ (UZDoom, Freedoom bundled, drag-drop IWAD/PK3, IDBFS)
- Repos: https://github.com/abootnet/uzdoom-wasm (GLES2/WebGL2, OpenAL+ZMusic, pthreads, IDBFS) + https://github.com/mungus43/tomb-engine (GZDoom g4.11.3, Worker+OffscreenCanvas, JSPI not Asyncify: -37% size, +25% FPS, Brutal Doom v22 159MB loads)
- In lists? No (Ultimate has PrBoom/chocolate-doom only, no GZDoom-family).

## 13. Touhou Eiyashou (TH08) Web

- Needs: own `th08.dat` + `thbgm.dat`, desktop Chrome rec., Firefox separate build
- Tech: refactored C++ → WASM + WebGL2, Web Audio BGM on-demand, local saves/replays, MIT code (not assets)
- In lists? No.

## 14. OpenLara (Tomb Raider) WebGL build

- Play: http://xproger.info/projects/OpenLara/
- Repo: https://github.com/XProger/OpenLara — C++ → Emscripten → WASM + WebGL1/2, IndexedDB cache, Gamepad API, Browse-Level `.PHD/.PSX/.TR2/.TR4`
- In lists? No as OpenLara (Ultimate has Tomb Raider via other means in editorial #14 only).

## 15. DevilutionX / Tomb-Engine extras / ChronoDivide

- https://devilutionx.app (Diablo, Ultimate repo-only) — include here because Play URL missing in Ultimate
- https://chronodivide.com/ (RA2, missing in Ultimate)
- https://gawen.me/webduke (Duke3D Web, Ultimate repo-only)
- https://eikehein.com/stuff/sabatu (Tomb Raider, editorial-only)

---

Add new finds with: Play URL (verified live), repo URL, tech (engine → WASM path, renderer translation, FS/audio/input), needs-own-files?, proof links (HN/Reddit/news), `in_lists: []` check output.
