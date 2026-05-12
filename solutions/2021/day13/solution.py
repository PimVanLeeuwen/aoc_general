"""
Day 13 - Transparent Origami
Year: 2021

Fold a transparent paper with dots along horizontal and vertical lines
to reveal a code made of capital letters.
"""


def parse_input(text):
    """Parse dot positions and fold instructions."""
    dots_section, folds_section = text.strip().split("\n\n")

    dots = set()
    for line in dots_section.split("\n"):
        x, y = line.split(",")
        dots.add((int(x), int(y)))

    folds = []
    for line in folds_section.split("\n"):
        axis, value = line.split("=")
        folds.append((axis[-1], int(value)))

    return dots, folds


def fold(dots, axis, value):
    """Fold dots along the given axis at the given value."""
    new_dots = set()
    for x, y in dots:
        if axis == "x" and x > value:
            x = 2 * value - x
        elif axis == "y" and y > value:
            y = 2 * value - y
        new_dots.add((x, y))
    return new_dots


def render(dots):
    """Render dots as a list of strings."""
    max_x = max(x for x, y in dots)
    max_y = max(y for x, y in dots)
    lines = []
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "#" if (x, y) in dots else " "
        lines.append(line)
    return lines


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    dots, folds = parse_input(puzzle_input)

    # Part 1: dots after first fold
    dots_p1 = fold(dots, *folds[0])
    part1 = len(dots_p1)

    # Part 2: fold all, read the letters
    for axis, value in folds:
        dots = fold(dots, axis, value)

    part2 = "\n".join(render(dots))

    return str(part1), part2


def visualize(puzzle_input: str):
    """Yield frames showing paper folding."""
    dots, folds = parse_input(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Transparent Origami",
            "",
            f"  Dots: {len(dots)}",
            f"  Folds: {len(folds)}",
        ],
        "delay": 600,
    }

    for i, (axis, value) in enumerate(folds):
        dots = fold(dots, axis, value)
        if i == 0 or i == len(folds) - 1:
            max_x = max(x for x, y in dots)
            max_y = max(y for x, y in dots)

            cells = []
            for y in range(max_y + 1):
                row = []
                for x in range(max_x + 1):
                    row.append("#" if (x, y) in dots else ".")
                cells.append(row)

            yield {
                "type": "grid",
                "cells": cells,
                "colors": {
                    "#": "#00ff41",
                    ".": "#0f0f23",
                },
                "delay": 800,
            }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {len(fold(parse_input(puzzle_input)[0], *folds[0]))}",
            f"  Part 2: (see grid above)",
        ],
        "delay": 500,
    }
