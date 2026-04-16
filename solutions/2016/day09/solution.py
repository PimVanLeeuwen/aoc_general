"""
Day 09 - Explosives in Cyberspace
Year: 2016

Compute decompressed lengths of a custom marker-based compression format.
"""

import re

def decompress_length_v1(s: str) -> int:
    """Non-recursive decompression length (Part 1)."""
    i = 0
    length = 0
    marker_re = re.compile(r"\((\d+)x(\d+)\)")

    while i < len(s):
        if s[i] == "(":
            m = marker_re.match(s, i)
            if m:
                a, b = map(int, m.groups())
                i = m.end()
                length += a * b
                i += a
            else:
                length += 1
                i += 1
        else:
            length += 1
            i += 1

    return length


def decompress_length_v2(s: str, start=0, end=None) -> int:
    """Recursive decompression length (Part 2)."""
    if end is None:
        end = len(s)

    i = start
    length = 0
    marker_re = re.compile(r"\((\d+)x(\d+)\)")

    while i < end:
        if s[i] == "(":
            m = marker_re.match(s, i)
            if m:
                a, b = map(int, m.groups())
                i = m.end()
                # Recursively compute the length of the next A characters
                sub_len = decompress_length_v2(s, i, i + a)
                length += sub_len * b
                i += a
            else:
                length += 1
                i += 1
        else:
            length += 1
            i += 1

    return length


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    data = puzzle_input.strip().replace(" ", "").replace("\n", "")

    part1 = decompress_length_v1(data)
    part2 = decompress_length_v2(data)

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
