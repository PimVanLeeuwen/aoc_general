"""
Day 9 - Rope Bridge
Year: 2022

Simulate a rope with multiple knots following the head's movements.
"""


def simulate(moves, knot_count):
    """Simulate a rope with knot_count knots, return positions visited by the tail."""
    knots = [[0, 0] for _ in range(knot_count)]
    visited = {(0, 0)}

    directions = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}

    for line in moves:
        d, n = line.split()
        dx, dy = directions[d]

        for _ in range(int(n)):
            knots[0][0] += dx
            knots[0][1] += dy

            for i in range(1, knot_count):
                diff_x = knots[i - 1][0] - knots[i][0]
                diff_y = knots[i - 1][1] - knots[i][1]

                if abs(diff_x) <= 1 and abs(diff_y) <= 1:
                    break

                if abs(diff_x) >= 2:
                    diff_x //= abs(diff_x)
                if abs(diff_y) >= 2:
                    diff_y //= abs(diff_y)

                knots[i][0] += diff_x
                knots[i][1] += diff_y

            visited.add((knots[-1][0], knots[-1][1]))

    return visited


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    moves = puzzle_input.strip().split("\n")

    part1 = len(simulate(moves, 2))
    part2 = len(simulate(moves, 10))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing rope tail positions."""
    moves = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Rope Bridge",
            "",
            f"  Move instructions: {len(moves)}",
        ],
        "delay": 600,
    }

    visited_2 = simulate(moves, 2)
    visited_10 = simulate(moves, 10)

    if len(visited_2) <= 2000:
        min_x = min(p[0] for p in visited_2)
        max_x = max(p[0] for p in visited_2)
        min_y = min(p[1] for p in visited_2)
        max_y = max(p[1] for p in visited_2)

        cells = []
        for y in range(max_y, min_y - 1, -1):
            row = []
            for x in range(min_x, max_x + 1):
                if (x, y) in visited_2:
                    row.append("#")
                else:
                    row.append(".")
            cells.append(row)

        yield {
            "type": "grid",
            "cells": cells,
            "colors": {"#": "#00ff41", ".": "#0f0f23"},
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
            f"  Part 1: {part1} (2-knot tail)",
            f"  Part 2: {part2} (10-knot tail)",
        ],
        "delay": 500,
    }
