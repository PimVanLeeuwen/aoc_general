"""
Day 7 - Camel Cards
Year: 2023

Rank poker-like hands by type strength and card values,
then calculate total winnings.
"""

from collections import Counter


CARD_RANK = {c: i for i, c in enumerate("23456789TJQKA")}
CARD_RANK_JOKER = {c: i for i, c in enumerate("J23456789TQKA")}


def hand_type(cards):
    """Classify a hand into a type value (higher = stronger)."""
    counts = sorted(Counter(cards).values(), reverse=True)
    if counts[0] == 5:
        return 6  # Five of a kind
    if counts[0] == 4:
        return 5  # Four of a kind
    if counts[0] == 3 and counts[1] == 2:
        return 4  # Full house
    if counts[0] == 3:
        return 3  # Three of a kind
    if counts[0] == 2 and counts[1] == 2:
        return 2  # Two pair
    if counts[0] == 2:
        return 1  # One pair
    return 0  # High card


def hand_type_joker(cards):
    """Best possible hand type when J is wild."""
    jokers = cards.count("J")
    if jokers == 5:
        return 6
    remaining = [c for c in cards if c != "J"]
    counts = sorted(Counter(remaining).values(), reverse=True)
    counts[0] += jokers
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0


def sort_key(hand, joker=False):
    """Return a sortable key for a hand."""
    cards = hand[0]
    rank_map = CARD_RANK_JOKER if joker else CARD_RANK
    type_val = hand_type_joker(cards) if joker else hand_type(cards)
    return (type_val, tuple(rank_map[c] for c in cards))


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    hands = []
    for line in puzzle_input.strip().split("\n"):
        cards, bid = line.split()
        hands.append((cards, int(bid)))

    # Part 1: standard ranking
    ranked = sorted(hands, key=lambda h: sort_key(h, joker=False))
    part1 = sum(rank * bid for rank, (_, bid) in enumerate(ranked, 1))

    # Part 2: J is joker (weakest card, wild for type)
    ranked = sorted(hands, key=lambda h: sort_key(h, joker=True))
    part2 = sum(rank * bid for rank, (_, bid) in enumerate(ranked, 1))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing hand rankings."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Camel Cards",
            "",
            f"  Hands: {len(lines)}",
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
            f"  Part 1: {part1} (standard rules)",
            f"  Part 2: {part2} (joker rules)",
        ],
        "delay": 500,
    }
