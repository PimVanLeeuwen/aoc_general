"""
Day 17 - Clumsy Crucible
Year: 2023

Find the minimum heat loss path through a city grid with
constraints on how many consecutive steps in one direction.
"""

import heapq


def min_heat_loss(grid, min_straight, max_straight):
    """Dijkstra with direction constraints."""
    rows, cols = len(grid), len(grid[0])
    # State: (heat_loss, row, col, dir_r, dir_c, steps_in_direction)
    # Start: can go right or down from (0,0)
    start_states = [
        (0, 0, 0, 0, 1, 0),  # facing right, 0 steps taken
        (0, 0, 0, 1, 0, 0),  # facing down, 0 steps taken
    ]
    dist = {}
    heap = start_states[:]
    heapq.heapify(heap)

    while heap:
        cost, r, c, dr, dc, steps = heapq.heappop(heap)

        key = (r, c, dr, dc, steps)
        if key in dist:
            continue
        dist[key] = cost

        if r == rows - 1 and c == cols - 1 and steps >= min_straight:
            return cost

        # Continue straight (if under max)
        if steps < max_straight:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                ncost = cost + grid[nr][nc]
                nkey = (nr, nc, dr, dc, steps + 1)
                if nkey not in dist:
                    heapq.heappush(heap, (ncost, nr, nc, dr, dc, steps + 1))

        # Turn left or right (if at least min_straight steps taken)
        if steps >= min_straight:
            for ndr, ndc in [(-dc, dr), (dc, -dr)]:
                nr, nc = r + ndr, c + ndc
                if 0 <= nr < rows and 0 <= nc < cols:
                    ncost = cost + grid[nr][nc]
                    nkey = (nr, nc, ndr, ndc, 1)
                    if nkey not in dist:
                        heapq.heappush(heap, (ncost, nr, nc, ndr, ndc, 1))

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [[int(ch) for ch in line] for line in puzzle_input.strip().split("\n")]

    part1 = min_heat_loss(grid, 1, 3)
    part2 = min_heat_loss(grid, 4, 10)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing heat loss grid."""
    grid = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Clumsy Crucible",
            "",
            f"  Grid: {len(grid)}x{len(grid[0])}",
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
            f"  Part 1: {part1} (crucible, max 3)",
            f"  Part 2: {part2} (ultra, min 4 max 10)",
        ],
        "delay": 500,
    }
