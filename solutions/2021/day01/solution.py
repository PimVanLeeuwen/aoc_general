"""
Day 01 - Sonar Sweep
Year: 2021

Count depth measurement increases using sliding windows of size 1 and 3.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    depths = [int(x) for x in puzzle_input.strip().split("\n")]

    # Part 1: count single increases
    part1 = sum(depths[i] > depths[i - 1] for i in range(1, len(depths)))

    # Part 2: count sliding window (size 3) increases
    # Window sum increases iff the new element > the dropped element
    part2 = sum(depths[i] > depths[i - 3] for i in range(3, len(depths)))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing depth measurement analysis."""
    depths = [int(x) for x in puzzle_input.strip().split("\n")]

    part1 = sum(depths[i] > depths[i - 1] for i in range(1, len(depths)))
    part2 = sum(depths[i] > depths[i - 3] for i in range(3, len(depths)))

    # Show a depth profile as a grid
    sample = depths[:80]
    if sample:
        min_d = min(sample)
        max_d = max(sample)
        height = 30
        cells = []
        for row in range(height):
            line = []
            for col, d in enumerate(sample):
                threshold = max_d - (max_d - min_d) * row / (height - 1)
                if d >= threshold:
                    line.append("#")
                else:
                    line.append(".")
            cells.append(line)

        yield {
            "type": "grid",
            "cells": cells,
            "colors": {
                "#": "#0077cc",
                ".": "#0f0f23",
            },
            "delay": 800,
        }

    yield {
        "type": "text",
        "lines": [
            "  Sonar Sweep",
            "",
            f"  Measurements: {len(depths)}",
            f"  Depth range: {min(depths)} - {max(depths)}",
            "",
            f"  Part 1: {part1} (single increases)",
            f"  Part 2: {part2} (window-3 increases)",
        ],
        "delay": 500,
    }
