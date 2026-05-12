"""
Day 4 - Secure Container
Year: 2019

Count six-digit passwords in a range that have non-decreasing digits
and adjacent duplicates.
"""


def is_valid(n, strict=False):
    """Check if n meets the password criteria.

    strict=False: any adjacent pair of equal digits suffices.
    strict=True:  at least one run of exactly two equal digits required.
    """
    digits = str(n)
    # Non-decreasing check
    for i in range(len(digits) - 1):
        if digits[i + 1] < digits[i]:
            return False
    # Adjacent duplicate check
    if strict:
        i = 0
        while i < len(digits):
            run = 1
            while i + run < len(digits) and digits[i + run] == digits[i]:
                run += 1
            if run == 2:
                return True
            i += run
        return False
    else:
        return any(digits[i] == digits[i + 1] for i in range(len(digits) - 1))


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lo, hi = map(int, puzzle_input.strip().split("-"))

    part1 = sum(1 for n in range(lo, hi + 1) if is_valid(n))
    part2 = sum(1 for n in range(lo, hi + 1) if is_valid(n, strict=True))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the password search progress."""
    lo, hi = map(int, puzzle_input.strip().split("-"))
    total = hi - lo + 1

    yield {
        "type": "text",
        "lines": [
            "  Secure Container",
            "",
            f"  Range: {lo} - {hi}",
            f"  Candidates: {total:,}",
        ],
        "delay": 600,
    }

    count1 = 0
    count2 = 0
    examples_p1 = []
    examples_p2 = []
    step = max(1, total // 25)

    for i, n in enumerate(range(lo, hi + 1)):
        v1 = is_valid(n)
        v2 = is_valid(n, strict=True)
        if v1:
            count1 += 1
            if len(examples_p1) < 5:
                examples_p1.append(n)
        if v2:
            count2 += 1
            if len(examples_p2) < 5:
                examples_p2.append(n)

        if (i + 1) % step == 0:
            pct = (i + 1) * 100 // total
            bar_w = 30
            fill = (i + 1) * bar_w // total
            bar = "=" * fill + ">" + " " * (bar_w - fill - 1)

            yield {
                "type": "text",
                "lines": [
                    "  Scanning passwords...",
                    "",
                    f"  [{bar}] {pct}%",
                    "",
                    f"  Part 1 (any double):    {count1:>5}",
                    f"  Part 2 (exact double):  {count2:>5}",
                ],
                "delay": 60,
            }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {count1} passwords (any adjacent double)",
            f"    e.g. {', '.join(str(x) for x in examples_p1)}",
            "",
            f"  Part 2: {count2} passwords (exact double, no larger group)",
            f"    e.g. {', '.join(str(x) for x in examples_p2)}",
        ],
        "delay": 500,
    }
