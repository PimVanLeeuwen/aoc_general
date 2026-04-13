"""
Day 14 - Disk Defragmentation
Year: 2017

Part 1: Count used squares in the 128x128 grid.
Part 2: Count connected regions of used squares.
"""

def knot_hash(s):
    nums = list(range(256))
    lengths = [ord(c) for c in s] + [17, 31, 73, 47, 23]

    pos = skip = 0
    n = 256

    for _ in range(64):
        # copied from day 10
        for length in lengths:
            idxs = [(pos + i) % n for i in range(length)]
            vals = [nums[i] for i in idxs][::-1]
            for i, v in zip(idxs, vals):
                nums[i] = v
            pos = (pos + length + skip) % n
            skip += 1

    dense = []
    for i in range(0, 256, 16):
        x = 0
        for v in nums[i:i+16]:
            x ^= v
        dense.append(x)

    return "".join(f"{x:02x}" for x in dense)


def solve(puzzle_input: str) -> tuple[str, str]:
    key = puzzle_input.strip()

    grid = []

    # Build 128x128 grid
    for row in range(128):
        h = knot_hash(f"{key}-{row}")
        bits = "".join(f"{int(c, 16):04b}" for c in h)
        grid.append(list(bits))

    # Part 1: count used squares
    part1 = sum(row.count("1") for row in grid)

    # Part 2: count regions using DFS
    visited = [[False]*128 for _ in range(128)]

    def dfs(r, c):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if not (0 <= x < 128 and 0 <= y < 128):
                continue
            if visited[x][y] or grid[x][y] == "0":
                continue
            visited[x][y] = True
            stack.extend([(x+1,y), (x-1,y), (x,y+1), (x,y-1)])

    regions = 0
    for r in range(128):
        for c in range(128):
            if grid[r][c] == "1" and not visited[r][c]:
                dfs(r, c)
                regions += 1

    return str(part1), str(regions)

def visualize(puzzle_input: str):
    """Visualize grid construction and region-filling for Day 14 with fixed-size frames."""
    key = puzzle_input.strip()

    # Start with a full 128x128 placeholder grid
    grid = [["."] * 128 for _ in range(128)]

    def hex_to_bits(h):
        return "".join(f"{int(c, 16):04b}" for c in h)

    # --- Phase 1: Build grid row by row ---
    for row in range(128):
        h = knot_hash(f"{key}-{row}")
        bits = hex_to_bits(h)

        # Fill the row into the fixed-size grid
        for col, b in enumerate(bits):
            grid[row][col] = "#" if b == "1" else "."

        # Emit frame with full 128x128 grid (but only rows 0..row are real)
        yield {
            "type": "grid",
            "cells": grid,
            "colors": {
                "#": "#00ff41",
                ".": "#0f0f23"
            },
            "text": [
                "Building disk grid...",
                f"Row {row+1}/128",
                f"Used squares so far: {sum(r.count('#') for r in grid)}"
            ],
            "delay": 40
        }

    # --- Phase 2: Region detection ---
    visited = [[False]*128 for _ in range(128)]

    region_colors = [
        "#ff0040", "#ff7f00", "#ffff00", "#7fff00", "#00ff7f",
        "#00ffff", "#007fff", "#7f00ff", "#ff00ff"
    ]

    def dfs(r, c, region_id):
        stack = [(r, c)]
        region_cells = []

        while stack:
            x, y = stack.pop()
            if not (0 <= x < 128 and 0 <= y < 128):
                continue
            if visited[x][y] or grid[x][y] == ".":
                continue

            visited[x][y] = True
            region_cells.append((x, y))

            stack.extend([(x+1,y), (x-1,y), (x,y+1), (x,y-1)])

            # Build a display grid with highlighted region
            display = []
            for rr in range(128):
                row_display = []
                for cc in range(128):
                    if (rr, cc) in region_cells:
                        row_display.append("#")
                    else:
                        row_display.append(grid[rr][cc])
                display.append(row_display)

            yield {
                "type": "grid",
                "cells": display,
                "colors": {
                    "#": region_colors[region_id % len(region_colors)],
                    ".": "#0f0f23"
                },
                "text": [
                    "Detecting regions...",
                    f"Current region: {region_id + 1}",
                    f"Cells in this region: {len(region_cells)}"
                ],
                "delay": 10
            }

    region_count = 0
    for r in range(128):
        for c in range(128):
            if grid[r][c] == "#" and not visited[r][c]:
                for frame in dfs(r, c, region_count):
                    yield frame
                region_count += 1

    # Final summary
    yield {
        "type": "text",
        "lines": [
            "Disk Defragmentation Complete",
            f"Total used squares: {sum(row.count('#') for row in grid)}",
            f"Total regions: {region_count}"
        ],
        "delay": 500
    }
