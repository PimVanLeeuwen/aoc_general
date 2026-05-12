"""
Day 12 - The N-Body Problem
Year: 2019

Simulate gravity between four moons in 3D. Find total energy after 1000
steps, then find the cycle length by factoring into independent axes.
"""

import re
from math import gcd


def parse_moons(text):
    """Return list of [x, y, z] positions."""
    return [list(map(int, re.findall(r'-?\d+', line))) for line in text.strip().splitlines()]


def sign(x):
    return (x > 0) - (x < 0)


def simulate(positions, steps):
    """Simulate n steps, return (positions, velocities) after."""
    n = len(positions)
    pos = [list(p) for p in positions]
    vel = [[0, 0, 0] for _ in range(n)]

    for _ in range(steps):
        # Apply gravity
        for i in range(n):
            for j in range(i + 1, n):
                for axis in range(3):
                    d = sign(pos[j][axis] - pos[i][axis])
                    vel[i][axis] += d
                    vel[j][axis] -= d
        # Apply velocity
        for i in range(n):
            for axis in range(3):
                pos[i][axis] += vel[i][axis]

    return pos, vel


def total_energy(pos, vel):
    """Compute total energy: sum of (potential * kinetic) per moon."""
    total = 0
    for i in range(len(pos)):
        pot = sum(abs(p) for p in pos[i])
        kin = sum(abs(v) for v in vel[i])
        total += pot * kin
    return total


def find_axis_cycle(positions, axis):
    """Find the cycle length for a single axis."""
    n = len(positions)
    pos = [p[axis] for p in positions]
    vel = [0] * n
    initial = (tuple(pos), tuple(vel))

    step = 0
    while True:
        # Gravity
        for i in range(n):
            for j in range(i + 1, n):
                d = sign(pos[j] - pos[i])
                vel[i] += d
                vel[j] -= d
        # Velocity
        for i in range(n):
            pos[i] += vel[i]
        step += 1

        if (tuple(pos), tuple(vel)) == initial:
            return step


def lcm(a, b):
    return a * b // gcd(a, b)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    positions = parse_moons(puzzle_input)

    pos, vel = simulate(positions, 1000)
    part1 = total_energy(pos, vel)

    cx = find_axis_cycle(positions, 0)
    cy = find_axis_cycle(positions, 1)
    cz = find_axis_cycle(positions, 2)
    part2 = lcm(lcm(cx, cy), cz)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the moon simulation and cycle detection."""
    positions = parse_moons(puzzle_input)
    moon_names = ["Io", "Europa", "Ganymede", "Callisto"]

    yield {
        "type": "text",
        "lines": [
            "  The N-Body Problem — Jupiter's Moons",
            "",
        ] + [
            f"  {moon_names[i]:>10}: x={p[0]:>4}, y={p[1]:>4}, z={p[2]:>4}"
            for i, p in enumerate(positions)
        ],
        "delay": 600,
    }

    # Show simulation snapshots
    n = len(positions)
    pos = [list(p) for p in positions]
    vel = [[0, 0, 0] for _ in range(n)]

    for step in range(1, 1001):
        for i in range(n):
            for j in range(i + 1, n):
                for axis in range(3):
                    d = sign(pos[j][axis] - pos[i][axis])
                    vel[i][axis] += d
                    vel[j][axis] -= d
        for i in range(n):
            for axis in range(3):
                pos[i][axis] += vel[i][axis]

        if step in (1, 10, 100, 500, 1000):
            energy = total_energy(pos, vel)
            lines = [f"  After {step} steps:  (energy = {energy})", ""]
            for i in range(n):
                lines.append(
                    f"  {moon_names[i]:>10}: "
                    f"pos=({pos[i][0]:>4},{pos[i][1]:>4},{pos[i][2]:>4})  "
                    f"vel=({vel[i][0]:>4},{vel[i][1]:>4},{vel[i][2]:>4})"
                )
            yield {"type": "text", "lines": lines, "delay": 400}

    energy_1000 = total_energy(pos, vel)

    # Cycle detection
    cx = find_axis_cycle(positions, 0)
    cy = find_axis_cycle(positions, 1)
    cz = find_axis_cycle(positions, 2)
    full_cycle = lcm(lcm(cx, cy), cz)

    yield {
        "type": "text",
        "lines": [
            "  Cycle detection (per axis):",
            "",
            f"  X-axis cycle: {cx:>12,} steps",
            f"  Y-axis cycle: {cy:>12,} steps",
            f"  Z-axis cycle: {cz:>12,} steps",
            "",
            f"  LCM = {full_cycle:,} steps",
        ],
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {energy_1000} (energy after 1000 steps)",
            f"  Part 2: {full_cycle} (cycle length)",
        ],
        "delay": 500,
    }
