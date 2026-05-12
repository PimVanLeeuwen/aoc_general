"""
Day 22 - Slam Shuffle
Year: 2019

Shuffle a deck of cards using modular arithmetic. Each operation is a
linear function mod N; compose them and use modular exponentiation
to handle astronomical repetition counts.
"""


def parse_shuffle(text):
    """Parse shuffle instructions into a list of (operation, argument) tuples."""
    instructions = []
    for line in text.strip().split("\n"):
        if line == "deal into new stack":
            instructions.append(("reverse", 0))
        elif line.startswith("cut "):
            instructions.append(("cut", int(line[4:])))
        elif line.startswith("deal with increment "):
            instructions.append(("increment", int(line[20:])))
    return instructions


def compose_shuffle(instructions, n):
    """Compose all shuffle steps into a single linear function f(x) = a*x + b mod n.

    Each operation maps a card's position:
    - reverse:      x -> -x - 1     (a=-1, b=-1)
    - cut k:        x -> x - k      (a=1,  b=-k)
    - increment k:  x -> k*x        (a=k,  b=0)
    """
    a, b = 1, 0  # identity: f(x) = x
    for op, arg in instructions:
        if op == "reverse":
            a = (-a) % n
            b = (-b - 1) % n
        elif op == "cut":
            b = (b - arg) % n
        elif op == "increment":
            a = (a * arg) % n
            b = (b * arg) % n
    return a, b


def apply_linear(a, b, x, n):
    """Apply f(x) = a*x + b mod n."""
    return (a * x + b) % n


def power_linear(a, b, k, n):
    """Compute f^k(x) = A*x + B mod n where f(x) = a*x + b.

    f^k(x) = a^k * x + b * (a^k - 1) / (a - 1) mod n.
    Uses repeated squaring on the linear function.
    """
    ra, rb = 1, 0  # identity
    while k > 0:
        if k & 1:
            # Compose: (ra*x + rb) then (a*x + b) -> ra = ra*a, rb = a*rb + b
            # Wait, we want to compose g(f(x)) where current result is g, step is f
            # Actually: result = result ∘ step
            # If result is (ra, rb) and step is (a, b), then
            # result(step(x)) = ra*(a*x + b) + rb = ra*a*x + ra*b + rb
            ra, rb = (ra * a) % n, (ra * b + rb) % n
        a, b = (a * a) % n, (a * b + b) % n
        k >>= 1
    return ra, rb


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    instructions = parse_shuffle(puzzle_input)

    # Part 1: deck of 10007, find position of card 2019
    n1 = 10007
    a1, b1 = compose_shuffle(instructions, n1)
    part1 = apply_linear(a1, b1, 2019, n1)

    # Part 2: deck of 119315717514047, shuffle 101741582076661 times,
    # find which card is at position 2020
    n2 = 119315717514047
    k = 101741582076661
    a2, b2 = compose_shuffle(instructions, n2)

    # We need the inverse: given position p, find card c such that f^k(c) = p
    # f^k(c) = A*c + B => c = A^(-1) * (p - B)
    # Compute f^k coefficients
    ak, bk = power_linear(a2, b2, k, n2)

    # Inverse: c = ak^(-1) * (2020 - bk) mod n2
    ak_inv = pow(ak, n2 - 2, n2)  # Fermat's little theorem (n2 is prime)
    part2 = (ak_inv * (2020 - bk)) % n2

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the shuffle composition."""
    instructions = parse_shuffle(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Slam Shuffle",
            "",
            f"  Instructions: {len(instructions)} steps",
            "",
            "  Each operation is a linear function f(x) = ax + b mod N.",
            "  All steps compose into a single function.",
        ],
        "delay": 800,
    }

    # Show small deck example
    n_small = 10
    a_s, b_s = compose_shuffle(instructions, n_small)
    deck = [apply_linear(a_s, b_s, i, n_small) for i in range(n_small)]
    # deck[i] = position of card i, but we want card at each position
    result = [0] * n_small
    for card, pos in enumerate(deck):
        result[pos] = card

    yield {
        "type": "text",
        "lines": [
            "  Small deck (10 cards) after shuffle:",
            f"  {' '.join(str(c) for c in result)}",
            "",
            f"  Composed function: f(x) = {a_s}x + {b_s} mod {n_small}",
        ],
        "delay": 600,
    }

    # Part 1
    n1 = 10007
    a1, b1 = compose_shuffle(instructions, n1)
    part1 = apply_linear(a1, b1, 2019, n1)

    yield {
        "type": "text",
        "lines": [
            "  Part 1 — Deck of 10,007 cards",
            "",
            f"  f(x) = {a1}x + {b1} mod {n1}",
            f"  Card 2019 goes to position {part1}",
        ],
        "delay": 600,
    }

    # Part 2
    n2 = 119315717514047
    k = 101741582076661
    a2, b2 = compose_shuffle(instructions, n2)
    ak, bk = power_linear(a2, b2, k, n2)
    ak_inv = pow(ak, n2 - 2, n2)
    part2 = (ak_inv * (2020 - bk)) % n2

    yield {
        "type": "text",
        "lines": [
            "  Part 2 — Massive deck, repeated shuffle",
            "",
            f"  Deck size: {n2:,}",
            f"  Repetitions: {k:,}",
            "",
            "  Composed via modular exponentiation on",
            "  the linear function, then inverted.",
        ],
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1}",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
