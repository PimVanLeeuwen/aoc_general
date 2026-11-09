"""
Day XX - Title
Year: XXXX

Brief description of the puzzle.
"""

# Common imports: remove the unused ones before publishing.
import heapq
import math
import re
from collections import Counter, defaultdict, deque
from functools import cache
from itertools import combinations, pairwise, product

DIRS_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def ints(text: str) -> list[int]:
    """All integers in a string, including negative ones."""
    return [int(number) for number in re.findall(r"-?\d+", text)]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    # sections = puzzle_input.strip().split("\n\n")  # blocks separated by a blank line
    # grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}

    # Part 1
    part1 = ""

    # Part 2
    part2 = ""

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
