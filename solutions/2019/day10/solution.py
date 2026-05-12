"""
Day 10 - Monitoring Station
Year: 2019

Find the asteroid with the best line-of-sight to other asteroids,
then simulate a rotating laser vaporizing them in order.
"""

from math import gcd, atan2, pi
from collections import defaultdict


def parse_asteroids(text):
    """Return set of (x, y) asteroid positions."""
    asteroids = set()
    for y, line in enumerate(text.strip().splitlines()):
        for x, ch in enumerate(line):
            if ch == '#':
                asteroids.add((x, y))
    return asteroids


def visible_count(station, asteroids):
    """Count how many asteroids are visible from station (unique angles)."""
    directions = set()
    sx, sy = station
    for ax, ay in asteroids:
        if (ax, ay) == station:
            continue
        dx, dy = ax - sx, ay - sy
        g = gcd(abs(dx), abs(dy))
        directions.add((dx // g, dy // g))
    return len(directions)


def find_best(asteroids):
    """Return (best_position, visible_count)."""
    best = max(asteroids, key=lambda a: visible_count(a, asteroids))
    return best, visible_count(best, asteroids)


def laser_angle(dx, dy):
    """Angle from straight up, going clockwise. Range [0, 2*pi)."""
    # atan2 gives angle from positive x-axis, counterclockwise
    # We want angle from negative y-axis (up), clockwise
    angle = atan2(dx, -dy)
    if angle < 0:
        angle += 2 * pi
    return angle


def vaporize_order(station, asteroids):
    """Return asteroids in laser vaporization order."""
    sx, sy = station

    # Group by normalized direction, sorted by distance within each group
    groups = defaultdict(list)
    for ax, ay in asteroids:
        if (ax, ay) == station:
            continue
        dx, dy = ax - sx, ay - sy
        g = gcd(abs(dx), abs(dy))
        key = (dx // g, dy // g)
        dist = abs(dx) + abs(dy)
        groups[key].append((dist, ax, ay))

    # Sort each group by distance (closest first)
    for key in groups:
        groups[key].sort()

    # Sort directions by laser angle
    sorted_dirs = sorted(groups.keys(), key=lambda d: laser_angle(d[0], d[1]))

    # Sweep: vaporize closest in each direction, repeat
    order = []
    remaining = dict(groups)
    while remaining:
        for d in sorted_dirs:
            if d in remaining and remaining[d]:
                _, ax, ay = remaining[d].pop(0)
                order.append((ax, ay))
                if not remaining[d]:
                    del remaining[d]
    return order


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    asteroids = parse_asteroids(puzzle_input)

    best, count = find_best(asteroids)
    part1 = count

    order = vaporize_order(best, asteroids)
    target = order[199]
    part2 = target[0] * 100 + target[1]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the laser vaporizing asteroids."""
    asteroids = parse_asteroids(puzzle_input)
    lines = puzzle_input.strip().splitlines()
    h = len(lines)
    w = len(lines[0])

    best, count = find_best(asteroids)
    order = vaporize_order(best, asteroids)

    yield {
        "type": "text",
        "lines": [
            "  Monitoring Station",
            "",
            f"  Asteroids: {len(asteroids)}",
            f"  Best station: {best} — sees {count} asteroids",
        ],
        "delay": 600,
    }

    # Show vaporization as grid frames
    remaining = set(asteroids)
    remaining.discard(best)

    # Show key milestones
    milestones = {1, 2, 3, 10, 50, 100, 199, 200, 201, len(order)}
    # Also show every Nth for animation
    anim_step = max(1, len(order) // 30)

    for i, (ax, ay) in enumerate(order):
        remaining.discard((ax, ay))
        n = i + 1

        if n in milestones or n % anim_step == 0:
            cells = []
            for row in range(h):
                r = []
                for col in range(w):
                    if (col, row) == best:
                        r.append("X")
                    elif (col, row) == (ax, ay):
                        r.append("*")
                    elif (col, row) in remaining:
                        r.append("#")
                    else:
                        r.append(".")
                cells.append(r)

            yield {
                "type": "grid",
                "cells": cells,
                "colors": {
                    ".": "#0f0f23",
                    "#": "#666688",
                    "X": "#00ff41",
                    "*": "#ff4444",
                },
                "delay": 200 if n <= 10 else 80,
            }

    target = order[199]
    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {count} (visible from {best})",
            f"  Part 2: 200th vaporized = {target}",
            f"          {target[0]} * 100 + {target[1]} = {target[0]*100+target[1]}",
        ],
        "delay": 500,
    }
