"""
Day 06 - Signals and Noise
Year: 2016

Recover a corrupted message by analyzing per-column character frequencies.
"""

from collections import Counter


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # Transpose columns: zip(*lines) gives tuples of characters per column
    columns = list(zip(*lines))

    # Part 1: most common character per column
    part1 = "".join(Counter(col).most_common(1)[0][0] for col in columns)

    # Part 2: least common character per column
    part2 = "".join(sorted(Counter(col).items(), key=lambda x: x[1])[0][0] for col in columns)

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
