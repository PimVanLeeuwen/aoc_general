"""
Day 14 - One-Time Pad
Year: 2016

Find the 64th one-time pad key by scanning MD5 hashes for triplets confirmed
by a matching quintuplet within the next 1000 hashes.
"""

import hashlib
import re


def make_hasher(salt, stretch=0):
    """Return a cached hash function for the given salt and stretch count."""
    cache = {}

    def h(index):
        if index not in cache:
            digest = hashlib.md5(f"{salt}{index}".encode()).hexdigest()
            for _ in range(stretch):
                digest = hashlib.md5(digest.encode()).hexdigest()
            cache[index] = digest
        return cache[index]

    return h


def find_triplet(s):
    """Return the first character that appears three times in a row, or None."""
    m = re.search(r"(.)\1\1", s)
    return m.group(1) if m else None


def has_quintuplet(s, ch):
    """Return True if ch appears five times in a row in s."""
    return ch * 5 in s


def find_keys(salt, stretch=0, target=64):
    h = make_hasher(salt, stretch)
    keys = []
    index = 0

    while len(keys) < target:
        digest = h(index)
        ch = find_triplet(digest)
        if ch:
            if any(has_quintuplet(h(index + k), ch) for k in range(1, 1001)):
                keys.append(index)
        index += 1

    return keys


def solve(puzzle_input: str) -> tuple[str, str]:
    salt = puzzle_input.strip()

    part1 = find_keys(salt, stretch=0)[-1]
    part2 = find_keys(salt, stretch=2016)[-1]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Show the key-finding process: scanning hashes, spotting triplets, confirming with quintuplets."""
    salt = puzzle_input.strip()
    h = make_hasher(salt, stretch=0)
    keys = []
    index = 0
    frame_interval = 50

    while len(keys) < 64:
        digest = h(index)
        ch = find_triplet(digest)
        confirmed = False

        if ch:
            confirmed = any(has_quintuplet(h(index + k), ch) for k in range(1, 1001))
            if confirmed:
                keys.append((index, ch, digest))

        if index % frame_interval == 0 or confirmed:
            recent = keys[-5:] if keys else []
            key_lines = [
                f"  [{i+1:>2}] index {idx:>6}  triplet='{c}'  {d[:32]}..."
                for i, (idx, c, d) in enumerate(recent, start=len(keys) - len(recent))
            ]
            yield {
                "type": "text",
                "lines": [
                    f"  Salt: {salt}",
                    f"  Scanning index: {index}",
                    f"  Keys found: {len(keys)} / 64",
                    "",
                    "  Recent keys:",
                    *key_lines,
                ],
                "delay": 40 if not confirmed else 200,
            }

        index += 1

    yield {
        "type": "text",
        "lines": [
            f"  Salt: {salt}",
            f"  64th key at index: {keys[-1][0]}",
            "",
            "  Last 10 keys:",
            *[
                f"  [{i+1:>2}] index {idx:>6}  triplet='{c}'  {d[:32]}..."
                for i, (idx, c, d) in enumerate(keys[-10:], start=54)
            ],
        ],
        "delay": 800,
    }
