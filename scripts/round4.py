#!/usr/bin/env python3
"""Round 4 (last): hero art, GOG/itch probes, first-image probes of official
sites. Everything HEAD-verified before caching. Prints LEFTovers at the end.
"""
import json
import re
import urllib.parse
import urllib.request
from fetch_images import http_ok, CACHE

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def get(url, timeout=20, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if r.status >= 400:
            return None
        return r.read() if binary else r.read().decode("utf-8", "replace")


def og_of(page):
    try:
        html = get(page)
    except Exception:
        return None
    if not html:
        return None
    m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)', html)
    if not m:
        return None
    u = urllib.parse.urljoin(page, m.group(1))
    return u if (u.startswith("http") and http_ok(u)) else None


def first_img(page, must_contain=None):
    """First content <img> on a page (skips icons/logos), HEAD-verified."""
    try:
        html = get(page)
    except Exception:
        return None
    if not html:
        return None
    for m in re.finditer(r'<img[^>]*src=["\']([^"\']+)', html):
        u = urllib.parse.urljoin(page, m.group(1))
        low = u.lower()
        if any(k in low for k in ("icon", "logo", "favicon", "sprite", "button",
                                  "avatar", "emoji", ".svg")):
            continue
        if must_contain and must_contain not in low:
            continue
        if http_ok(u):
            return u
    return None


def itch_top(query, title_must):
    """First itch.io search result whose title contains title_must -> og:image."""
    try:
        html = get("https://itch.io/search?q=" + urllib.parse.quote(query))
    except Exception:
        return None
    if not html:
        return None
    for m in re.finditer(r'href="(https://[a-z0-9-]+\.itch\.io/[^"]+)"[^>]*class="title[^"]*"[^>]*>([^<]+)<', html):
        if title_must.lower() in m.group(2).lower():
            return og_of(m.group(1))
    return None


JOBS = [
    ("HERETIC / HEXEN",
     "https://cdn.cloudflare.steamstatic.com/steam/apps/3286930/library_hero.jpg"),
]
WANT = {
    "Unreal Gold": lambda: og_of("https://www.gog.com/game/unreal_gold"),
    "Anarch": lambda: og_of("https://drummyfish.itch.io/anarch"),
    "Rocks'n'Diamonds": lambda: first_img("https://www.artsoft.org/rocksndiamonds/"),
    "xrick": lambda: first_img("https://www.xrick.net/"),
    "Ballerburg SDL": lambda: first_img("https://baller.tuxfamily.org/"),
    "My Femboy Roommate (2)": lambda: itch_top("My Femboy Roommate", "femboy roommate"),
    "Dressing Room": lambda: itch_top("Dressing Room horror", "dressing room"),
    "wasm.rip": lambda: next((u for u in
        ["https://wasm.rip/logo.png", "https://wasm.rip/assets/logo.png",
         "https://wasm.rip/icon.png", "https://wasm.rip/favicon.png"]
        if http_ok(u)), None),
}


def main():
    cache = json.loads(CACHE.read_text())
    for t, u in JOBS:
        if t not in cache and http_ok(u):
            cache[t] = {"pic": u}
            print(f"fixed {t!r}")
    for t, fn in WANT.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        try:
            u = fn()
        except Exception as e:
            print(f"ERR {t!r}: {str(e)[:60]}")
            u = None
        if u:
            cache[t] = {"pic": u}
            print(f"found {t!r} -> {u[:80]}")
        else:
            print(f"LEFT {t!r}")
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    print("cached total:", len(cache))


if __name__ == "__main__":
    main()
