"""
Day 03 - No Matter How You Slice It 
Year: 2018

Determine how many square inches of fabric are within two or more claims, and find the only claim that doesn't overlap any other.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    import re
    claims = []
    for line in lines:
        # Example: #123 @ 3,2: 5x4
        if not line:
            continue
        m = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        if m:
            claim_id, left, top, width, height = map(int, m.groups())
            claims.append((claim_id, left, top, width, height))

    fabric = {}
    for claim_id, left, top, width, height in claims:
        for x in range(left, left + width):
            for y in range(top, top + height):
                if (x, y) not in fabric:
                    fabric[(x, y)] = []
                fabric[(x, y)].append(claim_id)

    # Part 1: Count squares with 2+ claims
    part1 = sum(1 for v in fabric.values() if len(v) > 1)

    # Part 2: Find claim with no overlap
    overlapping = set()
    for v in fabric.values():
        if len(v) > 1:
            overlapping.update(v)
    all_ids = set(c[0] for c in claims)
    non_overlapping = all_ids - overlapping
    part2 = str(next(iter(non_overlapping))) if non_overlapping else ""

    return str(part1), part2


def visualize(puzzle_input: str):
    """Yield visualization frames for Day 03."""
    lines = puzzle_input.strip().split("\n")
    import re
    claims = []
    for line in lines:
        m = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        if m:
            claim_id, left, top, width, height = map(int, m.groups())
            claims.append((claim_id, left, top, width, height))

    # Fixed 20x20 grid for consistent visualization
    grid_size = 20
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    fabric = {}
    
    step = 0
    total_claims = len(claims)
    show_every = max(1, total_claims // 30)  # Show at most 30 steps
    
    for claim_id, left, top, width, height in claims:
        step += 1
        
        # Mark fabric for overlap detection
        for x in range(left, left + width):
            for y in range(top, top + height):
                if (x, y) not in fabric:
                    fabric[(x, y)] = []
                fabric[(x, y)].append(claim_id)
        
        # Update visualization grid (scaled down for preview)
        for x in range(left, left + width):
            for y in range(top, top + height):
                gx, gy = x // 50, y // 50  # Scale down by 50 for preview
                if 0 <= gx < grid_size and 0 <= gy < grid_size:
                    if len(fabric.get((x, y), [])) == 1:
                        grid[gy][gx] = str(claim_id % 10)
                    elif len(fabric.get((x, y), [])) > 1:
                        grid[gy][gx] = "X"
        
        if step == 1 or step % show_every == 0 or step == total_claims:
            yield {
                "type": "grid",
                "cells": [row[:] for row in grid],
                "colors": {".": "#0f0f23", "X": "#ff0041", "0": "#00ff41", "1": "#00aaff", "2": "#ffaa00", "3": "#aaff00", "4": "#ff00aa", "5": "#aa00ff", "6": "#00ffaa", "7": "#fffa00", "8": "#fa00ff", "9": "#00faaf"},
                "delay": 200,
            }

    # Find overlaps and non-overlapping claim
    overlapping = set()
    for v in fabric.values():
        if len(v) > 1:
            overlapping.update(v)
    all_ids = set(c[0] for c in claims)
    non_overlapping = all_ids - overlapping
    
    # Highlight non-overlapping claim with special color
    if non_overlapping:
        unique_claim = next(iter(non_overlapping))
        highlight_grid = [row[:] for row in grid]
        
        # Mark the unique claim with a special symbol
        for cid, left, top, width, height in claims:
            if cid == unique_claim:
                for x in range(left, left + width):
                    for y in range(top, top + height):
                        gx, gy = x // 50, y // 50
                        if 0 <= gx < grid_size and 0 <= gy < grid_size:
                            highlight_grid[gy][gx] = "*"
        
        yield {
            "type": "grid",
            "cells": highlight_grid,
            "colors": {".": "#0f0f23", "X": "#ff0041", "*": "#00ff00", "0": "#00ff41", "1": "#00aaff", "2": "#ffaa00", "3": "#aaff00", "4": "#ff00aa", "5": "#aa00ff", "6": "#00ffaa", "7": "#fffa00", "8": "#fa00ff", "9": "#00faaf"},
            "delay": 1000,
        }
    else:
        # Final state showing all overlaps
        yield {
            "type": "grid",
            "cells": [row[:] for row in grid],
            "colors": {".": "#0f0f23", "X": "#ff0041", "0": "#00ff41", "1": "#00aaff", "2": "#ffaa00", "3": "#aaff00", "4": "#ff00aa", "5": "#aa00ff", "6": "#00ffaa", "7": "#fffa00", "8": "#fa00ff", "9": "#00faaf"},
            "delay": 1000,
        }
