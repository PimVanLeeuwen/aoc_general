"""
Day 17 - Pyroclastic Flow
Year: 2022

Simulate falling rocks in a narrow chamber and use cycle detection
to handle a trillion rocks.
"""

ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],          # horizontal bar
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],   # plus
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],   # L-shape
    [(0, 0), (0, 1), (0, 2), (0, 3)],            # vertical bar
    [(0, 0), (1, 0), (0, 1), (1, 1)],            # square
]


def simulate(jets, target):
    """Simulate rocks falling. Return tower height after target rocks."""
    filled = set()
    for x in range(7):
        filled.add((x, 0))

    height = 0
    jet_idx = 0
    seen = {}
    added_height = 0
    rock_num = 0

    while rock_num < target:
        rock_type = rock_num % 5
        rock = ROCKS[rock_type]

        # Spawn at left=2, bottom=height+4
        rx, ry = 2, height + 4

        while True:
            # Jet push
            dx = 1 if jets[jet_idx % len(jets)] == ">" else -1
            jet_idx += 1
            if all(
                0 <= rx + px + dx < 7 and (rx + px + dx, ry + py) not in filled
                for px, py in rock
            ):
                rx += dx

            # Fall
            if all((rx + px, ry + py - 1) not in filled for px, py in rock):
                ry -= 1
            else:
                for px, py in rock:
                    filled.add((rx + px, ry + py))
                    height = max(height, ry + py)
                break

        # Cycle detection using top profile
        if added_height == 0:
            profile = []
            for x in range(7):
                for dy in range(30):
                    if (x, height - dy) in filled:
                        profile.append(dy)
                        break
                else:
                    profile.append(30)

            state = (rock_type, jet_idx % len(jets), tuple(profile))
            if state in seen:
                prev_rock, prev_height = seen[state]
                cycle_len = rock_num - prev_rock
                cycle_height = height - prev_height
                remaining = target - rock_num - 1
                full_cycles = remaining // cycle_len
                added_height = full_cycles * cycle_height
                rock_num += full_cycles * cycle_len

            seen[state] = (rock_num, height)

        rock_num += 1

    return height + added_height


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    jets = puzzle_input.strip()

    part1 = simulate(jets, 2022)
    part2 = simulate(jets, 1_000_000_000_000)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the tower."""
    jets = puzzle_input.strip()

    yield {
        "type": "text",
        "lines": [
            "  Pyroclastic Flow",
            "",
            f"  Jet pattern length: {len(jets)}",
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
            f"  Part 1: {part1} (2022 rocks)",
            f"  Part 2: {part2} (1 trillion rocks)",
        ],
        "delay": 500,
    }
