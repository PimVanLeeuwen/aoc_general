"""
Day 17 - Trick Shot
Year: 2021

Launch a probe toward a target area. Find the highest trajectory
that still hits, and count all valid initial velocities.
"""

import re


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    x1, x2, y1, y2 = map(int, re.findall(r"-?\d+", puzzle_input))

    best_y = 0
    count = 0

    # vx range: 0 to x2 (beyond x2, first step overshoots)
    # vy range: y1 to -y1 (beyond -y1, first step below target after apex)
    for vx0 in range(x2 + 1):
        for vy0 in range(y1, -y1 + 1):
            x, y = 0, 0
            vx, vy = vx0, vy0
            max_y = 0

            while x <= x2 and y >= y1:
                x += vx
                y += vy
                max_y = max(max_y, y)
                vx -= (vx > 0) - (vx < 0)
                vy -= 1

                if x1 <= x <= x2 and y1 <= y <= y2:
                    best_y = max(best_y, max_y)
                    count += 1
                    break

    return str(best_y), str(count)


def visualize(puzzle_input: str):
    """Yield frames showing trajectory analysis."""
    x1, x2, y1, y2 = map(int, re.findall(r"-?\d+", puzzle_input))

    yield {
        "type": "text",
        "lines": [
            "  Trick Shot",
            "",
            f"  Target: x={x1}..{x2}, y={y1}..{y2}",
        ],
        "delay": 600,
    }

    best_y = 0
    count = 0

    for vx0 in range(x2 + 1):
        for vy0 in range(y1, -y1 + 1):
            x, y = 0, 0
            vx, vy = vx0, vy0
            max_y = 0

            while x <= x2 and y >= y1:
                x += vx
                y += vy
                max_y = max(max_y, y)
                vx -= (vx > 0) - (vx < 0)
                vy -= 1

                if x1 <= x <= x2 and y1 <= y <= y2:
                    best_y = max(best_y, max_y)
                    count += 1
                    break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {best_y} (max height)",
            f"  Part 2: {count} (valid velocities)",
        ],
        "delay": 500,
    }
