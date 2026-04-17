"""
Day 20 - Firewall Rules
Year: 2016

Merge overlapping blocked IP ranges to find the lowest allowed IP
and count all allowed IPs in the 32-bit address space.
"""

MAX_IP = 4_294_967_295


def parse(puzzle_input):
    ranges = []
    for line in puzzle_input.strip().splitlines():
        lo, hi = map(int, line.split("-"))
        ranges.append((lo, hi))
    return ranges


def merge(ranges):
    """Return sorted, non-overlapping merged ranges."""
    merged = []
    for lo, hi in sorted(ranges):
        if merged and lo <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def solve(puzzle_input: str) -> tuple[str, str]:
    merged = merge(parse(puzzle_input))

    # Part 1: lowest IP not covered — first gap after the leading block
    part1 = merged[0][1] + 1

    # Part 2: count IPs in the gaps between merged blocks
    allowed = 0
    prev_end = -1
    for lo, hi in merged:
        if lo > prev_end + 1:
            allowed += lo - (prev_end + 1)
        prev_end = hi
    if prev_end < MAX_IP:
        allowed += MAX_IP - prev_end

    return str(part1), str(allowed)


def visualize(puzzle_input: str):
    """Show the merge process step by step, then the resulting gaps."""
    ranges = parse(puzzle_input)
    sorted_ranges = sorted(ranges)
    total = len(sorted_ranges)

    # Show raw sorted ranges (first 30)
    preview = sorted_ranges[:30]
    yield {
        "type": "text",
        "lines": [
            f"  {total} blocked ranges (sorted, showing first 30):",
            "",
            *[f"  {lo:>12} – {hi:>12}" for lo, hi in preview],
            *([f"  … and {total - 30} more"] if total > 30 else []),
        ],
        "delay": 600,
    }

    # Animate the merge
    merged = []
    for step, (lo, hi) in enumerate(sorted_ranges):
        if merged and lo <= merged[-1][1] + 1:
            old = merged[-1]
            merged[-1] = (old[0], max(old[1], hi))
            action = f"  Merge {old} + ({lo},{hi}) → {merged[-1]}"
        else:
            merged.append((lo, hi))
            action = f"  Add   ({lo}, {hi})"

        if step % max(1, total // 40) == 0 or step == total - 1:
            yield {
                "type": "text",
                "lines": [
                    f"  Merging ranges… ({step+1}/{total})",
                    "",
                    action,
                    "",
                    f"  Merged blocks so far: {len(merged)}",
                ],
                "delay": 80,
            }

    # Show final gaps
    gaps = []
    prev_end = -1
    for lo, hi in merged:
        if lo > prev_end + 1:
            gaps.append((prev_end + 1, lo - 1))
        prev_end = hi
    if prev_end < MAX_IP:
        gaps.append((prev_end + 1, MAX_IP))

    allowed = sum(hi - lo + 1 for lo, hi in gaps)
    gap_lines = [f"  {lo:>12} – {hi:>12}  ({hi - lo + 1} IPs)" for lo, hi in gaps[:20]]
    if len(gaps) > 20:
        gap_lines.append(f"  … and {len(gaps) - 20} more gaps")

    yield {
        "type": "text",
        "lines": [
            f"  Merge complete: {len(merged)} blocked blocks → {len(gaps)} allowed gap(s)",
            "",
            "  Allowed ranges:",
            *gap_lines,
            "",
            f"  Lowest allowed IP : {gaps[0][0]}",
            f"  Total allowed IPs : {allowed}",
        ],
        "delay": 1000,
    }
