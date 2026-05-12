"""
Day 13 - Shuttle Search
Year: 2020

Find the earliest bus departure, then use the Chinese Remainder Theorem
to find the timestamp where buses depart at consecutive offsets.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    earliest = int(lines[0])
    entries = lines[1].split(",")

    # Part 1: find the bus with the shortest wait
    buses = [(int(b), i) for i, b in enumerate(entries) if b != "x"]
    best_bus, best_wait = 0, float("inf")
    for bus_id, _ in buses:
        wait = bus_id - (earliest % bus_id)
        if wait < best_wait:
            best_wait = wait
            best_bus = bus_id
    part1 = best_bus * best_wait

    # Part 2: Chinese Remainder Theorem
    # Find t such that (t + offset) % bus_id == 0 for each bus
    # Equivalent to t ≡ -offset (mod bus_id)
    # Solve incrementally: maintain (t, step) where step is the LCM so far
    t, step = 0, 1
    for bus_id, offset in buses:
        while (t + offset) % bus_id != 0:
            t += step
        step *= bus_id  # all bus_ids are prime, so LCM = product

    return str(part1), str(t)


def visualize(puzzle_input: str):
    """Yield frames showing bus schedule analysis."""
    lines = puzzle_input.strip().split("\n")
    earliest = int(lines[0])
    entries = lines[1].split(",")
    buses = [(int(b), i) for i, b in enumerate(entries) if b != "x"]

    yield {
        "type": "text",
        "lines": [
            "  Shuttle Search",
            "",
            f"  Earliest departure: {earliest}",
            f"  Bus IDs: {len(buses)} active, {entries.count('x')} out of service",
            f"  IDs: {', '.join(str(b) for b, _ in buses)}",
        ],
        "delay": 600,
    }

    best_bus, best_wait = 0, float("inf")
    for bus_id, _ in buses:
        wait = bus_id - (earliest % bus_id)
        if wait < best_wait:
            best_wait = wait
            best_bus = bus_id

    t, step = 0, 1
    for bus_id, offset in buses:
        while (t + offset) % bus_id != 0:
            t += step
        step *= bus_id

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {best_bus * best_wait}",
            f"    Bus {best_bus}, wait {best_wait} min",
            "",
            f"  Part 2: {t}",
            f"    Consecutive departures at t={t:,}",
        ],
        "delay": 500,
    }
