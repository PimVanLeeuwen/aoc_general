"""
Day 01 - Inverse Captcha
Year: 2017

Sum digits that match the next digit in a circular sequence.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip()
    n = len(lines)

    part1 = 0
    part2 = 0
    for i in range(n):
        if lines[i] == lines[(i + 1) % n]:
            part1 += int(lines[i])
        if lines[i] == lines[(i + (n//2)) % n]:
            part2 += int(lines[i])

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
