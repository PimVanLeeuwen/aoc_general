"""
Day 23 - Experimental Emergency Teleportation
Year: 2018

Part 1: Count nanobots in range of the strongest.
Part 2: Find point in range of most nanobots (closest to origin if tied),
using 3D spatial subdivision with a priority queue.
"""

import heapq
import re


def parse(puzzle_input):
    bots = []
    for line in puzzle_input.strip().splitlines():
        nums = list(map(int, re.findall(r'-?\d+', line)))
        bots.append((nums[0], nums[1], nums[2], nums[3]))
    return bots


def solve(puzzle_input: str) -> tuple[str, str]:
    bots = parse(puzzle_input)

    # Part 1: in range of strongest
    sx, sy, sz, sr = max(bots, key=lambda b: b[3])
    part1 = sum(1 for x, y, z, r in bots if abs(x-sx)+abs(y-sy)+abs(z-sz) <= sr)

    # Part 2: spatial subdivision
    # Find bounding box, round size up to power of 2
    coords = [(x, y, z) for x, y, z, r in bots]
    lo = [min(c[i] for c in coords) for i in range(3)]
    hi = [max(c[i] for c in coords) for i in range(3)]
    size = 1
    while size < max(hi[i] - lo[i] for i in range(3)):
        size *= 2

    def bots_in_range_of_box(bx, by, bz, sz):
        """Count bots whose range intersects the axis-aligned box [bx, bx+sz) etc."""
        count = 0
        for x, y, z, r in bots:
            # Manhattan distance from (x,y,z) to nearest point in box
            d = 0
            for val, blo in ((x, bx), (y, by), (z, bz)):
                if val < blo:
                    d += blo - val
                elif val >= blo + sz:
                    d += val - blo - sz + 1
            if d <= r:
                count += 1
        return count

    # Priority queue: (-num_bots, size, manhattan_to_origin, bx, by, bz)
    initial_count = bots_in_range_of_box(lo[0], lo[1], lo[2], size)
    origin_dist = sum(max(0, lo[i], -lo[i] - size + 1) for i in range(3))
    pq = [(-initial_count, size, origin_dist, lo[0], lo[1], lo[2])]

    while pq:
        neg_count, sz, od, bx, by, bz = heapq.heappop(pq)

        if sz == 1:
            part2 = abs(bx) + abs(by) + abs(bz)
            break

        half = sz // 2
        for dx in (0, half):
            for dy in (0, half):
                for dz in (0, half):
                    nx, ny, nz = bx + dx, by + dy, bz + dz
                    c = bots_in_range_of_box(nx, ny, nz, half)
                    if c > 0:
                        # Distance from origin to nearest point in sub-box
                        md = 0
                        for val, blo in ((0, nx), (0, ny), (0, nz)):
                            if val < blo:
                                md += blo
                            elif val >= blo + half:
                                md += val - blo - half + 1
                        heapq.heappush(pq, (-c, half, md, nx, ny, nz))

    return str(part1), str(part2)