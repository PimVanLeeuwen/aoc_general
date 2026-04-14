"""
Day 03 - Squares With Three Sides
Year: 2016

Determine how many sets of three numbers form valid triangles.
Part 1 checks triangles row-by-row.
Part 2 checks triangles column-by-column in groups of three rows.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rows = [
        [int(x) for x in line.split() if x]
        for line in puzzle_input.strip().split("\n")
    ]

    def is_triangle(a: int, b: int, c: int) -> bool:
        return a + b > c and b + c > a and a + c > b

    part1 = sum(1 for a, b, c in rows if is_triangle(a, b, c))

    part2 = 0
    for i in range(0, len(rows), 3):
        r1, r2, r3 = rows[i], rows[i + 1], rows[i + 2]
        for col in range(3):
            if is_triangle(r1[col], r2[col], r3[col]):
                part2 += 1

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
