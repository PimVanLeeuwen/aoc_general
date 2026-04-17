"""
Day 18 - Like a Rogue
Year: 2016

Cellular automaton: count safe tiles across many rows where traps spread
based on left/right neighbours from the previous row.
"""


def count_safe(first_row, total_rows):
    """Count safe tiles across `total_rows` rows using integer bitmask arithmetic."""
    width = len(first_row)
    mask = (1 << width) - 1
    row = int(first_row.replace(".", "0").replace("^", "1")[::-1], 2)

    safe = 0
    for _ in range(total_rows):
        safe += width - bin(row).count("1")
        row = ((row << 1) ^ (row >> 1)) & mask

    return safe


def solve(puzzle_input: str) -> tuple[str, str]:
    first_row = puzzle_input.strip()
    part1 = count_safe(first_row, 40)
    part2 = count_safe(first_row, 400_000)
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Render the trap pattern growing row by row as a grid."""
    first_row = puzzle_input.strip()
    width = len(first_row)
    display_rows = min(60, width)  # keep the grid roughly square

    rows = [first_row]
    row = first_row
    for _ in range(display_rows - 1):
        next_row = ""
        for i in range(width):
            left = row[i - 1] if i > 0 else "."
            right = row[i + 1] if i < width - 1 else "."
            next_row += "^" if left != right else "."
        rows.append(next_row)
        row = next_row

    # Yield incrementally so the pattern builds up on screen
    for end in range(1, display_rows + 1):
        safe = sum(r.count(".") for r in rows[:end])
        yield {
            "type": "grid",
            "cells": [list(r) for r in rows[:end]],
            "colors": {"^": "#cc2200", ".": "#003322"},
            "delay": 60,
        }

    # Final summary
    yield {
        "type": "text",
        "lines": [
            f"  First row:  {first_row[:60]}{'…' if width > 60 else ''}",
            f"  Width:      {width}",
            "",
            f"  Safe tiles in {display_rows} rows (shown): {safe}",
            f"  Safe tiles in 40 rows:      {count_safe(first_row, 40)}",
            f"  Safe tiles in 400,000 rows: {count_safe(first_row, 400_000)}",
        ],
        "delay": 1000,
    }
