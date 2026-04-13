"""
Day 11 - Hex Ed
Year: 2017

Part 1: Fewest steps to reach the final position.
Part 2: Maximum distance from the start at any point along the path.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    steps = puzzle_input.strip().split(",")

    # Cube coordinate deltas
    dirs = {
        "n":  (0, 1, -1),
        "ne": (1, 0, -1),
        "se": (1, -1, 0),
        "s":  (0, -1, 1),
        "sw": (-1, 0, 1),
        "nw": (-1, 1, 0),
    }

    x = y = z = 0
    max_dist = 0

    def dist(x, y, z):
        return (abs(x) + abs(y) + abs(z)) // 2

    for step in steps:
        dx, dy, dz = dirs[step]
        x += dx
        y += dy
        z += dz

        max_dist = max(max_dist, dist(x, y, z))

    part1 = dist(x, y, z)
    part2 = max_dist

    return str(part1), str(part2)



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
