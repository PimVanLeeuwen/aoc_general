"""
Day 16 - Dragon Checksum
Year: 2016

Generate disk data using a modified dragon curve, then compute an odd-length checksum.
"""


def dragon(a):
    """One step of the dragon curve: a + '0' + reverse(flip(a))."""
    return a + "0" + a[::-1].translate(str.maketrans("01", "10"))


def fill(initial, length):
    """Expand using dragon curve until we have at least `length` bits, then truncate."""
    data = initial
    while len(data) < length:
        data = dragon(data)
    return data[:length]


def checksum(data):
    """Reduce pairs to a single bit until the result has odd length."""
    while len(data) % 2 == 0:
        data = "".join("1" if data[i] == data[i + 1] else "0" for i in range(0, len(data), 2))
    return data


def solve(puzzle_input: str) -> tuple[str, str]:
    initial = puzzle_input.strip()

    part1 = checksum(fill(initial, 272))
    part2 = checksum(fill(initial, 35651584))

    return part1, part2


def visualize(puzzle_input: str):
    """Show the dragon curve expanding, then the checksum reduction steps."""
    initial = puzzle_input.strip()

    # ── Phase 1: dragon curve expansion ──────────────────────────────────────
    data = initial
    step = 0
    target = 272

    while len(data) < target:
        step += 1
        data = dragon(data)
        preview = data[:60] + ("…" if len(data) > 60 else "")
        yield {
            "type": "text",
            "lines": [
                "  Dragon curve expansion (target: 272 bits)",
                "",
                f"  Round {step}",
                f"  Length: {len(data)}",
                "",
                f"  {preview}",
            ],
            "delay": 400,
        }

    disk = data[:target]

    yield {
        "type": "text",
        "lines": [
            "  Disk filled — truncated to 272 bits:",
            "",
            f"  {disk[:60]}…",
            "",
            "  Starting checksum reduction…",
        ],
        "delay": 600,
    }

    # ── Phase 2: checksum reduction ───────────────────────────────────────────
    current = disk
    cksum_round = 0

    while len(current) % 2 == 0:
        cksum_round += 1
        next_cs = "".join(
            "1" if current[i] == current[i + 1] else "0"
            for i in range(0, len(current), 2)
        )
        preview = next_cs[:60] + ("…" if len(next_cs) > 60 else "")
        yield {
            "type": "text",
            "lines": [
                f"  Checksum round {cksum_round}",
                f"  Input length:  {len(current)}  (even — continue)",
                f"  Output length: {len(next_cs)}",
                "",
                f"  {preview}",
            ],
            "delay": 500,
        }
        current = next_cs

    yield {
        "type": "text",
        "lines": [
            f"  Checksum round {cksum_round + 1 if cksum_round == 0 else cksum_round}",
            f"  Length {len(current)} is odd — done.",
            "",
            f"  Checksum: {current}",
        ],
        "delay": 800,
    }
