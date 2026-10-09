#!/usr/bin/env python3
"""Gap pass: resolve images for titles missing from data/images.json.

Passes (cheapest first), all verified before caching:
  1. cleaned-query Steam retry (strip parens/colon-suffixes/demos)
  2. manual pins (certain appids, curated pic reuse, repo pins)
  3. GitHub org/user avatars for user/org-only repo URLs
  4. og:image scraped from play_url, then repo_url pages
  5. GitHub repo search (needs GITHUB_TOKEN env) for the rest

Usage: GITHUB_TOKEN=... python3 scripts/fill_gaps.py
"""
import difflib
import json
import os
import pathlib
import re
import time
import urllib.parse
import urllib.request
from fetch_images import (norm, http_json, http_ok, steam_match, github_preview,
                          ALLGAMES, CACHE, INDEX, rest_titles, CDN)

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# title -> certain steam appid (auto-verified, dropped on failure)
PINS = {
    "DOOM I & II": 2280,
    "Black Ops 1 Zombies": 42700,
    "Modern Warfare 2 (OVZ)": 10180,
    "Plague Inc": 246620,
    "Brotato (3)": 1942280,
    "Deltarune Chapters 1-4": 1671210,
    "Totally Accurate Battle Simulator (TABS)": 508440,
    "Untitled Goose Game (2)": 837740,
    "Hollow Knight: Silksong (2)": 1030300,
}
# title -> extra search aliases tried in order
ALIASES = {
    "HERETIC / HEXEN": ["Heretic + Hexen", "Heretic", "Hexen"],
    "NAM / Napalm": ["NAM"],
    "Unreal Gold": ["Unreal Gold", "Unreal"],
    "Redneck Rampage: Route 66": ["Redneck Rampage"],
    "Descent": ["Descent"],
    "Gorilla Tag (2)": ["Gorilla Tag"],
    "Rec Room": ["Rec Room"],
    "Granny (2)": ["Granny"],
    "Space Rangers: Quests": ["Space Rangers"],
    "Counter Strike & Half Life": ["Half-Life", "Counter-Strike"],
    "Quake TG": ["Quake"],
    "Duke Nukem 3D TG": ["Duke Nukem 3D"],
    "DUNE II TG": ["Dune II"],
    "Wolfenstein 3D TG": ["Wolfenstein 3D"],
    "Super Monkey Ball": ["Super Monkey Ball"],
}
# title -> reuse curated pic URL
PIC_REUSE = {
    "Skate 3": "https://upload.wikimedia.org/wikipedia/en/8/84/Skate-3-Boxart.jpg",
    "Simpsons: Hit & Run": "https://upload.wikimedia.org/wikipedia/en/5/5f/The_Simpsons_Hit_and_Run_cover.png",
}
# title -> pinned github owner/repo (auto-verified, dropped on failure)
REPO_PINS = {
    "Eaglercraft": "lax1dude/eaglercraftX-1.8",
    "GTA V": "shadany7824/playgta5",
    "Simpsons: Hit & Run": None,
}
OG = "https://opengraph.githubassets.com/1/{o}/{r}"
SKIP_OG_HOSTS = ("gn-math.dev",)
GENERIC_OG = ("logo", "favicon", "default", "placeholder", "gitlab-logo")


def clean_queries(title):
    yield title
    no_paren = re.sub(r"\s*\([^)]*\)", "", title).strip()
    if no_paren != title:
        yield no_paren
    for sep in (":", "/", "&"):
        if sep in title:
            yield title.split(sep)[0].strip()
    t = re.sub(r"\s+(demo|TG|\(2\)|\(3\))$", "", title, flags=re.I).strip()
    if t != title:
        yield t


def steam_alias(title):
    for q in ALIASES.get(title, []):
        hit = steam_match(q)
        if hit:
            return hit
        time.sleep(0.4)
    return None


def avatar(user):
    u = f"https://github.com/{user}.png"
    return u if http_ok(u) else None


def user_avatar(repo_url):
    m = re.match(r"https?://(?:www\.)?github\.com/([^/?#]+)/?\s*(?:\(.*\))?$", repo_url or "")
    if not m or "/" in m.group(1):
        return None
    user = m.group(1).rstrip("/")
    if user in ("tree", "blob"):
        return None
    # repo-style URL with .git or subpath -> not a plain user page
    if re.search(r"\.git|/tree/|/blob/", repo_url or ""):
        # extract owner for owner-only fallback? no - keep strict
        pass
    if "/" in (repo_url or "").split("github.com/")[-1].strip("/"):
        return None
    return avatar(user)


