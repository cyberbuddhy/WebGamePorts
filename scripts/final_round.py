#!/usr/bin/env python3
"""Final round: gn-math catalog covers, slow Steam re-check, Wikipedia
pageimages, same-franchise pins (all HEAD/API-verified, dropped on failure),
and og rescrapes. Updates data/images.json for still-missing titles only.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from fetch_images import norm, http_json, http_ok, steam_match, CDN, CACHE, ALLGAMES, INDEX, rest_titles
from fill_gaps import og_image, clean_queries

GN_COVER = ("https://gn-math.dev/s/EE0_FEFXflkxUx5iECccXCcNRB9_"
            "GDdDXysSex5LLgFQGDgFPFIDP1U3F08uFkEtPBc7WV8/{n}.png")
WIKI = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
        "&format=json&pithumbsize=616&titles={t}")
STEAM_SEARCH = "https://store.steampowered.com/api/storesearch/?term={q}&l=en&cc=US"

SLOW_STEAM = {  # title -> queries (verified, containment-or-better)
    "Rec Room": ["Rec Room"],
    "Worldbox": ["WorldBox"],
    "HERETIC / HEXEN": ["Heretic + Hexen", "Heretic", "Hexen"],
    "Unreal Gold": ["Unreal Gold", "Unreal"],
    "Duke Nukem 3D TG": ["Duke Nukem 3D"],
    "DUNE II TG": ["Dune II"],
    "WWII GI": ["WWII GI"],
    "NBlood": ["Blood"],
    "Descent": ["Descent"],
    "Rocks'n'Diamonds": ["Rocks'n'Diamonds"],
    "xrick": ["xrick"],
    "Ballerburg SDL": ["Ballerburg"],
    "Quake TG": ["Quake"],
    "Wolfenstein 3D TG": ["Wolfenstein 3D"],
    "NAM / Napalm": ["NAM"],
    "Minecraft Story Mode": ["Minecraft Story Mode"],
    "Minecraft Pocket Edition": ["Minecraft"],
    "Minecraft 0.6.1": ["Minecraft"],
    "Minecraft LCE": ["Minecraft"],
    "Super Mario 64": ["Super Mario"],
    "Bad Piggies": ["Bad Piggies"],
    "Duck Life 8": ["Duck Life"],
    "Slender: The 8 Pages": ["Slender"],
    "Jumbo Mario": ["Mario"],
    "Sonic.EXE (ORIGINAL)": ["Sonic"],
    "My Talking Baby Hippo": ["My Talking Tom"],
}
# title -> certain steam appid (same game / same franchise fangame)
FRANCHISE_PINS = {
    "Quake TG": 2310,                      # Quake, same game
    "Duke Nukem 3D TG": 434050,            # Duke 3D, same game
    "GTA V": 271590,                       # same game (repo gone)
    "GZDoom / Brutal Doom in browser": 2280,  # DOOM engine port
    "Five Nights at Candy's": 319510,      # FNAF fangame
    "Five Nights at Last Breath": 319510,  # FNAF fangame
    "The Man In The Window": 319510,       # FNAF fangame
    "Raldi's Crackhouse": 319510,          # FNAF fangame
    "Slendytubbies 1": 252330,             # Slender fangame (The Arrival)
    "Gabriel's Awesome Schoolhouse (GASH)": 1275890,  # Baldi fangame (BB+)
    "CaseOh's Basics in Eating and Fast Food": 1275890,  # Baldi-like
}
# title -> wikipedia article for cover art
WIKI_TITLES = {
    "Animal Crossing (GAMECUBE)": "Animal Crossing (video game)",
    "Minecraft Story Mode": "Minecraft: Story Mode",
    "Bad Piggies": "Bad Piggies",
    "Slender: The 8 Pages": "Slender: The Eight Pages",
    "Eaglercraft": None,
}


def wiki_cover(article):
    try:
        data = http_json(WIKI.format(t=urllib.parse.quote(article)))
    except Exception:
        return None
    for page in (data.get("query", {}).get("pages", {}) or {}).values():
        thumb = (page.get("thumbnail") or {}).get("source")
        if thumb and "disambiguation" not in str(page.get("pageprops", "")):
            return thumb if http_ok(thumb) else None
    return None


def steam_verified(appid):
    if http_ok(f"{CDN}{appid}/capsule_616x353.jpg"):
        return {"img": appid}
    if http_ok(f"{CDN}{appid}/header.jpg"):
        return {"img": appid, "h": 1}
    return None


def main():
    games = {g["title"]: g for g in json.loads(ALLGAMES.read_text())["games"]}
    cache = json.loads(CACHE.read_text())
    html = INDEX.read_text()
    titles = dict.fromkeys(list(games) + [json.loads(f'"{r}"') for r in rest_titles(html)])
    todo = [t for t in titles if t not in cache]
    print(f"{len(todo)} left")

    def save():
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")

    for i, t in enumerate(todo):
        tag = f"[{i+1}/{len(todo)}]"
        g = games.get(t, {})
        entry = None
        # 1. gn-math catalog cover (?id=N)
        m = re.search(r"gn-math\.dev/\?id=(\d+)", g.get("play_url") or "")
        if m:
            u = GN_COVER.format(n=m.group(1))
            if http_ok(u):
                entry = {"pic": u}
                print(f"{tag} gnmath {t!r}")
        # 2. franchise pins
        if entry is None and t in FRANCHISE_PINS:
            entry = steam_verified(FRANCHISE_PINS[t])
            print(f"{tag} franchise {t!r} -> {'OK' if entry else 'FAIL'}")
        # 3. slow steam re-check
        if entry is None and t in SLOW_STEAM:
            for q in SLOW_STEAM[t]:
                hit = steam_match(q)
                if hit:
                    appid, hdr = hit
                    entry = {"img": appid} | ({"h": 1} if hdr else {})
                    print(f"{tag} steam {t!r} -> {appid} via {q!r}")
                    break
                time.sleep(1.2)
            else:
                print(f"{tag} steam-miss {t!r}")
        # 4. wikipedia cover
        if entry is None and t in WIKI_TITLES and WIKI_TITLES[t]:
            pic = wiki_cover(WIKI_TITLES[t])
            if pic:
                entry = {"pic": pic}
                print(f"{tag} wiki {t!r}")
            else:
                print(f"{tag} wiki-miss {t!r}")
        # 5. og rescrape (play, then repo)
        if entry is None:
            for u in (g.get("play_url"), g.get("repo_url")):
                im = og_image(u)
                if im:
                    entry = {"pic": im}
                    print(f"{tag} ogscrape {t!r} -> {im[:70]}")
                    break
                time.sleep(0.5)
        if entry is None:
            print(f"{tag} LEFT {t!r}")
        else:
            cache[t] = entry
            save()
        time.sleep(0.3)
    missing = [t for t in titles if t not in cache]
    print(f"\nleft: {len(missing)}")
    for t in missing:
        print(f"  LEFT: {t}")


if __name__ == "__main__":
    main()
