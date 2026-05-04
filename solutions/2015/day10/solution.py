"""
Day 10 - Elves Look, Elves Say
Year: 2015

Repeatedly apply the look-and-say transformation to a sequence of digits.
"""


def look_and_say(s: str) -> str:
    result = []
    i = 0
    while i < len(s):
        digit = s[i]
        count = 1
        while i + count < len(s) and s[i + count] == digit:
            count += 1
        result.append(str(count))
        result.append(digit)
        i += count
    return "".join(result)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    s = puzzle_input.strip()

    for _ in range(40):
        s = look_and_say(s)
    part1 = str(len(s))

    for _ in range(10):
        s = look_and_say(s)
    part2 = str(len(s))

    return part1, part2


def visualize(puzzle_input: str):
    """Yield visualization frames showing the look-and-say sequence growing."""
    s = puzzle_input.strip()
    max_display = 72

    lengths = [len(s)]
    sequences = [s]

    for i in range(50):
        s = look_and_say(s)
        lengths.append(len(s))
        sequences.append(s)

    max_len = max(lengths)
    bar_width = 50

    for i in range(len(lengths)):
        seq = sequences[i]
        display = seq if len(seq) <= max_display else seq[:max_display - 3] + "..."

        bar_fill = round(lengths[i] / max_len * bar_width)
        bar = "█" * bar_fill + "░" * (bar_width - bar_fill)

        lines = [
            f"  Iteration {i:>2} / 50",
            "",
            f"  Length: {lengths[i]:>8,}",
            "",
            f"  [{bar}]",
            "",
            f"  {display}",
        ]

        if i == 40:
            lines.append("")
            lines.append(f"  ★ Part 1 answer: {lengths[i]}")

        if i == 50:
            lines.append("")
            lines.append(f"  ★ Part 2 answer: {lengths[i]}")

        delay = 400 if i < 20 else 200 if i < 40 else 300
        yield {"type": "text", "lines": lines, "delay": delay}
