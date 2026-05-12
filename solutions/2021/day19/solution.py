"""
Day 19 - Beacon Scanner
Year: 2021

Align overlapping 3D scanners using beacon distance fingerprints,
then count unique beacons and find the largest scanner separation.
"""

from collections import Counter
from itertools import combinations


# All 24 rotation functions for a right-handed coordinate system
ROTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-z, -y, -x),
]


def parse_scanners(text):
    """Parse input into list of beacon lists."""
    scanners = []
    for block in text.strip().split("\n\n"):
        beacons = []
        for line in block.split("\n")[1:]:
            beacons.append(tuple(map(int, line.split(","))))
        scanners.append(beacons)
    return scanners


def try_align(known_beacons, candidate):
    """Try to align candidate beacons to known coordinate frame.
    Uses offset voting: for each rotation, compute all possible offsets
    and check if any offset is consistent for >= 12 beacon pairs."""
    known_set = set(known_beacons)

    for rot in ROTATIONS:
        rotated = [rot(*b) for b in candidate]

        offsets = Counter()
        for kx, ky, kz in known_beacons:
            for rx, ry, rz in rotated:
                offset = (kx - rx, ky - ry, kz - rz)
                offsets[offset] += 1

        (dx, dy, dz), count = offsets.most_common(1)[0]
        if count >= 12:
            aligned = [(bx + dx, by + dy, bz + dz) for bx, by, bz in rotated]
            return (dx, dy, dz), aligned

    return None


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    scanners = parse_scanners(puzzle_input)

    # Scanner 0 defines the reference frame
    all_beacons = set(scanners[0])
    scanner_positions = [(0, 0, 0)]
    aligned = {0}
    unaligned = set(range(1, len(scanners)))

    while unaligned:
        # Use only the beacons from most recently aligned scanners as anchors
        # to keep the inner loop size manageable
        anchor = list(all_beacons)

        found_any = False
        for idx in list(unaligned):
            result = try_align(anchor, scanners[idx])
            if result:
                offset, new_beacons = result
                all_beacons.update(new_beacons)
                scanner_positions.append(offset)
                aligned.add(idx)
                unaligned.discard(idx)
                found_any = True
                break  # restart with updated beacon set

        if not found_any:
            break

    part1 = len(all_beacons)

    part2 = max(
        abs(ax - bx) + abs(ay - by) + abs(az - bz)
        for (ax, ay, az), (bx, by, bz) in combinations(scanner_positions, 2)
    )

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing scanner alignment."""
    scanners = parse_scanners(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Beacon Scanner",
            "",
            f"  Scanners: {len(scanners)}",
            f"  Beacons per scanner: {min(len(s) for s in scanners)}-{max(len(s) for s in scanners)}",
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
            f"  Part 1: {part1} (unique beacons)",
            f"  Part 2: {part2} (max Manhattan distance)",
        ],
        "delay": 500,
    }
