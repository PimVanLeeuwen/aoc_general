"""
Day 02 - Corruption Checksum
Year: 2017

Brief description of the puzzle.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rows = [
        list(map(int, line.split()))
        for line in puzzle_input.strip().split("\n")
    ]

    part1 = 0
    part2 = 0

    for r in rows:
        part1 += max(r) - min(r)
        r.sort(reverse=True)
        for i, a in enumerate(r):
            for j, b in enumerate(r):
                if i != j and a % b == 0:
                    part2 += a // b
                    break

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
