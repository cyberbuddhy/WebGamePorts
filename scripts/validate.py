#!/usr/bin/env python3
"""Validate data/games.json: schema + duplicate play/repo URLs."""
import json, sys, pathlib

p = pathlib.Path(__file__).parent.parent / "data" / "games.json"
db = json.loads(p.read_text())
games = db.get("games", [])
required = {"title","play_url","repo_url","engine","tech","status","last_verified","in_lists","needs_own_files","notes"}
errors = []
seen_play, seen_repo = {}, {}
for i,g in enumerate(games):
    missing = required - set(g.keys())
    if missing:
        errors.append(f"[{i}] {g.get('title','?')}: missing {missing}")
    for key, seen in (("play_url",seen_play),("repo_url",seen_repo)):
        v = str(g.get(key,"")).strip().lower()
        if v and v in seen:
            errors.append(f"[{i}] {g.get('title')}: duplicate {key} '{g.get(key)}' also in [{seen[v]}]")
        elif v:
            seen[v]=i
if errors:
    print("FAIL:")
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(games)} games, no duplicates, schema clean.")
