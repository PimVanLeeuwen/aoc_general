"""
Day 01 - No Time for a Taxicab
Year: 2016

Follow turn instructions on a grid, compute Manhattan distance to final
location (Part 1) and distance to the first location visited twice (Part 2).
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    steps = puzzle_input.strip().split(", ")

    # Directions: 0=N, 1=E, 2=S, 3=W
    direction = 0
    x = y = 0

    visited = set()
    visited.add((0, 0))
    first_revisit = None

    # Movement vectors for N,E,S,W
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for step in steps:
        turn = step[0]
        dist = int(step[1:])

        # Update direction
        if turn == "R":
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4

        dx, dy = moves[direction]

        # Move step-by-step to detect revisits
        for _ in range(dist):
            x += dx
            y += dy

            if first_revisit is None:
                if (x, y) in visited:
                    first_revisit = (x, y)
                visited.add((x, y))

    part1 = str(abs(x) + abs(y))
    part2 = str(abs(first_revisit[0]) + abs(first_revisit[1])) if first_revisit else ""

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
