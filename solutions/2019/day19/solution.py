"""
Day 19 - Tractor Beam
Year: 2019

Query an Intcode drone program to map a tractor beam, then find
where a 100x100 square first fits inside the beam.
"""

from intcode import IntcodeComputer


def probe(program, x, y):
    """Query whether position (x, y) is in the tractor beam."""
    cpu = IntcodeComputer(program, inputs=[x, y])
    cpu.run()
    return cpu.outputs[0]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Part 1: count affected points in 50x50 grid
    part1 = sum(probe(program, x, y) for y in range(50) for x in range(50))

    # Part 2: find top-left corner of first 100x100 square fitting in the beam
    # Track the left edge of the beam as we scan down rows.
    # For each row y, find the leftmost x in the beam, then check if
    # (x+99, y-99) is also in the beam — meaning a 100-wide span exists
    # at row y AND the beam is tall enough 99 rows above.
    x = 0
    y = 100  # start far enough down that the beam is wide enough
    while True:
        # Find leftmost beam position in this row
        while not probe(program, x, y):
            x += 1
        # Check if 100-wide span: top-right corner of the square
        if probe(program, x + 99, y - 99):
            part2 = x * 10000 + (y - 99)
            break
        y += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the tractor beam scan."""
    program = [int(x) for x in puzzle_input.strip().split(",")]

    # Scan a portion of the beam for display
    size = 50
    cells = []
    count = 0
    for y in range(size):
        row = []
        for x in range(size):
            val = probe(program, x, y)
            count += val
            row.append("#" if val else ".")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "#": "#4488ff",
        },
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  Tractor Beam — 50x50 Scan",
            "",
            f"  Affected points: {count}",
            "",
            "  Searching for 100x100 square...",
        ],
        "delay": 600,
    }

    # Find part 2 answer
    x = 0
    y = 100
    while True:
        while not probe(program, x, y):
            x += 1
        if probe(program, x + 99, y - 99):
            sq_x, sq_y = x, y - 99
            break
        y += 1

    # Show a zoomed view around the square
    margin = 5
    view_x0 = max(0, sq_x - margin)
    view_y0 = max(0, sq_y - margin)
    view_x1 = sq_x + 100 + margin
    view_y1 = sq_y + 100 + margin

    cells2 = []
    for vy in range(view_y0, view_y1):
        row = []
        for vx in range(view_x0, view_x1):
            in_beam = probe(program, vx, vy)
            in_square = sq_x <= vx < sq_x + 100 and sq_y <= vy < sq_y + 100
            if in_square:
                row.append("S")
            elif in_beam:
                row.append("#")
            else:
                row.append(".")
        cells2.append(row)

    yield {
        "type": "grid",
        "cells": cells2,
        "colors": {
            ".": "#0f0f23",
            "#": "#4488ff",
            "S": "#ffff00",
        },
        "delay": 800,
    }

    part2 = sq_x * 10000 + sq_y

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {count} (affected in 50x50)",
            f"  Part 2: {part2} (square at {sq_x},{sq_y})",
        ],
        "delay": 500,
    }
