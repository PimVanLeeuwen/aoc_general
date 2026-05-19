"""
Day 15 - Lens Library
Year: 2023

Compute HASH values for initialization steps and simulate
a lens box arrangement system.
"""


def holiday_hash(s):
    """Compute the HASH of a string."""
    val = 0
    for ch in s:
        val = (val + ord(ch)) * 17 % 256
    return val


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    steps = puzzle_input.strip().split(",")

    # Part 1: sum of HASH values
    part1 = sum(holiday_hash(step) for step in steps)

    # Part 2: HASHMAP lens arrangement
    boxes = [[] for _ in range(256)]  # each box is list of (label, focal_length)

    for step in steps:
        if "=" in step:
            label, focal = step.split("=")
            focal = int(focal)
            box_id = holiday_hash(label)
            # Replace existing lens or add new one
            for i, (lbl, _) in enumerate(boxes[box_id]):
                if lbl == label:
                    boxes[box_id][i] = (label, focal)
                    break
            else:
                boxes[box_id].append((label, focal))
        else:
            label = step[:-1]  # remove the '-'
            box_id = holiday_hash(label)
            boxes[box_id] = [(lbl, f) for lbl, f in boxes[box_id] if lbl != label]

    part2 = 0
    for b, box in enumerate(boxes):
        for slot, (_, focal) in enumerate(box):
            part2 += (b + 1) * (slot + 1) * focal

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing HASH computation."""
    steps = puzzle_input.strip().split(",")

    yield {
        "type": "text",
        "lines": [
            "  Lens Library",
            "",
            f"  Steps: {len(steps)}",
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
            f"  Part 1: {part1} (HASH sum)",
            f"  Part 2: {part2} (focusing power)",
        ],
        "delay": 500,
    }
