"""
Day 10 - Cathode-Ray Tube
Year: 2022

Simulate a simple CPU to compute signal strengths and
render a CRT display based on sprite position.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    x = 1
    cycle = 0
    signal_sum = 0
    crt = []
    row = []

    def tick():
        nonlocal cycle, signal_sum
        pixel = cycle % 40
        row.append("#" if abs(x - pixel) <= 1 else ".")
        cycle += 1
        if cycle % 40 == 0:
            crt.append("".join(row))
            row.clear()
        if cycle % 40 == 20:
            signal_sum += cycle * x

    for line in puzzle_input.strip().split("\n"):
        if line == "noop":
            tick()
        else:
            tick()
            tick()
            x += int(line.split()[1])

    part2 = "\n".join(crt)

    return str(signal_sum), part2


def visualize(puzzle_input: str):
    """Yield frames showing CRT output."""
    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Cathode-Ray Tube",
            "",
            f"  Signal strength sum: {part1}",
        ],
        "delay": 600,
    }

    crt_lines = part2.split("\n")
    cells = [list(line) for line in crt_lines if line]

    if cells:
        yield {
            "type": "grid",
            "cells": cells,
            "colors": {"#": "#00ff41", ".": "#0f0f23"},
            "delay": 600,
        }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  CRT Output",
            "  ===================================",
            "",
        ]
        + [f"  {line}" for line in crt_lines if line],
        "delay": 500,
    }
