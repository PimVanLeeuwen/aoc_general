"""
Day 24 - Electromagnetic Moat
Year: 2017

Build the strongest and longest magnetic bridge using backtracking.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    components = []
    for line in puzzle_input.strip().split("\n"):
        a, b = map(int, line.split("/"))
        components.append((a, b))

    # Precompute adjacency: port -> list of component indices
    portmap = {}
    for i, (a, b) in enumerate(components):
        portmap.setdefault(a, []).append(i)
        portmap.setdefault(b, []).append(i)

    used = [False] * len(components)

    best_strength = 0
    best_len = 0
    best_len_strength = 0

    def dfs(open_port, strength, length):
        nonlocal best_strength, best_len, best_len_strength

        # Update Part 1
        if strength > best_strength:
            best_strength = strength

        # Update Part 2
        if length > best_len:
            best_len = length
            best_len_strength = strength
        elif length == best_len and strength > best_len_strength:
            best_len_strength = strength

        # Try all components that match open_port
        for idx in portmap.get(open_port, []):
            if not used[idx]:
                a, b = components[idx]
                used[idx] = True

                next_port = b if a == open_port else a
                dfs(next_port, strength + a + b, length + 1)

                used[idx] = False

    # Start from port 0
    dfs(0, 0, 0)

    part1 = str(best_strength)
    part2 = str(best_len_strength)

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
