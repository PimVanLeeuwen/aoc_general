"""
Day 9 - Disk Fragmenter
Year: 2024

Compact a fragmented disk by moving file blocks to fill gaps.
Part 1 moves individual blocks; part 2 moves whole files.
"""


def parse_disk_map(line):
    """Convert disk map string into a list of block IDs (-1 for free)."""
    blocks = []
    file_id = 0
    for i, ch in enumerate(line):
        size = int(ch)
        if i % 2 == 0:
            blocks.extend([file_id] * size)
            file_id += 1
        else:
            blocks.extend([-1] * size)
    return blocks


def compact_blocks(blocks):
    """Part 1: move individual blocks from right to leftmost free space."""
    blocks = list(blocks)
    left = 0
    right = len(blocks) - 1

    while left < right:
        while left < right and blocks[left] != -1:
            left += 1
        while left < right and blocks[right] == -1:
            right -= 1
        if left < right:
            blocks[left], blocks[right] = blocks[right], blocks[left]
            left += 1
            right -= 1

    return blocks


def compact_files(blocks):
    """Part 2: move whole files from right to leftmost fitting gap."""
    blocks = list(blocks)
    max_id = max(b for b in blocks if b != -1)

    for file_id in range(max_id, 0, -1):
        # Find file position and length
        start = blocks.index(file_id)
        length = 0
        while start + length < len(blocks) and blocks[start + length] == file_id:
            length += 1

        # Find leftmost free span that fits, before the file
        free_start = None
        i = 0
        while i < start:
            if blocks[i] == -1:
                free_len = 0
                j = i
                while j < len(blocks) and blocks[j] == -1:
                    free_len += 1
                    j += 1
                if free_len >= length:
                    free_start = i
                    break
                i = j
            else:
                i += 1

        if free_start is not None:
            for k in range(length):
                blocks[free_start + k] = file_id
                blocks[start + k] = -1

    return blocks


def checksum(blocks):
    return sum(i * b for i, b in enumerate(blocks) if b != -1)


def solve(puzzle_input: str) -> tuple[str, str]:
    line = puzzle_input.strip()
    blocks = parse_disk_map(line)

    part1 = checksum(compact_blocks(blocks))
    part2 = checksum(compact_files(blocks))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    line = puzzle_input.strip()
    blocks = parse_disk_map(line)

    total = len(blocks)
    used = sum(1 for b in blocks if b != -1)
    free = total - used
    file_count = max(b for b in blocks if b != -1) + 1

    yield {
        "type": "text",
        "lines": [
            "  Disk Fragmenter",
            "",
            f"  Total blocks: {total}",
            f"  Used blocks: {used}",
            f"  Free blocks: {free}",
            f"  Files: {file_count}",
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
            f"  Part 1: {part1} (block compaction)",
            f"  Part 2: {part2} (file compaction)",
        ],
        "delay": 500,
    }
