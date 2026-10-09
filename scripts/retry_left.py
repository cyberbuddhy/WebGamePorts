#!/usr/bin/env python3
"""Final targeted retry for titles still missing after fill_gaps.py.

- Steam match with word-sequence containment (catches 'FTL: Faster Than
  Light', 'Duke Nukem 3D: 20th Anniversary...', ...), min 10 chars.
- Extra aliases for known store games.
- Verifies every capsule with HEAD before caching.
"""
import json
import time
import urllib.parse
from fetch_images import norm, http_json, http_ok, CDN, CACHE, ALLGAMES, INDEX, rest_titles
from fill_gaps import ALIASES as BASE_ALIASES, clean_queries

EXTRA_ALIASES = {
    "Faster Than Light: Demo": ["FTL"],
    "Duke Nukem 3D TG": ["Duke Nukem 3D"],
    "Quake TG": ["Quake"],
    "DOOM I & II": ["DOOM", "DOOM II"],
    "DUNE II TG": ["Dune II"],
    "Wolfenstein 3D TG": ["Wolfenstein 3D"],
    "NAM / Napalm": ["NAM"],
    "WWII GI": ["WWII GI"],
    "Counter Strike & Half Life": ["Counter-Strike", "Half-Life"],
    "Unreal Gold": ["Unreal"],
    "Descent": ["Descent"],
    "Space Rangers: Quests": ["Space Rangers"],
    "Super Monkey Ball": ["Super Monkey Ball"],
    "Granny (2)": ["Granny"],
    "Gorilla Tag (2)": ["Gorilla Tag"],
    "Rec Room": ["Rec Room"],
    "Ballerburg SDL": ["Ballerburg"],
    "Rocks'n'Diamonds": ["Rocks'n'Diamonds"],
    "xrick": ["xrick"],
    "Taiko no Tatsujin": ["Taiko no Tatsujin"],
}

STEAM_SEARCH = "https://store.steampowered.com/api/storesearch/?term={q}&l=en&cc=US"


def words(t):
    return norm(t).split()


def contains(a, b):
    """True if word-seq a appears in order inside word-seq b."""
    n, m = len(a), len(b)
    return n and any(a == b[i:i + n] for i in range(m - n + 1))


def steam_relaxed(title):
    queries = list(clean_queries(title)) + EXTRA_ALIASES.get(title, [])
    for q in dict.fromkeys(queries):
        try:
            data = http_json(STEAM_SEARCH.format(q=urllib.parse.quote(q)))
        except Exception:
            continue
        want = words(title)
        cands = []
        for item in data.get("items", []) or []:
            if item.get("type") != "app":
                continue
            name = words(str(item.get("name", "")))
            if not name or not want:
                continue
            if name == want:
                score = 1.0
            elif (len(" ".join(want)) >= 10 and contains(want, name)) or \
                 (len(" ".join(name)) >= 10 and contains(name, want)):
                score = 0.95
            else:
                import difflib
                score = difflib.SequenceMatcher(None, " ".join(name),
                                               " ".join(want)).ratio()
                if score < 0.92:
                    continue
            cands.append((score, item))
        if not cands:
            time.sleep(0.3)
            continue
        cands.sort(reverse=True, key=lambda x: x[0])
        appid = cands[0][1]["id"]
        if http_ok(f"{CDN}{appid}/capsule_616x353.jpg"):
            return appid, False
        if http_ok(f"{CDN}{appid}/header.jpg"):
            return appid, True
        time.sleep(0.3)
    return None


def main():
    cache = json.loads(CACHE.read_text())
    games = {g["title"]: g for g in json.loads(ALLGAMES.read_text())["games"]}
    html = INDEX.read_text()
    titles = dict.fromkeys(list(games) + [json.loads(f'"{r}"') for r in rest_titles(html)])
    todo = [t for t in titles if t not in cache]
    print(f"{len(todo)} left, retrying with relaxed rules")
    for i, t in enumerate(todo):
        hit = steam_relaxed(t)
        if hit:
            appid, hdr = hit
            cache[t] = {"img": appid} | ({"h": 1} if hdr else {})
            print(f"[{i+1}/{len(todo)}] steam {t!r} -> {appid}")
            if len(cache) % 5 == 0:
                CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
        else:
            print(f"[{i+1}/{len(todo)}] still none {t!r}")
        time.sleep(0.3)
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    missing = [t for t in titles if t not in cache]
    print(f"\nleft: {len(missing)}")
    for t in missing:
        print(f"  LEFT: {t}")


if __name__ == "__main__":
    main()
