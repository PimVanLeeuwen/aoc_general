"""
Day 14 - Restroom Redoubt
Year: 2024

Simulate robots moving on a toroidal grid. Part 1 counts
quadrants after 100 steps; part 2 finds the Easter egg frame.
"""

import re


WIDTH = 101
HEIGHT = 103


def parse_robots(text):
    robots = []
    for line in text.strip().split("\n"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        robots.append((nums[0], nums[1], nums[2], nums[3]))
    return robots


def simulate(robots, steps):
    """Return positions after given steps on the toroidal grid."""
    positions = []
    for x, y, vx, vy in robots:
        nx = (x + vx * steps) % WIDTH
        ny = (y + vy * steps) % HEIGHT
        positions.append((nx, ny))
    return positions


def safety_score(positions):
    mid_x, mid_y = WIDTH // 2, HEIGHT // 2
    q = [0, 0, 0, 0]
    for x, y in positions:
        if x < mid_x and y < mid_y:
            q[0] += 1
        elif x > mid_x and y < mid_y:
            q[1] += 1
        elif x < mid_x and y > mid_y:
            q[2] += 1
        elif x > mid_x and y > mid_y:
            q[3] += 1
    return q[0] * q[1] * q[2] * q[3]


def solve(puzzle_input: str) -> tuple[str, str]:
    robots = parse_robots(puzzle_input)

    # Part 1: safety score after 100 seconds
    positions = simulate(robots, 100)
    part1 = safety_score(positions)

    # Part 2: find the frame with lowest safety score (most clustered)
    min_score = float("inf")
    best_t = 0
    for t in range(1, WIDTH * HEIGHT + 1):
        pos = simulate(robots, t)
        score = safety_score(pos)
        if score < min_score:
            min_score = score
            best_t = t

    return str(part1), str(best_t)


def visualize(puzzle_input: str):
    robots = parse_robots(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Restroom Redoubt",
            "",
            f"  Robots: {len(robots)}",
            f"  Grid: {WIDTH} x {HEIGHT}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)
    t = int(part2)

    # Show the Easter egg frame
    positions = set(simulate(robots, t))
    display_rows = min(HEIGHT, 40)
    display_cols = min(WIDTH, 50)
    cells = []
    colors = {"#": "#00ff41", " ": "#0a0a0a"}

    for y in range(display_rows):
        row = []
        for x in range(display_cols):
            row.append("#" if (x, y) in positions else " ")
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 1000}

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (safety score at t=100)",
            f"  Part 2: {part2} (Easter egg frame)",
        ],
        "delay": 500,
    }
