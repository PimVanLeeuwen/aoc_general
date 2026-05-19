"""
Day 1 - Trebuchet?!
Year: 2023

Extract calibration values from lines by finding the first
and last digit, including spelled-out digits in part 2.
"""

WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9",
}


def calibration_value(line, use_words=False):
    """Find first and last digit in the line."""
    digits = []
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(line[i])
        elif use_words:
            for word, val in WORDS.items():
                if line[i:].startswith(word):
                    digits.append(val)
                    break
    if not digits:
        return 0
    return int(digits[0] + digits[-1])


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    part1 = sum(calibration_value(line) for line in lines)
    part2 = sum(calibration_value(line, use_words=True) for line in lines)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing calibration extraction."""
    lines = puzzle_input.strip().split("\n")

    sample = lines[:5]
    text_lines = ["  Trebuchet?!", ""]
    for line in sample:
        v1 = calibration_value(line)
        v2 = calibration_value(line, use_words=True)
        text_lines.append(f"  {line[:30]:30s} → {v1:3d} / {v2:3d}")

    yield {"type": "text", "lines": text_lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (digits only)",
            f"  Part 2: {part2} (with word digits)",
        ],
        "delay": 500,
    }
