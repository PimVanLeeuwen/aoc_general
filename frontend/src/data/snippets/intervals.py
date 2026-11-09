def merge(intervals):
    """Merge overlapping or touching inclusive ranges [(start, end), ...]."""
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [tuple(interval) for interval in merged]


def overlap(a, b):
    """Intersection of two inclusive ranges, or None."""
    start, end = max(a[0], b[0]), min(a[1], b[1])
    return (start, end) if start <= end else None


def apply_shift(interval, rule_start, rule_end, shift):
    """
    Map a whole range through one 'source range moves by shift' rule without
    touching individual numbers. Returns (moved part or None, leftover parts).
    """
    start, end = interval
    moved = overlap(interval, (rule_start, rule_end))
    if moved is None:
        return None, [interval]
    leftovers = []
    if start < moved[0]:
        leftovers.append((start, moved[0] - 1))
    if moved[1] < end:
        leftovers.append((moved[1] + 1, end))
    return (moved[0] + shift, moved[1] + shift), leftovers
