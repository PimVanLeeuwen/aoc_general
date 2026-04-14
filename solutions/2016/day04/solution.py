"""
Day 04 - Security Through Obscurity
Year: 2016

Validate encrypted room names using frequency-based checksums.
Part 1: Sum sector IDs of real rooms.
Part 2: Decrypt names using a Caesar shift to find the North Pole storage room.
"""

from collections import Counter

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    lines = puzzle_input.strip().split("\n")

    def parse(i_line: str):
        # Find last '-' before the sector ID
        last_dash = i_line.rfind("-")

        i_name = i_line[:last_dash]
        rest = i_line[last_dash + 1:]  # e.g. "123[abcde]"

        # Split sector and checksum
        sector_str, c = rest.split("[")
        c = c[:-1]  # remove trailing ']'

        return i_name, int(sector_str), c

    def compute_checksum(i_name: str) -> str:
        counts = Counter(ch for ch in i_name if ch != "-")
        sorted_items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return "".join(ch for ch, _ in sorted_items[:5])

    def decrypt(i_name: str, i_sector: int) -> str:
        result = []
        for ch in i_name:
            if ch == "-":
                result.append(" ")
            else:
                shifted = chr((ord(ch) - ord("a") + i_sector) % 26 + ord("a"))
                result.append(shifted)
        return "".join(result)

    part1 = 0
    part2 = ""

    for line in lines:
        name, sector, checksum = parse(line)

        if compute_checksum(name) == checksum:
            part1 += sector

            decrypted = decrypt(name, sector)
            if "northpole" in decrypted:
                part2 = str(sector)

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
