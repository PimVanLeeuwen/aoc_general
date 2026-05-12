"""
Day 06 - Lanternfish
Year: 2021

Model exponential lanternfish population growth using timer buckets
instead of tracking individual fish.
"""


def simulate(timers, days):
    """Simulate lanternfish growth for a given number of days."""
    # Count fish by their timer value (0-8)
    buckets = [0] * 9
    for t in timers:
        buckets[t] += 1

    for _ in range(days):
        spawning = buckets[0]
        # Shift all timers down by 1
        buckets = buckets[1:] + [0]
        # Fish that spawned reset to 6
        buckets[6] += spawning
        # New fish start at 8
        buckets[8] += spawning

    return sum(buckets)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    timers = [int(x) for x in puzzle_input.strip().split(",")]

    part1 = simulate(timers, 80)
    part2 = simulate(timers, 256)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing lanternfish population growth."""
    timers = [int(x) for x in puzzle_input.strip().split(",")]

    yield {
        "type": "text",
        "lines": [
            "  Lanternfish",
            "",
            f"  Initial fish: {len(timers)}",
        ],
        "delay": 600,
    }

    # Show population at milestones
    buckets = [0] * 9
    for t in timers:
        buckets[t] += 1

    milestones = []
    for day in range(1, 257):
        spawning = buckets[0]
        buckets = buckets[1:] + [0]
        buckets[6] += spawning
        buckets[8] += spawning
        if day <= 18 or day == 80 or day == 256:
            milestones.append((day, sum(buckets)))

    lines = ["  Population growth:", ""]
    for day, count in milestones:
        bar = "#" * min(60, count // max(1, milestones[-1][1] // 60))
        lines.append(f"  Day {day:>3}: {count:>15,} {bar}")

    yield {
        "type": "text",
        "lines": lines,
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {milestones[-2][1]} (after 80 days)",
            f"  Part 2: {milestones[-1][1]} (after 256 days)",
        ],
        "delay": 500,
    }
