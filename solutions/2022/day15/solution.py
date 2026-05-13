"""
Day 15 - Beacon Exclusion Zone
Year: 2022

Use Manhattan distance to find positions where beacons cannot exist
and locate the one uncovered position.
"""

import re


def parse_sensors(text):
    """Parse sensor and beacon positions."""
    sensors = []
    for line in text.strip().split("\n"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        sx, sy, bx, by = nums
        dist = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, dist, bx, by))
    return sensors


def covered_ranges_at_row(sensors, row):
    """Return sorted, merged ranges of x-positions covered at the given row."""
    ranges = []
    for sx, sy, dist, _, _ in sensors:
        dy = abs(sy - row)
        if dy <= dist:
            dx = dist - dy
            ranges.append((sx - dx, sx + dx))
    ranges.sort()

    merged = []
    for lo, hi in ranges:
        if merged and lo <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sensors = parse_sensors(puzzle_input)

    # Auto-detect sample vs real input
    max_coord = max(max(abs(sx), abs(sy)) for sx, sy, _, _, _ in sensors)
    if max_coord <= 100:
        target_row, search_bound = 10, 20
    else:
        target_row, search_bound = 2_000_000, 4_000_000

    # Part 1: count positions in target_row that can't have a beacon
    ranges = covered_ranges_at_row(sensors, target_row)
    covered = sum(hi - lo + 1 for lo, hi in ranges)
    beacons_in_row = len({(bx, by) for _, _, _, bx, by in sensors if by == target_row})
    part1 = covered - beacons_in_row

    # Part 2: walk perimeter of each sensor at distance+1
    part2 = 0
    for sx, sy, dist, _, _ in sensors:
        d = dist + 1
        for delta in range(d + 1):
            for sign_x, sign_y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                x = sx + sign_x * delta
                y = sy + sign_y * (d - delta)
                if 0 <= x <= search_bound and 0 <= y <= search_bound:
                    if all(abs(x - s[0]) + abs(y - s[1]) > s[2] for s in sensors):
                        part2 = x * 4_000_000 + y
                        return str(part1), str(part2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing sensor coverage."""
    sensors = parse_sensors(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Beacon Exclusion Zone",
            "",
            f"  Sensors: {len(sensors)}",
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
            f"  Part 1: {part1} (excluded positions)",
            f"  Part 2: {part2} (tuning frequency)",
        ],
        "delay": 500,
    }
