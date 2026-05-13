"""
Day 18 - Boiling Boulders
Year: 2022

Count exposed surface area of a 3D lava droplet,
then exclude interior air pockets.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    cubes = set()
    for line in puzzle_input.strip().split("\n"):
        x, y, z = map(int, line.split(","))
        cubes.add((x, y, z))

    dirs = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

    # Part 1: total exposed faces
    part1 = 0
    for x, y, z in cubes:
        for dx, dy, dz in dirs:
            if (x + dx, y + dy, z + dz) not in cubes:
                part1 += 1

    # Part 2: only exterior faces (flood fill from outside)
    min_c = min(min(c) for c in cubes) - 1
    max_c = max(max(c) for c in cubes) + 1

    water = set()
    queue = deque([(min_c, min_c, min_c)])
    water.add((min_c, min_c, min_c))

    while queue:
        x, y, z = queue.popleft()
        for dx, dy, dz in dirs:
            nx, ny, nz = x + dx, y + dy, z + dz
            if min_c <= nx <= max_c and min_c <= ny <= max_c and min_c <= nz <= max_c:
                if (nx, ny, nz) not in cubes and (nx, ny, nz) not in water:
                    water.add((nx, ny, nz))
                    queue.append((nx, ny, nz))

    part2 = 0
    for x, y, z in cubes:
        for dx, dy, dz in dirs:
            if (x + dx, y + dy, z + dz) in water:
                part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing lava droplet stats."""
    cubes = set()
    for line in puzzle_input.strip().split("\n"):
        x, y, z = map(int, line.split(","))
        cubes.add((x, y, z))

    yield {
        "type": "text",
        "lines": [
            "  Boiling Boulders",
            "",
            f"  Lava cubes: {len(cubes)}",
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
            f"  Part 1: {part1} (total surface area)",
            f"  Part 2: {part2} (exterior only)",
        ],
        "delay": 500,
    }
