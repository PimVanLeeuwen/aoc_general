"""
Day 05 - How About a Nice Game of Chess?
Year: 2016

Brute-force MD5 hashing to discover an 8-character door password.
"""

import hashlib

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    door_id = puzzle_input.strip()

    # Part 1
    part1 = ""
    index = 0

    while len(part1) < 8:
        h = hashlib.md5(f"{door_id}{index}".encode()).hexdigest()
        if h.startswith("00000"):
            part1 += h[5]
        index += 1

    # Part 2
    part2 = ["_"] * 8
    filled = 0
    index = 0

    while filled < 8:
        h = hashlib.md5(f"{door_id}{index}".encode()).hexdigest()
        if h.startswith("00000"):
            pos = h[5]
            if pos.isdigit():
                pos = int(pos)
                if 0 <= pos < 8 and part2[pos] == "_":
                    part2[pos] = h[6]
                    filled += 1
        index += 1

    return part1, "".join(part2)



# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.
#
# def visualize(puzzle_input: str):
#     """Yield visualization frames (up to ~500 recommended)."""
#     lines = puzzle_input.strip().split("\n")
#
#     # Grid frame – renders as a pixel canvas:
#     yield {
#         "type": "grid",
#         "cells": [list(row) for row in lines],
#         "colors": {"#": "#00ff41", ".": "#0f0f23"},   # cell → hex color
#         "delay": 100,   # ms before advancing to next frame
#     }
#
#     # Text frame – renders as monospace text:
#     yield {
#         "type": "text",
#         "lines": ["Step 1", "Value: 42"],
#         "delay": 300,
#     }
