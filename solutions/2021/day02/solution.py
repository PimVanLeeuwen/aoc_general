"""
Day 02 - Dive!
Year: 2021

Follow submarine navigation commands to compute final position,
first with simple movement then with aim-based movement.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    commands = []
    for line in puzzle_input.strip().split("\n"):
        direction, amount = line.split()
        commands.append((direction, int(amount)))

    # Part 1: simple movement
    x, depth = 0, 0
    for direction, amount in commands:
        if direction == "forward":
            x += amount
        elif direction == "down":
            depth += amount
        elif direction == "up":
            depth -= amount
    part1 = x * depth

    # Part 2: aim-based movement
    x, depth, aim = 0, 0, 0
    for direction, amount in commands:
        if direction == "forward":
            x += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
    part2 = x * depth

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing submarine movement."""
    commands = []
    for line in puzzle_input.strip().split("\n"):
        direction, amount = line.split()
        commands.append((direction, int(amount)))

    yield {
        "type": "text",
        "lines": [
            "  Dive!",
            "",
            f"  Commands: {len(commands)}",
            f"  Forward: {sum(a for d, a in commands if d == 'forward')}",
            f"  Down: {sum(a for d, a in commands if d == 'down')}",
            f"  Up: {sum(a for d, a in commands if d == 'up')}",
        ],
        "delay": 600,
    }

    # Trace part 2 path at intervals
    x, depth, aim = 0, 0, 0
    path = [(x, depth)]
    for direction, amount in commands:
        if direction == "forward":
            x += amount
            depth += aim * amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
        path.append((x, depth))

    part1_x, part1_d = 0, 0
    for d, a in commands:
        if d == "forward":
            part1_x += a
        elif d == "down":
            part1_d += a
        elif d == "up":
            part1_d -= a

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1_x * part1_d}",
            f"    Position: ({part1_x}, {part1_d})",
            "",
            f"  Part 2: {x * depth}",
            f"    Position: ({x}, {depth})",
            f"    Final aim: {aim}",
        ],
        "delay": 500,
    }
