"""
Day 7 - No Space Left On Device
Year: 2022

Parse terminal output to reconstruct a directory tree,
then answer queries about directory sizes.
"""

from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    dir_sizes = defaultdict(int)
    path = []

    for line in puzzle_input.strip().split("\n"):
        if line == "$ ls" or line.startswith("dir"):
            continue
        elif line.startswith("$ cd"):
            dest = line.split()[2]
            if dest == "..":
                path.pop()
            else:
                path.append(dest if not path else path[-1] + "/" + dest)
        else:
            size = int(line.split()[0])
            for d in path:
                dir_sizes[d] += size

    total_used = dir_sizes["/"]
    free_space = 70_000_000 - total_used
    need_to_free = 30_000_000 - free_space

    # Part 1: sum of directories with size <= 100000
    part1 = sum(s for s in dir_sizes.values() if s <= 100_000)

    # Part 2: smallest directory that frees enough space
    part2 = min(s for s in dir_sizes.values() if s >= need_to_free)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing directory sizes."""
    dir_sizes = defaultdict(int)
    path = []

    for line in puzzle_input.strip().split("\n"):
        if line == "$ ls" or line.startswith("dir"):
            continue
        elif line.startswith("$ cd"):
            dest = line.split()[2]
            if dest == "..":
                path.pop()
            else:
                path.append(dest if not path else path[-1] + "/" + dest)
        else:
            size = int(line.split()[0])
            for d in path:
                dir_sizes[d] += size

    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: -x[1])
    top_dirs = sorted_dirs[:10]

    lines = ["  Directory sizes (top 10):", ""]
    for name, size in top_dirs:
        lines.append(f"  {size:>10,}  {name}")

    yield {"type": "text", "lines": lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (dirs ≤ 100k)",
            f"  Part 2: {part2} (smallest to delete)",
        ],
        "delay": 500,
    }
