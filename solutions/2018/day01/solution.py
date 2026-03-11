"""
Day 1 - Chronal Calibration
Year: 2018

Starting puzzle of 2018
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    part1 = sum(int(x) for x in lines)

    freq = 0
    seen = {0}
    part2 = None
    while part2 is None:
        for line in lines:
            freq += int(line)
            if freq in seen:
                part2 = freq
                break
            seen.add(freq)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Animate the frequency accumulation and first repeated frequency search."""
    deltas = [int(x) for x in puzzle_input.strip().split("\n")]

    freq = 0
    seen = {0}
    step = 0
    cycle = 0
    found = None

    while found is None:
        cycle += 1
        for delta in deltas:
            step += 1
            freq += delta
            if freq in seen:
                found = freq
                break
            seen.add(freq)

        yield {
            "type": "text",
            "lines": [
                f"  Cycle:     {cycle:>8}",
                f"  Steps:     {step:>8}",
                f"  Frequency: {freq:>8}",
                f"  Seen:      {len(seen):>8} unique values",
                f"",
                f"" if found is None else f"  First repeat: {found}",
            ],
            "delay": 100,
        }
