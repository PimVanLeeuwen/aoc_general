"""
Day 3 - Crossed Wires
Year: 2019

Trace two wires on a grid and find their intersections — closest by
Manhattan distance, then by fewest combined steps.
"""

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def trace_wire(path):
    """Return dict mapping each visited point to the step count when first reached."""
    visited = {}
    x, y, steps = 0, 0, 0
    for segment in path.split(","):
        dx, dy = DIRS[segment[0]]
        length = int(segment[1:])
        for _ in range(length):
            x += dx
            y += dy
            steps += 1
            if (x, y) not in visited:
                visited[(x, y)] = steps
    return visited


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().splitlines()
    wire1 = trace_wire(lines[0])
    wire2 = trace_wire(lines[1])

    crossings = wire1.keys() & wire2.keys()

    part1 = min(abs(x) + abs(y) for x, y in crossings)
    part2 = min(wire1[p] + wire2[p] for p in crossings)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the wires being traced on a grid."""
    lines = puzzle_input.strip().splitlines()
    wire1 = trace_wire(lines[0])
    wire2 = trace_wire(lines[1])
    crossings = wire1.keys() & wire2.keys()

    all_points = set(wire1.keys()) | set(wire2.keys())
    min_x = min(x for x, y in all_points)
    max_x = max(x for x, y in all_points)
    min_y = min(y for x, y in all_points)
    max_y = max(y for x, y in all_points)

    # Downsample if the grid is too large
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    scale = max(1, max(width, height) // 120)

    def downsample(points):
        return {(x // scale, y // scale) for x, y in points}

    w1_ds = downsample(wire1.keys())
    w2_ds = downsample(wire2.keys())
    cross_ds = downsample(crossings)
    origin_ds = (0 // scale, 0 // scale)

    ds_min_x = min(x for x, y in w1_ds | w2_ds)
    ds_max_x = max(x for x, y in w1_ds | w2_ds)
    ds_min_y = min(y for x, y in w1_ds | w2_ds)
    ds_max_y = max(y for x, y in w1_ds | w2_ds)

    grid_w = ds_max_x - ds_min_x + 1
    grid_h = ds_max_y - ds_min_y + 1

    # Cap grid size for the visualizer
    if grid_w > 150 or grid_h > 150:
        yield {
            "type": "text",
            "lines": [
                "  Crossed Wires",
                "",
                f"  Wire 1: {len(wire1):,} points",
                f"  Wire 2: {len(wire2):,} points",
                f"  Grid: {width} x {height} (too large for grid view)",
                "",
                f"  Intersections: {len(crossings)}",
                f"  Part 1 (min Manhattan): {min(abs(x)+abs(y) for x,y in crossings)}",
                f"  Part 2 (min steps): {min(wire1[p]+wire2[p] for p in crossings)}",
            ],
            "delay": 500,
        }
        return

    # Build the grid
    cells = []
    for gy in range(ds_max_y, ds_min_y - 1, -1):  # top to bottom
        row = []
        for gx in range(ds_min_x, ds_max_x + 1):
            p = (gx, gy)
            if p in cross_ds:
                row.append("X")
            elif p == origin_ds:
                row.append("o")
            elif p in w1_ds and p in w2_ds:
                row.append("X")
            elif p in w1_ds:
                row.append("1")
            elif p in w2_ds:
                row.append("2")
            else:
                row.append(".")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "1": "#00ff41",
            "2": "#4488ff",
            "X": "#ffff00",
            "o": "#ff4444",
        },
        "delay": 800,
    }

    best_manhattan = min(abs(x) + abs(y) for x, y in crossings)
    best_steps = min(wire1[p] + wire2[p] for p in crossings)
    best_m_point = min(crossings, key=lambda p: abs(p[0]) + abs(p[1]))
    best_s_point = min(crossings, key=lambda p: wire1[p] + wire2[p])

    yield {
        "type": "text",
        "lines": [
            "  Crossed Wires — Results",
            "",
            f"  Wire 1: {len(wire1):,} segments",
            f"  Wire 2: {len(wire2):,} segments",
            f"  Intersections: {len(crossings)}",
            "",
            f"  Part 1: closest by Manhattan distance",
            f"    Point {best_m_point}, distance = {best_manhattan}",
            "",
            f"  Part 2: fewest combined steps",
            f"    Point {best_s_point}, steps = {wire1[best_s_point]} + {wire2[best_s_point]} = {best_steps}",
        ],
        "delay": 500,
    }
