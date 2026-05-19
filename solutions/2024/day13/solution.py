"""
Day 13 - Claw Contraption
Year: 2024

Solve linear equations to find the minimum tokens needed
to reach each prize with two buttons (A costs 3, B costs 1).
"""

import re


def solve_machine(ax, ay, bx, by, px, py):
    """Solve the 2x2 system: ax*a + bx*b = px, ay*a + by*b = py.
    Returns the token cost (3*a + b) or 0 if no integer solution exists."""
    det = ax * by - ay * bx
    if det == 0:
        return 0

    # Cramer's rule
    a_num = px * by - py * bx
    b_num = ax * py - ay * px

    if a_num % det != 0 or b_num % det != 0:
        return 0

    a = a_num // det
    b = b_num // det

    if a < 0 or b < 0:
        return 0

    return 3 * a + b


def parse_machines(text):
    machines = []
    for block in text.strip().split("\n\n"):
        nums = list(map(int, re.findall(r"\d+", block)))
        machines.append((nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]))
    return machines


def solve(puzzle_input: str) -> tuple[str, str]:
    machines = parse_machines(puzzle_input)

    part1 = 0
    part2 = 0
    offset = 10000000000000

    for ax, ay, bx, by, px, py in machines:
        part1 += solve_machine(ax, ay, bx, by, px, py)
        part2 += solve_machine(ax, ay, bx, by, px + offset, py + offset)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    machines = parse_machines(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Claw Contraption",
            "",
            f"  Machines: {len(machines)}",
            "",
            "  Sample machine:",
            f"    Button A: X+{machines[0][0]}, Y+{machines[0][1]}",
            f"    Button B: X+{machines[0][2]}, Y+{machines[0][3]}",
            f"    Prize: X={machines[0][4]}, Y={machines[0][5]}",
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
            f"  Part 1: {part1} (tokens, nearby prizes)",
            f"  Part 2: {part2} (tokens, offset prizes)",
        ],
        "delay": 500,
    }
