"""
Day 25 - Combo Breaker
Year: 2020

Crack the hotel room's RFID handshake by finding the discrete logarithm
of the card's public key, then derive the encryption key.
"""


def find_loop_size(public_key):
    """Find the loop size that transforms subject number 7 into the public key."""
    value = 1
    loop = 0
    while value != public_key:
        value = value * 7 % 20201227
        loop += 1
    return loop


def transform(subject, loop_size):
    """Apply the transform operation loop_size times."""
    value = 1
    for _ in range(loop_size):
        value = value * subject % 20201227
    return value


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    card_pk = int(lines[0])
    door_pk = int(lines[1])

    card_loop = find_loop_size(card_pk)
    encryption_key = transform(door_pk, card_loop)

    return str(encryption_key), "0"


def visualize(puzzle_input: str):
    """Yield frames showing the key derivation process."""
    lines = puzzle_input.strip().split("\n")
    card_pk = int(lines[0])
    door_pk = int(lines[1])

    yield {
        "type": "text",
        "lines": [
            "  Combo Breaker",
            "",
            f"  Card public key: {card_pk}",
            f"  Door public key: {door_pk}",
            "",
            "  Finding loop sizes...",
        ],
        "delay": 600,
    }

    card_loop = find_loop_size(card_pk)
    door_loop = find_loop_size(door_pk)

    yield {
        "type": "text",
        "lines": [
            "  Loop sizes found:",
            "",
            f"  Card loop size: {card_loop}",
            f"  Door loop size: {door_loop}",
            "",
            "  Deriving encryption key...",
        ],
        "delay": 800,
    }

    encryption_key = transform(door_pk, card_loop)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Encryption key: {encryption_key}",
            "",
            f"  Verification:",
            f"    door_pk ^ card_loop = {transform(door_pk, card_loop)}",
            f"    card_pk ^ door_loop = {transform(card_pk, door_loop)}",
            f"    Keys match: {transform(door_pk, card_loop) == transform(card_pk, door_loop)}",
        ],
        "delay": 500,
    }
