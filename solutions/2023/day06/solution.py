"""
Day 6 - Wait For It
Year: 2023

Find how many ways you can hold the button to beat each boat race record.
"""

import math


def count_wins(time, record):
    """Count integer hold times that produce distance > record.

    Distance for hold h is h * (time - h). Solve h*(time-h) > record
    as a quadratic: h^2 - time*h + record < 0.
    """
    discriminant = time * time - 4 * record
    if discriminant <= 0:
        return 0
    sqrt_d = math.sqrt(discriminant)
    lo = (time - sqrt_d) / 2
    hi = (time + sqrt_d) / 2
    # Strictly greater than record, so exclude exact ties
    lo_int = int(math.floor(lo)) + 1
    hi_int = int(math.ceil(hi)) - 1
    return max(0, hi_int - lo_int + 1)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))

    # Part 1: product of wins per race
    part1 = 1
    for t, d in zip(times, distances):
        part1 *= count_wins(t, d)

    # Part 2: single race with concatenated numbers
    big_time = int("".join(str(t) for t in times))
    big_dist = int("".join(str(d) for d in distances))
    part2 = count_wins(big_time, big_dist)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing race analysis."""
    lines = puzzle_input.strip().split("\n")
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))

    text_lines = ["  Wait For It", ""]
    for i, (t, d) in enumerate(zip(times, distances)):
        w = count_wins(t, d)
        text_lines.append(f"  Race {i + 1}: time={t}, record={d}, wins={w}")

    yield {"type": "text", "lines": text_lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (product of wins)",
            f"  Part 2: {part2} (single big race)",
        ],
        "delay": 500,
    }
