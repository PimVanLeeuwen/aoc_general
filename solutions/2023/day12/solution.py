"""
Day 12 - Hot Springs
Year: 2023

Count valid arrangements of damaged/operational springs
matching a pattern with unknowns.
"""

from functools import lru_cache


def count_arrangements(pattern, groups):
    """Count valid ways to fill '?' in pattern to match the group sizes."""

    @lru_cache(maxsize=None)
    def dp(pos, group_idx):
        # Consumed all groups — remaining chars must not be '#'
        if group_idx == len(groups):
            return 0 if "#" in pattern[pos:] else 1

        # Not enough characters left for remaining groups
        needed = sum(groups[group_idx:]) + (len(groups) - group_idx - 1)
        if pos + needed > len(pattern):
            return 0

        result = 0
        ch = pattern[pos]

        # Try treating current position as operational ('.')
        if ch in ".?":
            result += dp(pos + 1, group_idx)

        # Try starting a group of damaged springs here
        if ch in "#?":
            g = groups[group_idx]
            block = pattern[pos : pos + g]
            # Block must be all '#' or '?' (no '.' breaking it)
            if "." not in block:
                if pos + g == len(pattern):
                    # End of string — only valid if this is the last group
                    result += dp(pos + g, group_idx + 1)
                elif pattern[pos + g] != "#":
                    # Character after block must not be '#' (separator)
                    result += dp(pos + g + 1, group_idx + 1)

        return result

    return dp(0, 0)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    part1 = 0
    part2 = 0

    for line in puzzle_input.strip().split("\n"):
        pattern, groups_str = line.split()
        groups = tuple(int(x) for x in groups_str.split(","))

        part1 += count_arrangements(pattern, groups)

        # Part 2: unfold 5 times
        pattern5 = "?".join([pattern] * 5)
        groups5 = groups * 5
        part2 += count_arrangements(pattern5, groups5)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing spring arrangement counting."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Hot Springs",
            "",
            f"  Spring rows: {len(lines)}",
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
            f"  Part 1: {part1} (original)",
            f"  Part 2: {part2} (unfolded 5x)",
        ],
        "delay": 500,
    }
