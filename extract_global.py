# Ce code à été écrit par une license ChatGPT Pro
# Virginie Cloutier, 2026-11-21

import re
from collections import Counter

LINE_RE = re.compile(
    r"\]\[INFO\]\[(?P<user>\w+)\]\s+"
    r"(?P<method>GET|POST)\s+/(?P<endpoint>\w+)"
)

STATE_NAMES = {
    "POST login": "login",
    "GET feed": "view_feed",
    "POST post": "create_post",
    "POST like": "like_post",
    "POST follow": "follow_user",
    "GET profile": "view_profile",
}

# Compter les requêtes
counts = Counter()

with open("logs.txt", encoding="utf-16") as f:
    for line in f:
        match = LINE_RE.search(line)

        if not match:
            continue

        key = f"{match['method']} {match['endpoint']}"

        if key in STATE_NAMES:
            counts[STATE_NAMES[key]] += 1

# Calculer les fréquences
total = sum(counts.values())

print(f"Nombre total de requêtes : {total}\n")

for action in STATE_NAMES.values():
    n = counts[action]
    frequency = n / total * 100 if total else 0

    print(f"{action:<15} {n:>6} {frequency:>7.2f}%")
