"""
Day 2 - Rock Paper Scissors
Year: 2022

Score a rock-paper-scissors tournament under two different
interpretations of the strategy guide.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    # Part 1: X=Rock, Y=Paper, Z=Scissors
    shape_score_1 = {"X": 1, "Y": 2, "Z": 3}
    outcome_1 = {
        ("A", "X"): 3, ("A", "Y"): 6, ("A", "Z"): 0,
        ("B", "X"): 0, ("B", "Y"): 3, ("B", "Z"): 6,
        ("C", "X"): 6, ("C", "Y"): 0, ("C", "Z"): 3,
    }

    # Part 2: X=Lose, Y=Draw, Z=Win
    outcome_score_2 = {"X": 0, "Y": 3, "Z": 6}
    shape_2 = {
        ("A", "X"): 3, ("A", "Y"): 1, ("A", "Z"): 2,
        ("B", "X"): 1, ("B", "Y"): 2, ("B", "Z"): 3,
        ("C", "X"): 2, ("C", "Y"): 3, ("C", "Z"): 1,
    }

    score1 = score2 = 0
    for line in puzzle_input.strip().split("\n"):
        opp, me = line.split()
        score1 += shape_score_1[me] + outcome_1[(opp, me)]
        score2 += outcome_score_2[me] + shape_2[(opp, me)]

    return str(score1), str(score2)


def visualize(puzzle_input: str):
    """Yield frames showing tournament results."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Rock Paper Scissors",
            "",
            f"  Rounds: {len(lines)}",
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
            f"  Part 1: {part1} (shape interpretation)",
            f"  Part 2: {part2} (outcome interpretation)",
        ],
        "delay": 500,
    }
