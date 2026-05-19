"""
Day 2 - Cube Conundrum
Year: 2023

Determine which games are possible with limited cubes,
and find the minimum required cubes per game.
"""


def parse_game(line):
    """Parse a game line into (game_id, list of {color: count} dicts)."""
    header, body = line.split(": ")
    game_id = int(header.split()[1])
    rounds = []
    for grab in body.split("; "):
        cubes = {}
        for part in grab.split(", "):
            count, color = part.strip().split()
            cubes[color] = int(count)
        rounds.append(cubes)
    return game_id, rounds


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    limits = {"red": 12, "green": 13, "blue": 14}
    part1 = 0
    part2 = 0

    for line in puzzle_input.strip().split("\n"):
        game_id, rounds = parse_game(line)

        # Part 1: check if game is possible
        possible = all(
            grab.get(color, 0) <= limit
            for grab in rounds
            for color, limit in limits.items()
        )
        if possible:
            part1 += game_id

        # Part 2: minimum cubes needed
        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for grab in rounds:
            for color, count in grab.items():
                min_cubes[color] = max(min_cubes[color], count)
        part2 += min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing game analysis."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Cube Conundrum",
            "",
            f"  Games: {len(lines)}",
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
            f"  Part 1: {part1} (possible game IDs)",
            f"  Part 2: {part2} (power of min sets)",
        ],
        "delay": 500,
    }
