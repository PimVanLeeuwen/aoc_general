"""
Day 04 - The Ideal Stocking Stuffer
Year: 2015

Find the lowest number that, appended to a secret key, produces an MD5 hash
starting with a given number of zeroes.
"""
import hashlib


def mine(key: str, zeroes: int) -> int:
    prefix = "0" * zeroes
    n = 1
    while True:
        digest = hashlib.md5(f"{key}{n}".encode()).hexdigest()
        if digest.startswith(prefix):
            return n
        n += 1


def solve(puzzle_input: str) -> tuple[str, str]:
    key = puzzle_input.strip()
    part1 = mine(key, 5)
    part2 = mine(key, 6)
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Show hashes being tested until the first 5-zero answer is found."""
    key = puzzle_input.strip()
    prefix = "00000"
    step = 500
    n = 1

    while True:
        digest = hashlib.md5(f"{key}{n}".encode()).hexdigest()
        found = digest.startswith(prefix)

        if n % step == 1 or found:
            yield {
                "type": "text",
                "lines": [
                    "Mining AdventCoins...",
                    "",
                    f"  Key     : {key}",
                    f"  Trying  : {n}",
                    f"  Input   : {key}{n}",
                    f"  Hash    : {digest}",
                    "",
                    f"  {'*** FOUND! ***' if found else 'No match yet...'}",
                ],
                "delay": 30,
            }

        if found:
            yield {
                "type": "text",
                "lines": [
                    "Solution found!",
                    "",
                    f"  Key     : {key}",
                    f"  Number  : {n}",
                    f"  Input   : {key}{n}",
                    f"  Hash    : {digest}",
                    "",
                    f"  Hash starts with '{prefix}'",
                    f"  Tested {n:,} candidates.",
                ],
                "delay": 2000,
            }
            break

        n += 1