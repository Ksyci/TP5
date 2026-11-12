# Ce code à été écrit par une license Claude Pro
# Alexy Parent, 2026-11-12

"""Extraction d'une chaîne de Markov à partir de logs.txt (TP5 LOG3430)."""
import re
import sys
from collections import Counter, defaultdict

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "logs.txt"

# Ex. : [2025-09-04 20:23:14][INFO][creative_beaver] POST /like/15
LINE_RE = re.compile(r"\]\[INFO\]\[(?P<user>\w+)\]\s+(?P<method>GET|POST)\s+/(?P<endpoint>\w+)")

STATE_NAMES = {
    "POST login": "login",
    "GET feed": "view_feed",
    "POST post": "create_post",
    "POST like": "like_post",
    "POST follow": "follow_user",
    "GET profile": "view_profile",
}

# Le fichier a été créé par une redirection PowerShell : UTF-16
with open(LOG_FILE, encoding="utf-16") as f:
    lines = f.readlines()

# 1) Séquence de requêtes par utilisateur, dans l'ordre des logs
sequences = defaultdict(list)
for line in lines:
    m = LINE_RE.search(line)
    if not m:
        continue
    state = STATE_NAMES[f"{m['method']} {m['endpoint']}"]
    if m["user"] == "anonymous":
        continue  # login anonyme : on l'ajoute comme état initial plus bas
    sequences[m["user"]].append(state)

# 2) Comptage des transitions (chaque utilisateur commence par login)
transitions = defaultdict(Counter)
for user, seq in sequences.items():
    seq = ["login"] + seq
    for current, nxt in zip(seq, seq[1:]):
        transitions[current][nxt] += 1

# 3) Affichage : comptes et probabilités
print(f"{len(sequences)} utilisateurs\n")
for state in STATE_NAMES.values():
    counts = transitions.get(state)
    if not counts:
        continue
    total = sum(counts.values())
    print(f"{state} ({total} transitions sortantes)")
    for nxt, n in counts.most_common():
        print(f"  -> {nxt:<13} {n:>4}  {n / total:6.1%}")
    print()
