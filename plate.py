# plate.py — Retro title animation

import time

def animated_title_plate():
    intro_lines = [
        "╔═══════════════════════════════════════════════╗",
        "║           MASONRY WALL QUEST SIMULATOR        ║",
        "╚═══════════════════════════════════════════════╝"
    ]
    for line in intro_lines:
        print(line)
        time.sleep(0.4)
    print()
