"""
Day 08 - Seven Segment Searches
Year: 2021

Decode scrambled seven-segment displays by deducing the wire-to-segment
mapping from signal patterns.
"""

from itertools import permutations

# Standard segments for each digit (sorted)
DIGIT_SEGMENTS = {
    "abcefg": "0", "cf": "1", "acdeg": "2", "acdfg": "3",
    "bcdf": "4", "abdfg": "5", "abdefg": "6", "acf": "7",
    "abcdefg": "8", "abcdfg": "9",
}


def decode_display(patterns, outputs):
    """Find the wire mapping and decode the output digits."""
    # Try all permutations of wire-to-segment mappings
    for perm in permutations("abcdefg"):
        mapping = dict(zip(perm, "abcdefg"))

        valid = True
        for pattern in patterns:
            translated = "".join(sorted(mapping[c] for c in pattern))
            if translated not in DIGIT_SEGMENTS:
                valid = False
                break

        if valid:
            result = ""
            for output in outputs:
                translated = "".join(sorted(mapping[c] for c in output))
                result += DIGIT_SEGMENTS[translated]
            return int(result)

    return 0


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    part1 = 0
    part2 = 0

    for line in lines:
        left, right = line.split(" | ")
        patterns = left.split()
        outputs = right.split()

        # Part 1: count outputs with unique segment counts (1, 4, 7, 8)
        for output in outputs:
            if len(output) in (2, 3, 4, 7):
                part1 += 1

        # Part 2: decode each display
        part2 += decode_display(patterns, outputs)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing seven-segment decoding."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Seven Segment Searches",
            "",
            f"  Displays: {len(lines)}",
        ],
        "delay": 600,
    }

    part1 = 0
    part2 = 0
    decoded_samples = []

    for line in lines:
        left, right = line.split(" | ")
        patterns = left.split()
        outputs = right.split()

        for output in outputs:
            if len(output) in (2, 3, 4, 7):
                part1 += 1

        value = decode_display(patterns, outputs)
        part2 += value
        if len(decoded_samples) < 5:
            decoded_samples.append((" ".join(outputs), value))

    sample_lines = ["  Sample decodings:", ""]
    for outputs_str, value in decoded_samples:
        sample_lines.append(f"  {outputs_str} -> {value}")

    yield {
        "type": "text",
        "lines": sample_lines,
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (unique digit count)",
            f"  Part 2: {part2} (sum of decoded outputs)",
        ],
        "delay": 500,
    }
