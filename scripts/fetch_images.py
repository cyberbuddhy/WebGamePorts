#!/usr/bin/env python3
"""Resolve a cover image for every game on the WebGamePorts page.

Priority per title:
  1. Steam capsule  (storesearch API match + HEAD-verified capsule_616x353.jpg,
     header.jpg recorded with h:1 when the capsule is missing)
  2. GitHub repo preview (repo page HEAD-verified, then opengraph image URL)
  3. nothing -> page keeps its gradient placeholder

Cache: data/images.json {title: {"img": appid[, "h": 1]} | {"pic": url}}.
Re-runs only query titles missing from the cache.

Usage:
  python3 scripts/fetch_images.py           # resolve, update data/images.json
  python3 scripts/fetch_images.py --embed   # resolve + patch index.html REST + mapper
"""
import difflib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent.parent
ALL = ROOT / "data" / "games.json"
ALLGAMES = ROOT / "data" / "all-games.json"
CACHE = ROOT / "data" / "images.json"
INDEX = ROOT / "index.html"

STEAM_SEARCH = "https://store.steampowered.com/api/storesearch/?term={q}&l=en&cc=US"
CDN = "https://cdn.cloudflare.steamstatic.com/steam/apps/"
OG = "https://opengraph.githubassets.com/1/{o}/{r}"


def norm(t):
    t = t.lower().strip()
    t = re.sub(r"\s*\([^)]*\)\s*", " ", t)          # " (GAMECUBE)", " (TH08)"
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^a-z0-9 ]", "", t).strip()        # punctuation
    t = re.sub(r"\s+(game|demo|full|web|port|remake)$", "", t)
    return t


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "WebGamePorts-image-bot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def http_ok(url, timeout=20):
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "WebGamePorts-image-bot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def steam_match(title):
    """Return (appid, use_header) or None."""
    try:
        data = http_json(STEAM_SEARCH.format(q=urllib.parse.quote(title)))
    except Exception as e:
        print(f"  steam api error for {title!r}: {e}", flush=True)
        return None
    want = norm(title)
    if not want:
        return None
    best, best_score = None, 0.0
    for item in data.get("items", []) or []:
        if item.get("type") != "app":
            continue
        name = norm(str(item.get("name", "")))
        if not name:
            continue
        if name == want:
            best, best_score = item, 1.0
            break
        score = difflib.SequenceMatcher(None, name, want).ratio()
        if score > best_score:
            best, best_score = item, score
    if best is None or best_score < 0.92:
        return None
    appid = best["id"]
    if http_ok(f"{CDN}{appid}/capsule_616x353.jpg"):
        return appid, False
    if http_ok(f"{CDN}{appid}/header.jpg"):
        return appid, True
    return None


def github_preview(repo_url):
    """Return og-image URL if repo_url is an existing github repo, else None."""
    m = re.match(r"https?://(?:www\.)?github\.com/([^/]+)/([^/?#]+)", repo_url or "")
    if not m:
        return None
    owner, repo = m.group(1), re.sub(r"\.git$", "", m.group(2))
    if not http_ok(f"https://github.com/{owner}/{repo}"):
        return None
    return OG.format(o=owner, r=repo)


def rest_titles(html):
    return re.findall(r'\{"t":"((?:[^"\\]|\\.)*)"', html)


def resolve_all():
    games = json.loads(ALLGAMES.read_text())["games"]
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    html = INDEX.read_text()
    have = set(rest_titles(html))
    titles = {}  # title -> repo_url (json wins; rest-only get None repo)
    for g in games:
        titles[g["title"]] = g.get("repo_url")
    for raw in have:
        t = json.loads(f'"{raw}"')
        titles.setdefault(t, None)

    todo = [t for t in titles if t not in cache]
    print(f"{len(titles)} titles total, {len(todo)} to resolve")
    for i, t in enumerate(todo):
        entry = None
        hit = steam_match(t)
        if hit:
            appid, use_header = hit
            entry = {"img": appid} | ({"h": 1} if use_header else {})
            print(f"[{i+1}/{len(todo)}] steam  {t!r} -> {appid}" + (" (header)" if use_header else ""))
        else:
            pic = github_preview(titles[t]) if titles[t] else None
            if pic:
                entry = {"pic": pic}
                print(f"[{i+1}/{len(todo)}] github {t!r} -> {pic}")
            else:
                print(f"[{i+1}/{len(todo)}] none   {t!r}")
        if entry:
            cache[t] = entry
        time.sleep(0.4)
        if (i + 1) % 25 == 0:
            CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    return cache


OBJ = re.compile(r'\{[^{}]*"t":"((?:[^"\\]|\\.)*)"[^{}]*\}')

MAPPER_OLD = 'REST.forEach((r,k)=>CARDS.push({t:r.t, st:r.p?"play":"self", play:r.p||null, playText:r.p?null:"No demo",'
MAPPER_NEW = ('REST.forEach((r,k)=>CARDS.push({t:r.t, st:r.p?"play":"self", play:r.p||null, playText:r.p?null:"No demo",\n'
              '  pic:r.pic||null, img:r.img||null, h:r.h||null,')


def embed(cache):
    html = INDEX.read_text()
    n = 0

    def patch(m):
        nonlocal n
        obj = json.loads(m.group(0))
        info = cache.get(obj["t"])
        if not info or "img" in obj or "pic" in obj:
            return m.group(0)
        extra = "".join(
            f',"{k}":{json.dumps(v)}' for k, v in info.items()
        )
        n += 1
        return m.group(0)[:-1] + extra + "}"

    html = OBJ.sub(patch, html)
    if MAPPER_NEW in html:
        print("mapper already patched")
    elif MAPPER_OLD not in html:
        print("mapper pattern not found - index.html changed?", file=sys.stderr)
        sys.exit(1)
    else:
        html = html.replace(MAPPER_OLD, MAPPER_NEW)
    INDEX.write_text(html)
    print(f"embedded images into {n} REST entries + mapper")


def report(cache):
    games = json.loads(ALLGAMES.read_text())["games"]
    html = INDEX.read_text()
    have = set(json.loads(f'"{r}"') for r in rest_titles(html))
    titles = {g["title"] for g in games} | have
    steam = sum(1 for t in titles if "img" in cache.get(t, {}))
    gh = sum(1 for t in titles if "pic" in cache.get(t, {}))
    missing = sorted(t for t in titles if t not in cache)
    print(f"\ncoverage: {steam} steam + {gh} github = {steam+gh}/{len(titles)} "
          f"({100*(steam+gh)//len(titles)}%), {len(missing)} placeholder")
    for t in missing:
        print(f"  placeholder: {t}")


if __name__ == "__main__":
    if "--embed-only" in sys.argv:
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        embed(cache)
        report(cache)
        sys.exit(0)
    cache = resolve_all()
    if "--embed" in sys.argv:
        embed(cache)
    report(cache)