def og_image(page_url):
    if not page_url:
        return None
    host = urllib.parse.urlparse(page_url).netloc
    if host in SKIP_OG_HOSTS:
        return None
    try:
        req = urllib.request.Request(page_url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status >= 400:
                return None
            html = r.read().decode("utf-8", "replace")[:300000]
    except Exception:
        return None
    m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)', html)
    if not m:
        m = re.search(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)', html)
    if not m:
        return None
    url = urllib.parse.urljoin(page_url, m.group(1))
    low = url.lower()
    if any(g in low for g in GENERIC_OG) or not url.startswith("http"):
        return None
    return url if http_ok(url) else None


def gh_search(title):
    if not TOKEN:
        return None
    q = norm(title) + " web port"
    url = ("https://api.github.com/search/repositories?q="
           + urllib.parse.quote(q) + "&per_page=5")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WGP/1.0",
                                                   "Authorization": f"Bearer {TOKEN}"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"  ghsearch error {title!r}: {e}")
        return None
    for item in data.get("items", []):
        name = norm(item.get("name", ""))
        score = difflib.SequenceMatcher(None, name, norm(title)).ratio()
        desc = (item.get("description") or "").lower()
        kw = any(k in desc for k in ("web", "port", "wasm", "browser", "emscripten"))
        if score >= 0.85 or (score >= 0.65 and kw):
            full = item["full_name"]
            if http_ok(f"https://github.com/{full}"):
                return OG.format(o=full.split("/")[0], r=full.split("/")[1])
    return None


def main():
    games = {g["title"]: g for g in json.loads(ALLGAMES.read_text())["games"]}
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    html = INDEX.read_text()
    rest_only = [json.loads(f'"{r}"') for r in rest_titles(html)]
    titles = dict.fromkeys(list(games) + rest_only)
    todo = [t for t in titles if t not in cache]
    print(f"{len(todo)} still missing")

    def save():
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")

    for i, t in enumerate(todo):
        tag = f"[{i+1}/{len(todo)}]"
        g = games.get(t, {})
        entry = None
        # 1. pins
        if t in PINS:
            appid = PINS[t]
            if http_ok(f"{CDN}{appid}/capsule_616x353.jpg"):
                entry = {"img": appid}
            elif http_ok(f"{CDN}{appid}/header.jpg"):
                entry = {"img": appid, "h": 1}
            print(f"{tag} pin-steam {t!r} -> {'OK' if entry else 'FAIL'}")
        if entry is None and t in PIC_REUSE and http_ok(PIC_REUSE[t]):
            entry = {"pic": PIC_REUSE[t]}
            print(f"{tag} pin-pic {t!r} -> OK")
        if entry is None and t in REPO_PINS:
            rp = REPO_PINS[t]
            if rp and http_ok(f"https://github.com/{rp}"):
                o, r = rp.split("/")
                entry = {"pic": OG.format(o=o, r=r)}
            print(f"{tag} pin-repo {t!r} -> {'OK' if entry else 'FAIL'}")
        # 2. cleaned steam retry + aliases
        if entry is None:
            hit = None
            for q in clean_queries(t):
                hit = steam_match(q)
                if hit:
                    break
                time.sleep(0.4)
            if hit is None:
                hit = steam_alias(t)
            if hit:
                appid, hdr = hit
                entry = {"img": appid} | ({"h": 1} if hdr else {})
                print(f"{tag} steam {t!r} -> {appid}")
        # 3. retry direct github repo (transients happen)
        if entry is None and g.get("repo_url"):
            pic = github_preview(g["repo_url"])
            if pic:
                entry = {"pic": pic}
                print(f"{tag} github {t!r} -> {pic}")
        # 4. avatars
        if entry is None and g.get("repo_url"):
            av = user_avatar(g["repo_url"])
            if av:
                entry = {"pic": av}
                print(f"{tag} avatar {t!r} -> {av}")
        # 5. og scrape: play page, then repo page
        if entry is None:
            for u in (g.get("play_url"), g.get("repo_url")):
                im = og_image(u)
                if im:
                    entry = {"pic": im}
                    print(f"{tag} ogscrape {t!r} -> {im[:80]}")
                    break
        # 6. authed repo search
        if entry is None and TOKEN:
            pic = gh_search(t)
            time.sleep(2.5)
            if pic:
                entry = {"pic": pic}
                print(f"{tag} ghsearch {t!r} -> {pic}")
        if entry is None:
            print(f"{tag} none {t!r}")
        else:
            cache[t] = entry
            if (len(cache) % 10) == 0:
                save()
    save()
    missing = [t for t in titles if t not in cache]
    s = sum(1 for v in cache.values() if "img" in v)
    print(f"\nnow: {s} steam + {len(cache)-s} other = {len(cache)}/{len(titles)}; {len(missing)} left")
    for t in missing:
        print(f"  LEFT: {t}")


if __name__ == "__main__":
    main()
