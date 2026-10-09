# WebGamePorts

Play full PC games in your browser. No installs, no streaming — click a link and play.

🌐 **Prefer a webpage?** Open `index.html` in this repo — same games with pictures, search, sort and filters.

## How to play

1. Open a **Play** link below in Chrome or Edge.
2. Click the game once to lock the mouse.
3. If a game asks for files, use your own copy of the game.

That's it. Saves stay in your browser.

## All games — most popular first

| # | Game | Play | Source |
|---|---|---|---|
| 1 | GTA V | offline (archived copy: `shadany7824/playgta5`) | frontend archive on GitHub |
| 2 | Half-Life 2 + Episodes | https://hl2.slqnt.dev | slqnt + 98006 |
| 3 | GTA: Vice City | https://revc.wasm.ltd, https://quenq.com/apps/vice-city/ | `origami-ltd/wasm-revc` |
| 4 | Portal | via `weliveinhell` portal webport | `weliveinhell` / `nillerusr` |
| 5 | The Simpsons: Hit & Run | https://shar-wasm.cjoseph.workers.dev/?skipmovie= | community port (see HN) |
| 6 | Counter-Strike 1.6 | `dos.zone/mp/?lobby=cs16` | Xash3D (`yohimik/webxash3d-fwgs`) |
| 7 | Half-Life 1 | https://x8bitrain.github.io/webXash/ | Xash3D FWGS |
| 8 | Doom 3 | https://wasm.continuation-labs.com/d3demo/ | `web-ports/doom-3` |
| 9 | Quake 3 Arena | https://thelongestyard.link/q3a-demo/ | `JWally/web-quaker` (multiplayer fork) |
| 10 | Unreal Tournament | `dos.zone/mp/?lobby=ut` | dos.zone build |
| 11 | Morrowind | https://morrowind.virtastic.app | `Virtastic/openmw-web` |
| 12 | Diablo 1 | https://devilutionx.app | DevilutionX (`d07RiV/diabloweb`) |
| 13 | Tomb Raider 1 | http://xproger.info/projects/OpenLara/ | `XProger/OpenLara` |
| 14 | Duke Nukem 3D | https://gawen.me/webduke | webduke |
| 15 | C&C Generals: Zero Hour | self-host | `caiiiycuk/Generals-WebAssembly` |
| 16 | C&C Red Alert 2 | https://chronodivide.com/ | ChronoDivide |
| 17 | SCP: Containment Breach | https://q8j-dev.github.io/scpcb-web-port/ | `q8j-dev/scpcb-web-port` |
| 18 | Doom mods (Brutal Doom etc.) | https://uzdoom.bootnet.io/ | `abootnet/uzdoom-wasm` |
| 19 | Heroes of Might and Magic 3 | self-host | `caiiiycuk/vcmi-wasm` |
| 20 | Star Wars Jedi Knight: Dark Forces 2 | self-host | `quagsire23/OpenJKDF2` |
| 21 | Jagged Alliance 2 | https://ja2.virtastic.app | `Virtastic/ja2-web` |
| 22 | GunZ: The Duel | https://gunz.sigr.io/ | community port |
| 23 | Arx Fatalis | demo in repo | `gabrielcuvillier/arxwasm` |
| 24 | Touhou Eiyashou (TH08) | self-host (needs your `th08.dat`) | community port |
| 25 | Dino Crisis (GOG) | via `wasm.ltd` | `wasm.ltd` initiative |
| 26 | Terraria | self-host | `mercuryWorkshop/terraria-wasm` |
| 27 | Stardew Valley | self-host | `degloved-net/stardew-wasm` |
| 28 | Celeste | self-host | `MercuryWorkshop/celeste-wasm` |
| 29 | Fallout 1 | self-host | `midzer/fallout1-ce` |
| 30 | Sonic Mania / 1 / 2 / CD | self-host | `VinMannie/*`, `TWS2401/Sonic-CD-WASM` |
| 31 | OpenTTD | self-host | `midzer` / OpenTTD |
| 32 | Inscryption | `wasm.rip/files/inscryption` | `reeyuki` |
| 33 | Quake 1 / 2 | self-host | `GMH-Code/Qwasm` |
| 34 | Doom 1 / 2 | https://playdoom.ossy.dev/ | `GMH-Code/Dwasm`, `UstymUkhman/webDOOM` |
| 35 | OpenXcom | self-host | `midzer/OpenXcom` |

Notes and extra details on the hard-to-find ones: see `GAMES_EXTRA.md`.

## Game lists

Other sites that track browser ports (same simplified list as on the webpage):

- [Ultimate Catalog (474 games)](https://github.com/Carter54git/Ultimate-Catalog-Of-Web-Game-Ports) — biggest catalog, 206 playable
- [genizy/web-ports](https://github.com/genizy/web-ports) — 100+ full-game ports
- [web-ports org](https://github.com/web-ports) — one repo per game
- [midzer.de/games](https://midzer.de/games) — 60+ Emscripten ports
- [wasm.rip](https://wasm.rip/) — porting collective
- [webport.ing](https://webport.ing/) — indie port team
- [quenq directory](https://quenq.com/directory/) — Vice City, Simpsons…
- [dos.zone](https://dos.zone) — 2000+ DOS games in browser
- [gn-math](https://gn-math.dev/) — school-friendly ports host
- [retrogamescenter.ru](https://retrogamescenter.ru/) — Russian ports hub
- [RetroPlay](https://github.com/MahanKenway/RetroPlay) — curated retro hub
- [webassemblygames.com](https://www.webassemblygames.com/) — WASM games + dev guides
- [Browser-games HN list](https://sigmonsays.github.io/browser-games.html) — big-title list
- [null.53bits ports](https://null.53bits.co.uk/page/in-browser-game-ports) — editorial list
- [Ported2Browser](https://ported2browser.com/) — hosted builds index
- [Open Awesome Emscripten](https://open-awesome.com/stacks/emscripten) — open-source builds
- [wasm.ltd](https://revc.wasm.ltd) — preservation ports
- [DOS abandonware hubs](https://archive.org/details/softwarelibrary_msdos_games) — 1000s via Internet Archive
- [genizy/web-port-list](https://github.com/genizy/web-port-list) — full list + credits

## Add a game

1. Run `/scrapgames` (it finds and checks new ports for you).
2. Or add a row to the table above + an entry in `data/games.json`.
3. Run `python3 scripts/validate.py` — it must print OK.

## Note

Links point to other people's projects. Most games need you to own the game — files are not included here.
