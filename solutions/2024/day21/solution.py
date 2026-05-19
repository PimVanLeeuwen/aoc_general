"""
Day 21 - Keypad Conundrum
Year: 2024

Chain of robots pressing directional keypads to type codes
on a numeric keypad. Minimize total button presses.
"""

from functools import lru_cache
from collections import deque


NUMERIC_PAD = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    "0": (3, 1), "A": (3, 2),
}
NUMERIC_GAP = (3, 0)

DIR_PAD = {
    "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}
DIR_GAP = (0, 0)


def get_paths(start, end, gap):
    """Find all shortest paths between two positions, avoiding the gap."""
    sr, sc = start
    er, ec = end
    queue = deque([(sr, sc, "")])
    results = []
    best_len = float("inf")

    while queue:
        r, c, path = queue.popleft()

        if len(path) > best_len:
            break

        if (r, c) == (er, ec):
            results.append(path + "A")
            best_len = len(path)
            continue

        if (r, c) == gap:
            continue

        if r < er:
            queue.append((r + 1, c, path + "v"))
        elif r > er:
            queue.append((r - 1, c, path + "^"))
        if c < ec:
            queue.append((r, c + 1, path + ">"))
        elif c > ec:
            queue.append((r, c - 1, path + "<"))

    return results


@lru_cache(maxsize=None)
def min_presses_dir(start_key, end_key, depth):
    """Minimum presses to move from start_key to end_key on a directional pad at given depth."""
    if depth == 0:
        return 1  # just press the button directly

    paths = get_paths(DIR_PAD[start_key], DIR_PAD[end_key], DIR_GAP)
    best = float("inf")

    for path in paths:
        cost = 0
        prev = "A"
        for ch in path:
            cost += min_presses_dir(prev, ch, depth - 1)
            prev = ch
        best = min(best, cost)

    return best


def cost_for_code(code, num_dir_robots):
    """Total presses needed to type a code on the numeric pad through a chain of robots."""
    total = 0
    prev = "A"

    for ch in code:
        paths = get_paths(NUMERIC_PAD[prev], NUMERIC_PAD[ch], NUMERIC_GAP)
        best = float("inf")

        for path in paths:
            cost = 0
            prev_dir = "A"
            for d in path:
                cost += min_presses_dir(prev_dir, d, num_dir_robots)
                prev_dir = d
            best = min(best, cost)

        total += best
        prev = ch

    return total


def solve(puzzle_input: str) -> tuple[str, str]:
    codes = puzzle_input.strip().split("\n")

    part1 = 0
    part2 = 0

    for code in codes:
        numeric = int(code.replace("A", ""))
        part1 += cost_for_code(code, 2) * numeric
        part2 += cost_for_code(code, 25) * numeric

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    codes = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Keypad Conundrum",
            "",
            f"  Codes: {len(codes)}",
            "  " + ", ".join(codes),
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
            f"  Part 1: {part1} (2 dir robots)",
            f"  Part 2: {part2} (25 dir robots)",
        ],
        "delay": 500,
    }
