"""
Day 6 - Tuning Trouble
Year: 2022

Find the first position where a sliding window of characters
contains all unique values — size 4 for part 1, size 14 for part 2.
"""


def find_marker(data, window_size):
    """Return the position after the first window of all-unique characters."""
    for i in range(window_size, len(data) + 1):
        if len(set(data[i - window_size : i])) == window_size:
            return i
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    data = puzzle_input.strip()

    part1 = find_marker(data, 4)
    part2 = find_marker(data, 14)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the sliding window search."""
    data = puzzle_input.strip()

    yield {
        "type": "text",
        "lines": [
            "  Tuning Trouble",
            "",
            f"  Signal length: {len(data)} characters",
            f"  First 60: {data[:60]}...",
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
            f"  Part 1: {part1} (4-char marker)",
            f"  Part 2: {part2} (14-char marker)",
        ],
        "delay": 500,
    }
