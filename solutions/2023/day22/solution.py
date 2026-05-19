"""
Day 22 - Sand Slabs
Year: 2023

Simulate 3D bricks falling and settling, then determine
which can be safely removed and chain reaction counts.
"""

from collections import deque


def parse_bricks(text):
    """Parse brick definitions as [(x1,y1,z1, x2,y2,z2), ...]."""
    bricks = []
    for line in text.split("\n"):
        a, b = line.split("~")
        coords = list(map(int, a.split(","))) + list(map(int, b.split(",")))
        bricks.append(tuple(coords))
    # Sort by lowest z
    bricks.sort(key=lambda b: min(b[2], b[5]))
    return bricks


def settle(bricks):
    """Drop all bricks to their resting positions. Return settled bricks."""
    # height_map[x][y] = highest occupied z
    settled = []
    height_map = {}

    for x1, y1, z1, x2, y2, z2 in bricks:
        # Find the highest point below this brick's footprint
        max_z = 0
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                max_z = max(max_z, height_map.get((x, y), 0))

        # Drop brick
        drop = min(z1, z2) - max_z - 1
        nz1, nz2 = z1 - drop, z2 - drop
        settled.append((x1, y1, nz1, x2, y2, nz2))

        # Update height map
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                height_map[(x, y)] = max(nz1, nz2)

    return settled


def build_support_graph(bricks):
    """Build maps of which bricks support which."""
    # Map (x,y,z) -> brick index for all occupied cells
    occupied = {}
    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    occupied[(x, y, z)] = i

    # supports[i] = set of bricks that i supports (sit on top of i)
    # supported_by[i] = set of bricks supporting i (below i)
    n = len(bricks)
    supports = [set() for _ in range(n)]
    supported_by = [set() for _ in range(n)]

    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        top_z = max(z1, z2)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                above = occupied.get((x, y, top_z + 1))
                if above is not None and above != i:
                    supports[i].add(above)
                    supported_by[above].add(i)

    return supports, supported_by


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    bricks = parse_bricks(puzzle_input.strip())
    settled = settle(bricks)
    supports, supported_by = build_support_graph(settled)
    n = len(settled)

    # Part 1: count bricks that can be safely removed
    # A brick can be removed if every brick it supports has at least one other support
    part1 = 0
    for i in range(n):
        can_remove = all(len(supported_by[j]) > 1 for j in supports[i])
        if can_remove:
            part1 += 1

    # Part 2: for each brick, count how many would fall if removed (chain reaction)
    part2 = 0
    for i in range(n):
        # BFS: remove brick i, see what falls
        falling = {i}
        queue = deque([i])
        while queue:
            brick = queue.popleft()
            for j in supports[brick]:
                if j not in falling and supported_by[j].issubset(falling):
                    falling.add(j)
                    queue.append(j)
        part2 += len(falling) - 1  # don't count the removed brick itself

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing brick settling."""
    bricks = parse_bricks(puzzle_input.strip())

    yield {
        "type": "text",
        "lines": [
            "  Sand Slabs",
            "",
            f"  Bricks: {len(bricks)}",
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
            f"  Part 1: {part1} (safe to remove)",
            f"  Part 2: {part2} (chain reaction sum)",
        ],
        "delay": 500,
    }
