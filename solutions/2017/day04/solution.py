"""
Day 04 - High-Entropy Passphrases
Year: 2017

Each line of the input represents a passphrase:
a sequence of space-separated words.
A passphrase is considered valid under different rules in Part 1 and Part 2.
Both parts reduce to checking whether any two words violate the given uniqueness constraints.
"""

from collections import Counter

def check_valid(line):
    items = line.strip().split(" ")
    items_set = set(items)

    return len(items) == len(items_set)

def check_valid_strict(line):
    items = [Counter(i) for i in line.strip().split(" ")]

    for (i, num) in enumerate(items):
        for (j, num2) in enumerate(items):
            if i != j and num == num2:
                return False

    return True

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    part1 = sum(check_valid(line) for line in lines)
    part2 = sum(check_valid_strict(line) for line in lines)

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
