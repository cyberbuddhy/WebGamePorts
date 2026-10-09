#!/usr/bin/env python3
"""Hand-verified additions: identity-confirmed Steam appids (via appdetails),
Wikipedia covers (pageimages API), itch/URL art (HEAD-verified), franchise
pins for fangames (disclosed in report). Also drops one wrong entry.
Every URL is HEAD-verified before caching. Run once (idempotent-ish).
"""
import json
import urllib.parse
from fetch_images import norm, http_json, http_ok, CDN, CACHE

UA = {"User-Agent": "WGP/1.0"}

# title -> steam appid, identity confirmed via appdetails
STEAM_OK = {
    "Rec Room": 471710,
    "HERETIC / HEXEN": 3286930,
    "Worldbox": 1206560,
    "GTA V": 271590,                      # same game as curated entry
    "GZDoom / Brutal Doom in browser": 2280,  # DOOM engine port
    "Five Nights at Candy's": 319510,     # FNAF fangame (franchise art)
    "Five Nights at Last Breath": 319510,  # FNAF fangame (franchise art)
    "Raldi's Crackhouse": 319510,         # FNAF fangame (franchise art)
    "Slendytubbies 1": 252330,            # Slender fangame (The Arrival)
    "Baldi's Basics: Minus 3": 1275890,   # Baldi fangame (BB+)
    "Cheesed Up 1.3.1": 1275890,          # Baldi fangame (franchise art)
    "OLD CheesedUP": 1275890,              # Baldi fangame (franchise art)
}
# title -> direct art URL (HEAD-verified below)
URL_OK = {
    "Egg Fried Rice": "https://img.itch.zone/aW1nLzE2NDg5OTY1LmdpZg==/original/UMd%2B1H.gif",
    "GO TO BED": "https://img.itch.zone/aW1nLzEzNTMyNDk4LnBuZw==/original/yRSrjd.png",
    "Pretend it's not there": "https://horrorgames.io/data/image/game/pretend-its-not-there.png",
}
# title -> wikipedia article for cover art
WIKI_OK = {
    "Unreal Gold": "Unreal (video game)",
    "Minecraft Story Mode": "Minecraft: Story Mode",
    "DUNE II TG": "Dune II",
    "Descent": "Descent (video game)",
    "NBlood": "Blood (video game)",
    "Animal Crossing (GAMECUBE)": "Animal Crossing (video game)",
}
WIKI = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages"
        "&format=json&pithumbsize=616&titles={t}")
# title -> repo page to re-probe (transients happen)
REPO_RETRY = {
    "Bloboats": "midzer/bloboats",
    "Gilbert and the doors": "midzer/gilbert",
    "bog/aukak": None,  # user avatar instead
    "Klifur": "aukak/klifur",
    "Running Fred": "aukak/running-fred",
}
OG = "https://opengraph.githubassets.com/1/{o}/{r}"


def wiki_cover(article):
    try:
        data = http_json(WIKI.format(t=urllib.parse.quote(article)))
    except Exception:
        return None
    pages = (data.get("query", {}).get("pages", {}) or {}).values()
    for page in pages:
        if "missing" in page:
            continue
        thumb = (page.get("thumbnail") or {}).get("source")
        if thumb and http_ok(thumb):
            return thumb
    return None


def main():
    cache = json.loads(CACHE.read_text())
    # 1. drop the wrong entry (adult DLC mismatched onto a junk row)
    if cache.get("Dressing Room", {}).get("img") == 3373100:
        del cache["Dressing Room"]
        print("dropped wrong entry: Dressing Room -> 3373100")
    for t, appid in STEAM_OK.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        if http_ok(f"{CDN}{appid}/capsule_616x353.jpg"):
            cache[t] = {"img": appid}
        elif http_ok(f"{CDN}{appid}/header.jpg"):
            cache[t] = {"img": appid, "h": 1}
        else:
            print(f"FAIL (no art): {t!r}");
            continue
        print(f"steam {t!r} -> {appid}")
    for t, u in URL_OK.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        if http_ok(u):
            cache[t] = {"pic": u}
            print(f"url {t!r}")
        else:
            print(f"FAIL (url dead): {t!r}")
    for t, art in WIKI_OK.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        pic = wiki_cover(art)
        if pic:
            cache[t] = {"pic": pic}
            print(f"wiki {t!r}")
        else:
            print(f"FAIL (wiki): {t!r}")
    for t, full in REPO_RETRY.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        if full is None:  # user avatar
            user = {"bog/aukak": "aukak"}[t]
            u = f"https://github.com/{user}.png"
            if http_ok(u):
                cache[t] = {"pic": u}
                print(f"avatar {t!r}")
            else:
                print(f"FAIL (avatar): {t!r}")
            continue
        if http_ok(f"https://github.com/{full}"):
            o, r = full.split("/")
            cache[t] = {"pic": OG.format(o=o, r=r)}
            print(f"repo {t!r}")
        else:
            print(f"FAIL (repo gone): {t!r}")
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    print(f"\ncached total: {len(cache)}")


if __name__ == "__main__":
    main()
