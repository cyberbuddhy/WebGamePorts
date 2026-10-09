# List of Every List

All known catalogs/hubs tracking WebAssembly browser game ports. `/scrapgames` must check all of these before claiming a game is "not in any list".

| # | List | URL | Count / scope | Type | Last checked |
|---|---|---|---|---|---|
| 1 | Ultimate Catalog of Web Game Ports | https://github.com/Carter54git/Ultimate-Catalog-Of-Web-Game-Ports | 474 games, 206 demos, 372 repos | WASM (Emscripten/SDL) + Unity WebGL + Godot + Ruffle + JS | 2026-10-09 |
| 2 | genizy/web-ports | https://github.com/genizy/web-ports | 100+ real-deal ports (not remakes) | WASM, gn-math hosted | 2026-10-09 |
| 3 | genizy/web-port-list | https://github.com/genizy/web-port-list | full list + credits (breadbb etc) | WASM | 2026-10-09 |
| 4 | web-ports org | https://github.com/web-ports (e.g. `/20-minutes`, `/doom-3`, `/antonblast`, `/celeste`) | dozens, per-game repos | WASM | 2026-10-09 |
| 5 | midzer.de/games + midzer github | https://midzer.de/games + https://github.com/midzer (abuse, astromenace, cdogs-sdl, fheroes2, OpenXcom, OpenClaw, fallout1-ce, dxx-rebirth, etc) | 60+ Emscripten ports | Emscripten, Open Source Game Clones discoveries | 2026-10-09 |
| 6 | wasm.rip collective | https://wasm.rip/ — members: shayder crackers cirsius NotRexed q8j sexyplankton sunsuke gurtmuncher reeyuki slqnt zxs dasher crax TS x8r | Inscryption, man-from-window-2, etc. | WASM | 2026-10-09 |
| 7 | webport.ing | https://webport.ing/ — team of 4, `webporting/*` (e.g. Your-Only-Move-Is-HUSTLE) | indie ports | WASM | 2026-10-09 |
| 8 | quenq.com directory | https://quenq.com/directory/ + https://quenq.com/apps/vice-city/ | Simpsons H&R, Vice City, etc. | WASM/WebGL | 2026-10-09 |
| 9 | dos.zone + Game Studio | https://dos.zone + `dos.zone/mp/?lobby=ut` `?lobby=cs16` | 2000+ DOS (js-dos = DOSBox→WASM) + UT/CS lobbies | DOSBox-WASM | 2026-10-09 |
| 10 | retrogamescenter.ru ports | https://retrogamescenter.ru/ports/* (ac-webport, cavestory, descentweb, truedoom, duke3dtg, ftldemo...) | Russian hub, many TG builds | WASM | 2026-10-09 |
| 11 | gn-math.dev / gn-math.github.io | https://gn-math.dev/?id=... + https://gn-math.github.io/web-port/* | school-unblocked host for genizy ports | WASM | 2026-10-09 |
| 12 | RetroPlay hub | https://github.com/MahanKenway/RetroPlay — Doom/Freedoom, C-Dogs SDL, FreeDink, OpenTyrian, LibreQuake, OpenTTD, FreeRCT, Neverball, ECWolf | curated, GitHub Pages + Actions + Emscripten | WASM | 2026-10-09 |
| 13 | webassemblygames.com | https://www.webassemblygames.com/ — Angry Bots, BananaBread, Funky Karts, Zombs Royale | curated WASM games + dev resources | Unity/WebGL/WASM | 2026-10-09 |
| 14 | sigmonsays browser-games (HN thread) | https://sigmonsays.github.io/browser-games.html — Q3, UT, Vice City, CS, HL1/HL2, Doom3, Diablo, Tomb Raider, Duke, RA2 | HN-sourced big-title list | various WASM | 2026-10-09 |
| 15 | null.53bits In-Browser Game Ports | https://null.53bits.co.uk/page/in-browser-game-ports — CS1.6, Doom3, Duke3D, Vice City, HL1/HL2, Q3, RA2, Simpsons H&R, UT | editorial list | various | 2026-10-09 |
| 16 | Ported2Browser | https://ported2browser.com/ports/... (e.g. Inscryption by reeyuki, hosted by wasm.rip) | hosted browser builds index | WASM | 2026-10-09 |
| 17 | Open Awesome Emscripten | https://open-awesome.com/stacks/emscripten — wipeout-rewrite, BananaBread, etc. | open-source built with Emscripten | Emscripten | 2026-10-09 |
| 18 | DOS / abandonware browser sites | https://bestdosgames.com/ https://dosgamesarchive.com/ https://archive.org/details/softwarelibrary_msdos_games https://www.myabandonware.com/ etc. | 1000s DOS playable via DOSBox-WASM | DOSBox-WASM | 2026-10-09 |
| 19 | wasm.ltd preservation initiative | https://revc.wasm.ltd (origami-ltd/wasm-revc) — Vice City + Dino Crisis via PROTON+WINE→WASM | preservation, BYO files, shared streaming layer | WASM + WebGPU/WebGL2 | 2026-10-09 |

## How lists overlap

- Ultimate #1 ingests #2 #3 #4 #5 #6 #7 #11 — but lags 2026 big ports (GTA V, HL2 repo, Simpsons H&R direct link, GunZ, Generals, OpenMW, JA2-web, web-quaker, scpcb-web-port, arxwasm, uzdoom/gzdoom-wasm).
- #14 #15 are the only editorial lists that already include HL2 + Simpsons H&R + RA2 + UT as direct links — use them as seed for `/scrapgames`.
- #18 is DOSBox-WASM, not native-engine WASM — track separately (different tech).
- #19 is newest (preservation-first, shared base: streaming asset layer + sync worker + SAB file bridge).

Add new lists via PR updating this file + `data/games.json` `in_lists[]`.
