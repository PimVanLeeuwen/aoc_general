"""
Day 02 - Inventory Management System
Year: 2018

"Wouldn't they have had enough fabric to fill several boxes in the warehouse? They'd be stored together, so the box IDs should be similar. Too bad it would take forever to search the warehouse for two similar box IDs..." They walk too far away to hear any more.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")


    part_1_checksum = [0, 0]
    for box in lines:
        count = {c: box.count(c) for c in set(box)}
        if 2 in count.values():
            part_1_checksum[0] += 1
        if 3 in count.values():
            part_1_checksum[1] += 1


    # Part 2
    part2 = ""
    for i, id1 in enumerate(lines):
        for j, id2 in enumerate(lines):
            if i == j:
                continue
            diffs = [k for k, (a, b) in enumerate(zip(id1, id2)) if a != b]
            if len(diffs) == 1:
                idx = diffs[0]
                part2 = id1[:idx] + id1[idx+1:]
                break
        if part2:
            break

    return str(part_1_checksum[0]*part_1_checksum[1]), part2


def visualize(puzzle_input: str):
    """Yield visualization frames for Day 02."""
    lines = puzzle_input.strip().split("\n")

    # Part 1: Animate checksum calculation
    part_1_checksum = [0, 0]
    for idx, box in enumerate(lines):
        count = {c: box.count(c) for c in set(box)}
        has_two = 2 in count.values()
        has_three = 3 in count.values()
        if has_two:
            part_1_checksum[0] += 1
        if has_three:
            part_1_checksum[1] += 1
        yield {
            "type": "text",
            "lines": [
                f"Box ID {idx+1}/{len(lines)}: {box}",
                f"Has two of any char: {'Yes' if has_two else 'No'}",
                f"Has three of any char: {'Yes' if has_three else 'No'}",
                f"Twos so far: {part_1_checksum[0]}",
                f"Threes so far: {part_1_checksum[1]}",
                f"Checksum so far: {part_1_checksum[0] * part_1_checksum[1]}",
            ],
            "delay": 120,
        }

    # Part 2: Animate search for similar box IDs
    found = False
    for i, id1 in enumerate(lines):
        for j, id2 in enumerate(lines):
            if i == j:
                continue
            diffs = [k for k, (a, b) in enumerate(zip(id1, id2)) if a != b]
            if len(diffs) == 1:
                idx = diffs[0]
                common = id1[:idx] + id1[idx+1:]
                found = True
                yield {
                    "type": "text",
                    "lines": [
                        f"Comparing Box ID {i+1} and {j+1}",
                        f"{id1}",
                        f"{id2}",
                        f"Found 1 difference at position {idx+1}",
                        f"Common letters: {common}",
                        f"Part 2 answer: {common}",
                    ],
                    "delay": 300,
                }
                break
            else:
                # Show comparison step
                yield {
                    "type": "text",
                    "lines": [
                        f"Comparing Box ID {i+1} and {j+1}",
                        f"{id1}",
                        f"{id2}",
                        f"Differences: {len(diffs)}",
                    ],
                    "delay": 60,
                }
        if found:
            break
