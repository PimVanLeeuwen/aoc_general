"""
Day 25 - Full of Hot Air
Year: 2022

Convert between SNAFU (balanced base-5) and decimal numbers.
"""

SNAFU_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
DIGIT_TO_SNAFU = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}


def snafu_to_decimal(s):
    """Convert a SNAFU string to a decimal integer."""
    result = 0
    for ch in s:
        result = result * 5 + SNAFU_DIGITS[ch]
    return result


def decimal_to_snafu(n):
    """Convert a decimal integer to a SNAFU string."""
    if n == 0:
        return "0"
    digits = []
    while n:
        rem = n % 5
        digits.append(DIGIT_TO_SNAFU[rem])
        if rem >= 3:
            n += 5 - rem
        n //= 5
    return "".join(reversed(digits))


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    total = sum(snafu_to_decimal(line) for line in puzzle_input.strip().split("\n"))
    part1 = decimal_to_snafu(total)
    return part1, "⭐"


def visualize(puzzle_input: str):
    """Yield frames showing SNAFU conversion."""
    lines = puzzle_input.strip().split("\n")

    sample = lines[:5]
    text_lines = ["  Full of Hot Air", ""]
    for s in sample:
        text_lines.append(f"  {s:>10} = {snafu_to_decimal(s)}")
    if len(lines) > 5:
        text_lines.append(f"  ... ({len(lines)} total)")

    yield {"type": "text", "lines": text_lines, "delay": 600}

    part1, _ = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (SNAFU sum)",
            "  Part 2: ⭐ (Day 25 only has one part)",
        ],
        "delay": 500,
    }
