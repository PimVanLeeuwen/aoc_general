"""
Day 14 - Regolith Reservoir
Year: 2022

Simulate sand falling through a cave with rock structures.
"""


def parse_rocks(text):
    """Parse rock paths into a set of filled coordinates."""
    filled = set()
    for line in text.strip().split("\n"):
        points = []
        for part in line.split(" -> "):
            x, y = map(int, part.split(","))
            points.append((x, y))
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    filled.add((x1, y))
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    filled.add((x, y1))
    return filled


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rocks = parse_rocks(puzzle_input)
    max_y = max(y for _, y in rocks)

    # Part 1: sand falls into void below max_y
    filled = set(rocks)
    part1 = 0
    while True:
        x, y = 500, 0
        settled = False
        while y <= max_y:
            if (x, y + 1) not in filled:
                y += 1
            elif (x - 1, y + 1) not in filled:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in filled:
                x += 1
                y += 1
            else:
                filled.add((x, y))
                part1 += 1
                settled = True
                break
        if not settled:
            break

    # Part 2: floor at max_y + 2, fill until source blocked
    floor = max_y + 2
    filled = set(rocks)
    part2 = 0
    while (500, 0) not in filled:
        x, y = 500, 0
        while True:
            if y + 1 == floor:
                filled.add((x, y))
                part2 += 1
                break
            elif (x, y + 1) not in filled:
                y += 1
            elif (x - 1, y + 1) not in filled:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in filled:
                x += 1
                y += 1
            else:
                filled.add((x, y))
                part2 += 1
                break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing sand simulation."""
    rocks = parse_rocks(puzzle_input)
    max_y = max(y for _, y in rocks)
    min_x = min(x for x, _ in rocks) - 2
    max_x = max(x for x, _ in rocks) + 2

    # Show the rock structure
    cells = []
    for y in range(max_y + 3):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) == (500, 0):
                row.append("+")
            elif (x, y) in rocks:
                row.append("#")
            else:
                row.append(".")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {"#": "#888888", "+": "#ffff00", ".": "#0f0f23"},
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (sand before void)",
            f"  Part 2: {part2} (sand with floor)",
        ],
        "delay": 500,
    }
