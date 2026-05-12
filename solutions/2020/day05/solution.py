"""
Day 5 - Binary Boarding
Year: 2020

Decode boarding passes as binary numbers to find seat IDs.
"""


def seat_id(boarding_pass):
    """Convert a boarding pass to a seat ID using binary space partitioning.

    F/L = 0, B/R = 1 — the pass is just a 10-bit binary number.
    """
    binary = boarding_pass.translate(str.maketrans("FBLR", "0101"))
    return int(binary, 2)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    ids = {seat_id(line) for line in puzzle_input.strip().split("\n")}

    part1 = max(ids)

    # Part 2: find the missing seat with neighbors present
    part2 = next(s for s in range(min(ids), max(ids)) if s not in ids)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the seat map."""
    lines = puzzle_input.strip().split("\n")
    ids = sorted(seat_id(line) for line in lines)

    yield {
        "type": "text",
        "lines": [
            "  Binary Boarding",
            "",
            f"  Boarding passes: {len(ids)}",
            f"  Seat ID range: {ids[0]} - {ids[-1]}",
            f"  Example: {lines[0]} -> {seat_id(lines[0])}",
        ],
        "delay": 600,
    }

    id_set = set(ids)
    missing = next(s for s in range(ids[0], ids[-1]) if s not in id_set)

    # Show a grid of seat occupancy (rows x cols)
    min_row = ids[0] // 8
    max_row = ids[-1] // 8
    cells = []
    for row in range(min_row, min(min_row + 60, max_row + 1)):
        r = []
        for col in range(8):
            sid = row * 8 + col
            if sid == missing:
                r.append("M")
            elif sid in id_set:
                r.append("#")
            else:
                r.append(".")
        cells.append(r)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "#": "#666688",
            "M": "#ffff00",
        },
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {ids[-1]} (highest seat ID)",
            f"  Part 2: {missing} (your seat)",
        ],
        "delay": 500,
    }
