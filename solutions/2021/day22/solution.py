"""
Day 22 - Reactor Reboot
Year: 2021

Toggle cuboid regions on/off in 3D space. Use cuboid subtraction
to track disjoint "on" regions without brute-force voxel counting.
"""

import re


def volume(cuboid):
    """Compute the number of integer points in a cuboid."""
    x1, x2, y1, y2, z1, z2 = cuboid
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def intersect(a, b):
    """Return the intersection cuboid, or None if they don't overlap."""
    x1 = max(a[0], b[0])
    x2 = min(a[1], b[1])
    y1 = max(a[2], b[2])
    y2 = min(a[3], b[3])
    z1 = max(a[4], b[4])
    z2 = min(a[5], b[5])
    if x1 <= x2 and y1 <= y2 and z1 <= z2:
        return (x1, x2, y1, y2, z1, z2)
    return None


def subtract(a, b):
    """Subtract cuboid b from a. Return list of remaining cuboids."""
    overlap = intersect(a, b)
    if overlap is None:
        return [a]

    result = []
    x1, x2, y1, y2, z1, z2 = a
    ox1, ox2, oy1, oy2, oz1, oz2 = overlap

    # Slice off 6 faces around the intersection
    if x1 < ox1:
        result.append((x1, ox1 - 1, y1, y2, z1, z2))
    if ox2 < x2:
        result.append((ox2 + 1, x2, y1, y2, z1, z2))
    if y1 < oy1:
        result.append((ox1, ox2, y1, oy1 - 1, z1, z2))
    if oy2 < y2:
        result.append((ox1, ox2, oy2 + 1, y2, z1, z2))
    if z1 < oz1:
        result.append((ox1, ox2, oy1, oy2, z1, oz1 - 1))
    if oz2 < z2:
        result.append((ox1, ox2, oy1, oy2, oz2 + 1, z2))

    return result


def reboot(instructions, limit=None):
    """Process instructions and return total on-count."""
    on_cuboids = []

    for on, cuboid in instructions:
        if limit and (cuboid[0] > limit or cuboid[1] < -limit):
            continue

        # Subtract new cuboid from all existing on-cuboids
        new_on = []
        for existing in on_cuboids:
            new_on.extend(subtract(existing, cuboid))

        # If turning on, add the new cuboid
        if on:
            new_on.append(cuboid)

        on_cuboids = new_on

    return sum(volume(c) for c in on_cuboids)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    instructions = []
    for line in puzzle_input.strip().split("\n"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        on = line.startswith("on")
        instructions.append((on, tuple(nums)))

    part1 = reboot(instructions, limit=50)
    part2 = reboot(instructions)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing reactor reboot."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Reactor Reboot",
            "",
            f"  Instructions: {len(lines)}",
            f"  On steps: {sum(1 for l in lines if l.startswith('on'))}",
            f"  Off steps: {sum(1 for l in lines if l.startswith('off'))}",
        ],
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
            f"  Part 1: {part1} (init region)",
            f"  Part 2: {part2} (full reboot)",
        ],
        "delay": 500,
    }
