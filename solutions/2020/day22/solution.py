"""
Day 22 - Crab Combat
Year: 2020

Simulate a card game between two players, first with simple rules
then with recursive sub-games.
"""

from collections import deque


def parse_decks(text):
    """Parse the two player decks from the input."""
    p1_block, p2_block = text.strip().split("\n\n")
    deck1 = deque(int(x) for x in p1_block.strip().split("\n")[1:])
    deck2 = deque(int(x) for x in p2_block.strip().split("\n")[1:])
    return deck1, deck2


def score(deck):
    """Calculate the score of a deck."""
    return sum(card * (len(deck) - i) for i, card in enumerate(deck))


def combat(deck1, deck2):
    """Play regular Combat, return the winning deck."""
    while deck1 and deck2:
        c1, c2 = deck1.popleft(), deck2.popleft()
        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)
    return deck1 if deck1 else deck2


def recursive_combat(deck1, deck2):
    """Play Recursive Combat, return (winner, winning_deck)."""
    seen = set()

    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in seen:
            return 1, deck1
        seen.add(state)

        c1, c2 = deck1.popleft(), deck2.popleft()

        if len(deck1) >= c1 and len(deck2) >= c2:
            sub1 = deque(list(deck1)[:c1])
            sub2 = deque(list(deck2)[:c2])
            winner, _ = recursive_combat(sub1, sub2)
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

    if deck1:
        return 1, deck1
    return 2, deck2


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    deck1, deck2 = parse_decks(puzzle_input)

    # Part 1: regular combat
    d1_copy, d2_copy = deque(deck1), deque(deck2)
    winner = combat(d1_copy, d2_copy)
    part1 = score(winner)

    # Part 2: recursive combat
    _, winning_deck = recursive_combat(deck1, deck2)
    part2 = score(winning_deck)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the card game progression."""
    deck1, deck2 = parse_decks(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Crab Combat",
            "",
            f"  Player 1: {len(deck1)} cards",
            f"  Player 2: {len(deck2)} cards",
        ],
        "delay": 600,
    }

    # Simulate regular combat with snapshots
    d1, d2 = deque(deck1), deque(deck2)
    rounds = 0
    while d1 and d2:
        c1, c2 = d1.popleft(), d2.popleft()
        if c1 > c2:
            d1.append(c1)
            d1.append(c2)
        else:
            d2.append(c2)
            d2.append(c1)
        rounds += 1

    winner_p1 = d1 if d1 else d2
    part1 = score(winner_p1)

    yield {
        "type": "text",
        "lines": [
            "  Regular Combat",
            "",
            f"  Rounds played: {rounds}",
            f"  Winner: Player {'1' if d1 else '2'}",
            f"  Score: {part1}",
        ],
        "delay": 800,
    }

    # Part 2 result
    _, winning_deck = recursive_combat(deque(deck1), deque(deck2))
    part2 = score(winning_deck)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (regular combat)",
            f"  Part 2: {part2} (recursive combat)",
        ],
        "delay": 500,
    }
