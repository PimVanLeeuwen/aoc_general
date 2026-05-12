"""
Day 10 - Syntax Scoring
Year: 2021

Score corrupted and incomplete lines of bracket expressions
using a stack-based parser.
"""

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
CORRUPT_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETE_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def analyze_line(line):
    """Parse a line and return either ('corrupt', char) or ('incomplete', stack)."""
    stack = []
    for ch in line:
        if ch in PAIRS:
            stack.append(ch)
        elif not stack or PAIRS[stack.pop()] != ch:
            return "corrupt", ch
    return "incomplete", stack


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    corrupt_score = 0
    completion_scores = []

    for line in lines:
        status, data = analyze_line(line)

        if status == "corrupt":
            corrupt_score += CORRUPT_SCORES[data]
        else:
            # Complete by closing remaining open brackets in reverse
            score = 0
            for ch in reversed(data):
                score = score * 5 + COMPLETE_SCORES[PAIRS[ch]]
            completion_scores.append(score)

    completion_scores.sort()
    part2 = completion_scores[len(completion_scores) // 2]

    return str(corrupt_score), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing syntax analysis."""
    lines = puzzle_input.strip().split("\n")

    corrupt_count = 0
    incomplete_count = 0
    corrupt_score = 0
    completion_scores = []

    for line in lines:
        status, data = analyze_line(line)
        if status == "corrupt":
            corrupt_count += 1
            corrupt_score += CORRUPT_SCORES[data]
        else:
            incomplete_count += 1
            score = 0
            for ch in reversed(data):
                score = score * 5 + COMPLETE_SCORES[PAIRS[ch]]
            completion_scores.append(score)

    yield {
        "type": "text",
        "lines": [
            "  Syntax Scoring",
            "",
            f"  Total lines: {len(lines)}",
            f"  Corrupted: {corrupt_count}",
            f"  Incomplete: {incomplete_count}",
        ],
        "delay": 600,
    }

    completion_scores.sort()
    part2 = completion_scores[len(completion_scores) // 2]

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {corrupt_score} (corruption score)",
            f"  Part 2: {part2} (middle completion score)",
            f"    Completion scores: {len(completion_scores)} values",
        ],
        "delay": 500,
    }
