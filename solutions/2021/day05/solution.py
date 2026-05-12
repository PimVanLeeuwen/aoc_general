"""
Day 05 - Hydrothermal Venture
Year: 2021

Map hydrothermal vent lines on the ocean floor and count overlap points,
first with only horizontal/vertical lines, then including diagonals.
"""

from collections import Counter


def parse_lines(text):
    """Parse line segments from input."""
    segments = []
    for line in text.strip().split("\n"):
        parts = line.split(" -> ")
        x1, y1 = map(int, parts[0].split(","))
        x2, y2 = map(int, parts[1].split(","))
        segments.append((x1, y1, x2, y2))
    return segments


def points_on_line(x1, y1, x2, y2):
    """Generate all integer points on a line segment (horizontal, vertical, or 45-degree diagonal)."""
    dx = (x2 > x1) - (x2 < x1)
    dy = (y2 > y1) - (y2 < y1)
    steps = max(abs(x2 - x1), abs(y2 - y1))
    for i in range(steps + 1):
        yield (x1 + dx * i, y1 + dy * i)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    segments = parse_lines(puzzle_input)

    # Part 1: only horizontal and vertical lines
    hv_counts = Counter()
    for x1, y1, x2, y2 in segments:
        if x1 == x2 or y1 == y2:
            for point in points_on_line(x1, y1, x2, y2):
                hv_counts[point] += 1
    part1 = sum(1 for v in hv_counts.values() if v >= 2)

    # Part 2: include diagonal lines
    all_counts = Counter()
    for x1, y1, x2, y2 in segments:
        for point in points_on_line(x1, y1, x2, y2):
            all_counts[point] += 1
    part2 = sum(1 for v in all_counts.values() if v >= 2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing vent line mapping."""
    segments = parse_lines(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Hydrothermal Venture",
            "",
            f"  Line segments: {len(segments)}",
            f"  Horizontal/Vertical: {sum(1 for x1, y1, x2, y2 in segments if x1 == x2 or y1 == y2)}",
            f"  Diagonal: {sum(1 for x1, y1, x2, y2 in segments if x1 != x2 and y1 != y2)}",
        ],
        "delay": 600,
    }

    # Build the full vent map for visualization
    all_counts = Counter()
    for x1, y1, x2, y2 in segments:
        for point in points_on_line(x1, y1, x2, y2):
            all_counts[point] += 1

    if all_counts:
        max_x = max(x for x, y in all_counts)
        max_y = max(y for x, y in all_counts)
        # Downsample if too large
        scale = max(1, max(max_x, max_y) // 80 + 1)
        w = max_x // scale + 1
        h = max_y // scale + 1

        scaled = Counter()
        for (x, y), v in all_counts.items():
            scaled[(x // scale, y // scale)] += v

        cells = []
        for row in range(min(h, 80)):
            line = []
            for col in range(min(w, 120)):
                v = scaled.get((col, row), 0)
                if v == 0:
                    line.append(".")
                elif v == 1:
                    line.append("1")
                else:
                    line.append("#")
            cells.append(line)

        yield {
            "type": "grid",
            "cells": cells,
            "colors": {
                ".": "#0f0f23",
                "1": "#333355",
                "#": "#ff6666",
            },
            "delay": 800,
        }

    part1 = sum(1 for x1, y1, x2, y2 in segments if x1 == x2 or y1 == y2)
    hv_counts = Counter()
    for x1, y1, x2, y2 in segments:
        if x1 == x2 or y1 == y2:
            for point in points_on_line(x1, y1, x2, y2):
                hv_counts[point] += 1
    p1 = sum(1 for v in hv_counts.values() if v >= 2)
    p2 = sum(1 for v in all_counts.values() if v >= 2)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {p1} (H/V overlaps)",
            f"  Part 2: {p2} (all overlaps)",
        ],
        "delay": 500,
    }
