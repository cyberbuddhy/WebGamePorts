#!/usr/bin/env python3
"""Round 5 (last): source-port repo pins (HEAD-verified), midzer page probes,
itch probes, one Play-Store probe. Updates data/images.json. Prints LEFTovers.
"""
import re
import urllib.parse
import urllib.request
from fetch_images import http_ok, CACHE
from round4 import og_of, get
import json

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
OG = "https://opengraph.githubassets.com/1/{o}/{r}"

REPO_PINS = {  # title -> owner/repo (the actual engine project)
    "NBlood": "nblood/nblood",
    "DUNE II TG": "OpenDUNE/OpenDUNE",
    "Descent": "dxx-rebirth/dxx-rebirth",
}


def itch_top(query, title_must):
    try:
        html = get("https://itch.io/search?q=" + urllib.parse.quote(query))
    except Exception:
        return None
    if not html:
        return None
    for m in re.finditer(
            r'href="(https://[a-z0-9-]+\.itch\.io/[^"]+)"[^>]*class="title[^"]*"[^>]*>([^<]+)<', html):
        if title_must.lower() in m.group(2).lower():
            from fill_gaps import og_image
            return og_image(m.group(1))
    return None


def playstore_top(query, title_must):
    try:
        html = get("https://play.google.com/store/search?q="
                   + urllib.parse.quote(query) + "&c=apps")
    except Exception:
        return None
    if not html:
        return None
    m = re.search(r"/store/apps/details\?id=([a-zA-Z0-9_.]+)", html)
    if not m:
        return None
    page = f"https://play.google.com/store/apps/details?id={m.group(1)}"
    try:
        html2 = get(page)
    except Exception:
        return None
    m2 = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)', html2 or "")
    if m2 and http_ok(m2.group(1)):
        return m2.group(1)
    return None


WANT = {
    "Klifur": lambda: itch_top("Klifur", "klifur"),
    "Running Fred": lambda: (itch_top("Running Fred", "running fred")
                             or playstore_top("Running Fred Dedalord", "fred")),
    "Bloboats": lambda: og_of("https://midzer.de/games/bloboats"),
    "Gilbert and the doors": lambda: og_of("https://midzer.de/games/gilbert"),
    "Anarch": lambda: og_of("https://drummyfish.itch.io/anarch"),
}


def main():
    import json as J
    cache = J.loads(CACHE.read_text())
    for t, full in REPO_PINS.items():
        if t in cache:
            print(f"skip (cached): {t!r}")
            continue
        if http_ok(f"https://github.com/{full}"):
            o, r = full.split("/")
            cache[t] = {"pic": OG.format(o=o, r=r)}
            print(f"repo {t!r}")
        else:
            print(f"LEFT {t!r}")
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
    CACHE.write_text(J.dumps(cache, indent=1, sort_keys=True) + "\n")
    print("cached total:", len(cache))


if __name__ == "__main__":
    main()
