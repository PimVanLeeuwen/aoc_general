"""
Day 12 - Rain Risk
Year: 2020

Navigate a ship using movement instructions — first with direct heading,
then with a waypoint that rotates around the ship.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    instructions = [
        (line[0], int(line[1:])) for line in puzzle_input.strip().split("\n")
    ]

    # Part 1: ship with facing direction
    x, y = 0, 0
    dx, dy = 1, 0  # facing east
    for action, value in instructions:
        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x += value
        elif action == "W":
            x -= value
        elif action == "F":
            x += dx * value
            y += dy * value
        elif action == "L":
            for _ in range(value // 90):
                dx, dy = -dy, dx
        elif action == "R":
            for _ in range(value // 90):
                dx, dy = dy, -dx
    part1 = abs(x) + abs(y)

    # Part 2: waypoint-based navigation
    sx, sy = 0, 0
    wx, wy = 10, 1  # waypoint relative to ship
    for action, value in instructions:
        if action == "N":
            wy += value
        elif action == "S":
            wy -= value
        elif action == "E":
            wx += value
        elif action == "W":
            wx -= value
        elif action == "F":
            sx += wx * value
            sy += wy * value
        elif action == "L":
            for _ in range(value // 90):
                wx, wy = -wy, wx
        elif action == "R":
            for _ in range(value // 90):
                wx, wy = wy, -wx
    part2 = abs(sx) + abs(sy)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing ship navigation."""
    instructions = [
        (line[0], int(line[1:])) for line in puzzle_input.strip().split("\n")
    ]

    yield {
        "type": "text",
        "lines": [
            "  Rain Risk — Ship Navigation",
            "",
            f"  Instructions: {len(instructions)}",
            f"  Actions: {', '.join(sorted(set(a for a, _ in instructions)))}",
        ],
        "delay": 600,
    }

    # Run both parts
    x, y, dx, dy = 0, 0, 1, 0
    for action, value in instructions:
        if action == "N": y += value
        elif action == "S": y -= value
        elif action == "E": x += value
        elif action == "W": x -= value
        elif action == "F": x += dx * value; y += dy * value
        elif action == "L":
            for _ in range(value // 90): dx, dy = -dy, dx
        elif action == "R":
            for _ in range(value // 90): dx, dy = dy, -dx
    part1 = abs(x) + abs(y)

    sx, sy, wx, wy = 0, 0, 10, 1
    for action, value in instructions:
        if action == "N": wy += value
        elif action == "S": wy -= value
        elif action == "E": wx += value
        elif action == "W": wx -= value
        elif action == "F": sx += wx * value; sy += wy * value
        elif action == "L":
            for _ in range(value // 90): wx, wy = -wy, wx
        elif action == "R":
            for _ in range(value // 90): wx, wy = wy, -wx
    part2 = abs(sx) + abs(sy)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (direct heading)",
            f"    Final position: ({x}, {y})",
            "",
            f"  Part 2: {part2} (waypoint navigation)",
            f"    Final position: ({sx}, {sy})",
        ],
        "delay": 500,
    }
