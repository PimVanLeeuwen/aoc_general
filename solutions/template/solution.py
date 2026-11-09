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

# Shared helpers (solutions/aoc_utils.py), loaded automatically on the site.
from aoc_utils import DIRS_4, DIRS_8, bfs, dijkstra, grid_find, ints, lines, neighbors, parse_grid, sections


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rows = lines(puzzle_input)
    # blocks = sections(puzzle_input)  # parts separated by a blank line
    # grid = parse_grid(puzzle_input)  # {(row, col): char}

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
#     rows = lines(puzzle_input)
#
#     # Grid frame – renders as a pixel canvas:
#     yield {
#         "type": "grid",
#         "cells": [list(row) for row in rows],
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
