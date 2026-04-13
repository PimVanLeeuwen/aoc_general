"""
Day 22 - Sporifica Virus
Year: 2017

Simulate a virus carrier on an infinite grid with evolving infection rules.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    lines = puzzle_input.strip().split("\n")
    n = len(lines)
    mid = n // 2

    # Parse initial infected nodes
    infected_initial = set()
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                infected_initial.add((r - mid, c - mid))

    # Directions: up, right, down, left
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    infected = set(infected_initial)
    r = c = 0
    d = 0  # facing up
    bursts_infected = 0

    for _ in range(10000):
        if (r, c) in infected:
            # turn right
            d = (d + 1) % 4
            infected.remove((r, c))
        else:
            # turn left
            d = (d - 1) % 4
            infected.add((r, c))
            bursts_infected += 1

        dr, dc = dirs[d]
        r += dr
        c += dc

    part1 = str(bursts_infected)

    # States: . (clean), W (weakened), # (infected), F (flagged)
    grid = {}
    for (rr, cc) in infected_initial:
        grid[(rr, cc)] = "#"

    r = c = 0
    d = 0
    bursts_infected2 = 0

    for _ in range(10_000_000):
        state = grid.get((r, c), ".")

        if state == ".":
            d = (d - 1) % 4  # left
            grid[(r, c)] = "W"
        elif state == "W":
            # no turn
            grid[(r, c)] = "#"
            bursts_infected2 += 1
        elif state == "#":
            d = (d + 1) % 4  # right
            grid[(r, c)] = "F"
        elif state == "F":
            d = (d + 2) % 4  # reverse
            grid[(r, c)] = "."

        dr, dc = dirs[d]
        r += dr
        c += dc

    part2 = str(bursts_infected2)

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
