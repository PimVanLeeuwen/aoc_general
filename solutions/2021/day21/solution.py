"""
Day 21 - Dirac Dice
Year: 2021

Play a board game with a deterministic die, then count winning
universes with a quantum die using memoized recursion.
"""

from functools import lru_cache


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    p1_start = int(lines[0].split(": ")[1])
    p2_start = int(lines[1].split(": ")[1])

    # Part 1: deterministic 100-sided die
    pos = [p1_start, p2_start]
    scores = [0, 0]
    die = 1
    rolls = 0
    turn = 0

    while True:
        total = 0
        for _ in range(3):
            total += die
            die = die % 100 + 1
            rolls += 1
        pos[turn] = (pos[turn] - 1 + total) % 10 + 1
        scores[turn] += pos[turn]
        if scores[turn] >= 1000:
            part1 = min(scores) * rolls
            break
        turn = 1 - turn

    # Part 2: Dirac quantum die (rolls 1, 2, or 3)
    # All possible sums of 3 rolls and their frequencies
    dirac_rolls = {}
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                s = a + b + c
                dirac_rolls[s] = dirac_rolls.get(s, 0) + 1

    @lru_cache(maxsize=None)
    def count_wins(p1_pos, p2_pos, p1_score, p2_score, turn):
        if p1_score >= 21:
            return (1, 0)
        if p2_score >= 21:
            return (0, 1)

        total_w1, total_w2 = 0, 0
        for roll_sum, freq in dirac_rolls.items():
            if turn == 0:
                new_pos = (p1_pos - 1 + roll_sum) % 10 + 1
                w1, w2 = count_wins(new_pos, p2_pos, p1_score + new_pos, p2_score, 1)
            else:
                new_pos = (p2_pos - 1 + roll_sum) % 10 + 1
                w1, w2 = count_wins(p1_pos, new_pos, p1_score, p2_score + new_pos, 0)
            total_w1 += w1 * freq
            total_w2 += w2 * freq

        return total_w1, total_w2

    w1, w2 = count_wins(p1_start, p2_start, 0, 0, 0)
    part2 = max(w1, w2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing Dirac Dice."""
    lines = puzzle_input.strip().split("\n")
    p1_start = int(lines[0].split(": ")[1])
    p2_start = int(lines[1].split(": ")[1])

    yield {
        "type": "text",
        "lines": [
            "  Dirac Dice",
            "",
            f"  Player 1 starts at: {p1_start}",
            f"  Player 2 starts at: {p2_start}",
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
            f"  Part 1: {part1} (deterministic die)",
            f"  Part 2: {part2} (quantum die)",
        ],
        "delay": 500,
    }
