"""
Day 5 - If You Give A Seed A Fertilizer
Year: 2023

Map seed numbers through a series of range-based transformations
to find the lowest location number.
"""


def parse_maps(text):
    """Parse seed numbers and mapping stages."""
    sections = text.strip().split("\n\n")
    seeds = list(map(int, sections[0].split(": ")[1].split()))

    maps = []
    for section in sections[1:]:
        ranges = []
        for line in section.split("\n")[1:]:
            dst, src, length = map(int, line.split())
            ranges.append((src, src + length, dst - src))
        maps.append(ranges)

    return seeds, maps


def apply_map(value, ranges):
    """Apply a single mapping stage to a value."""
    for src_start, src_end, offset in ranges:
        if src_start <= value < src_end:
            return value + offset
    return value


def apply_map_to_ranges(intervals, ranges):
    """Apply a mapping stage to a list of [start, end) intervals."""
    result = []
    todo = list(intervals)

    for src_start, src_end, offset in ranges:
        next_todo = []
        for lo, hi in todo:
            # Overlap with this mapping range
            overlap_lo = max(lo, src_start)
            overlap_hi = min(hi, src_end)
            if overlap_lo < overlap_hi:
                result.append((overlap_lo + offset, overlap_hi + offset))
                if lo < overlap_lo:
                    next_todo.append((lo, overlap_lo))
                if overlap_hi < hi:
                    next_todo.append((overlap_hi, hi))
            else:
                next_todo.append((lo, hi))
        todo = next_todo

    result.extend(todo)
    return result


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    seeds, maps = parse_maps(puzzle_input)

    # Part 1: individual seeds
    locations = list(seeds)
    for stage in maps:
        locations = [apply_map(v, stage) for v in locations]
    part1 = min(locations)

    # Part 2: seed ranges
    intervals = []
    for i in range(0, len(seeds), 2):
        intervals.append((seeds[i], seeds[i] + seeds[i + 1]))

    for stage in maps:
        intervals = apply_map_to_ranges(intervals, stage)

    part2 = min(lo for lo, hi in intervals)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing seed mapping."""
    seeds, maps = parse_maps(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  If You Give A Seed A Fertilizer",
            "",
            f"  Seeds: {len(seeds)} values",
            f"  Mapping stages: {len(maps)}",
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
            f"  Part 1: {part1} (individual seeds)",
            f"  Part 2: {part2} (seed ranges)",
        ],
        "delay": 500,
    }
