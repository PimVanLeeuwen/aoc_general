"""
Day 15 - Rambunctious Recitation
Year: 2020

Play a memory game where each number spoken depends on when that number
was last spoken. Simulate to turns 2020 and 30,000,000.
"""


def play(starting, target):
    """Play the memory game up to the target turn, return the last number spoken."""
    last_seen = {}
    for i, n in enumerate(starting[:-1]):
        last_seen[n] = i

    prev = starting[-1]
    for turn in range(len(starting), target):
        if prev in last_seen:
            speak = turn - 1 - last_seen[prev]
        else:
            speak = 0
        last_seen[prev] = turn - 1
        prev = speak

    return prev


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    starting = [int(x) for x in puzzle_input.strip().split(",")]

    part1 = play(starting, 2020)
    part2 = play(starting, 30_000_000)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the memory game."""
    starting = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  Rambunctious Recitation",
            "",
            f"  Starting numbers: {', '.join(str(n) for n in starting)}",
            "",
            "  Playing memory game...",
        ],
        "delay": 600,
    }

    part1 = play(starting, 2020)

    yield {
        "type": "text",
        "lines": [
            f"  Turn 2020: {part1}",
            "",
            "  Continuing to turn 30,000,000...",
        ],
        "delay": 400,
    }

    part2 = play(starting, 30_000_000)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (turn 2,020)",
            f"  Part 2: {part2} (turn 30,000,000)",
        ],
        "delay": 500,
    }
