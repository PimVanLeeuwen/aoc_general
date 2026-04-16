"""
Day 08 - Two-Factor Authentication
Year: 2016

Simulate a pixel display responding to rect and rotation instructions.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    # 50x6 display (width x height)
    W, H = 50, 6
    screen = [[0 for _ in range(W)] for _ in range(H)]

    def rect(a, b):
        for y in range(b):
            for x in range(a):
                screen[y][x] = 1

    def rotate_row(y, shift):
        shift %= W
        screen[y] = screen[y][-shift:] + screen[y][:-shift]

    def rotate_col(x, shift):
        shift %= H
        col = [screen[y][x] for y in range(H)]
        col = col[-shift:] + col[:-shift]
        for y in range(H):
            screen[y][x] = col[y]

    for line in puzzle_input.strip().split("\n"):
        parts = line.split()
        if parts[0] == "rect":
            a, b = map(int, parts[1].split("x"))
            rect(a, b)
        elif parts[1] == "row":
            y = int(parts[2].split("=")[1])
            shift = int(parts[4])
            rotate_row(y, shift)
        elif parts[1] == "column":
            x = int(parts[2].split("=")[1])
            shift = int(parts[4])
            rotate_col(x, shift)

    # Part 1: count lit pixels
    part1 = sum(sum(row) for row in screen)

    # Part 2: render the screen
    part2 = "\n".join("".join("#" if c else "." for c in row) for row in screen)

    return str(part1), part2

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
