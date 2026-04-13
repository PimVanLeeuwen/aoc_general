def solve(puzzle_input: str) -> tuple[str, str]:
    from collections import defaultdict

    lines = [line.strip() for line in puzzle_input.strip().split("\n") if line.strip()]

    particles = []
    for idx, line in enumerate(lines):
        parts_line = line.split(", ")
        def parse_vec(part):
            inside = part[3:-1]
            return list(map(int, inside.split(",")))

        p = parse_vec(parts_line[0])
        v = parse_vec(parts_line[1])
        a = parse_vec(parts_line[2])
        particles.append({"id": idx, "p": p, "v": v, "a": a})

    def manhattan(v):
        return abs(v[0]) + abs(v[1]) + abs(v[2])

    # -------------------------
    # Part 1 — simulate until stable
    # -------------------------
    parts1 = [
        {"id": p["id"], "p": p["p"][:], "v": p["v"][:], "a": p["a"][:]}
        for p in particles
    ]

    for _ in range(5000):
        for par in parts1:
            for i in range(3):
                par["v"][i] += par["a"][i]
                par["p"][i] += par["v"][i]

    # After stabilization, pick closest
    best = min(parts1, key=lambda p: manhattan(p["p"]))
    part1 = str(best["id"])

    # -------------------------
    # Part 2 — collisions
    # -------------------------
    parts2 = [
        {"id": p["id"], "p": p["p"][:], "v": p["v"][:], "a": p["a"][:]}
        for p in particles
    ]

    no_collision_streak = 0
    for _ in range(10000):
        # update
        for par in parts2:
            for i in range(3):
                par["v"][i] += par["a"][i]
                par["p"][i] += par["v"][i]

        # collisions
        pos = defaultdict(list)
        for par in parts2:
            pos[tuple(par["p"])].append(par)

        new_parts = [g[0] for g in pos.values() if len(g) == 1]

        if len(new_parts) == len(parts2):
            no_collision_streak += 1
        else:
            no_collision_streak = 0

        parts2 = new_parts

        if no_collision_streak > 200:
            break

    part2 = str(len(parts2))

    return part1, part2




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
