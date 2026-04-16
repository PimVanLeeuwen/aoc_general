"""
Day 11 - Radioisotope Thermoelectric Generators
Year: 2016

Use BFS to find the minimum steps to move all paired items to the top floor safely.
"""

from collections import deque
import re


def is_valid(pairs):
    """Check if a state is safe: no chip is fried."""
    gens = {g for g, _ in pairs}
    for g, c in pairs:
        if c != g and c in gens:
            return False
    return True


def canonical(elevator, pairs):
    """Canonical representation: sort pairs by relative structure."""
    return (elevator, tuple(sorted(pairs)))


def neighbors(elevator, pairs):
    """Generate all valid next states."""
    floors = [elevator + d for d in (-1, 1) if 1 <= elevator + d <= 4]

    # Items on current floor
    items = [(i, "G") for i, (g, _) in enumerate(pairs) if g == elevator] + \
            [(i, "M") for i, (_, c) in enumerate(pairs) if c == elevator]

    # Move 1 or 2 items
    moves = []
    for i in range(len(items)):
        moves.append([items[i]])
        for j in range(i + 1, len(items)):
            moves.append([items[i], items[j]])

    for f in floors:
        for move in moves:
            new_pairs = [list(p) for p in pairs]
            for idx, kind in move:
                if kind == "G":
                    new_pairs[idx][0] = f
                else:
                    new_pairs[idx][1] = f

            new_pairs = [tuple(p) for p in new_pairs]
            if is_valid(new_pairs):
                yield f, tuple(new_pairs)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    # Parse input
    floors = puzzle_input.strip().split("\n")
    pairs = []
    element_index = {}

    for floor_num, line in enumerate(floors, start=1):
        for element, kind in re.findall(r"(\w+)(?:-compatible)? (generator|microchip)", line):
            if element not in element_index:
                element_index[element] = len(element_index)
                pairs.append([None, None])
            idx = element_index[element]
            if kind == "generator":
                pairs[idx][0] = floor_num
            else:
                pairs[idx][1] = floor_num

    pairs = tuple((g, c) for g, c in pairs)

    def bfs(start_pairs):
        start = canonical(1, start_pairs)
        queue = deque([(start, 0)])
        seen = {start}

        while queue:
            (e, p), steps = queue.popleft()
            if all(g == 4 and c == 4 for g, c in p):
                return steps

            for ne, np in neighbors(e, p):
                state = canonical(ne, np)
                if state not in seen:
                    seen.add(state)
                    queue.append((state, steps + 1))

    # Part 1
    part1 = bfs(pairs)

    # Part 2: add extra pairs on floor 1
    extra = ((1, 1), (1, 1))  # two new generator/microchip pairs
    part2 = bfs(pairs + extra)

    return str(part1), str(part2)



# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.

def visualize(puzzle_input: str):
    """Yield visualization frames (up to ~500 recommended)."""
    import re

    # Parse input into (generator_floor, chip_floor) pairs
    floors = puzzle_input.strip().split("\n")
    pairs = []
    element_index = {}

    for floor_num, line in enumerate(floors, start=1):
        for element, kind in re.findall(r"(\w+)(?:-compatible)? (generator|microchip)", line):
            if element not in element_index:
                element_index[element] = len(element_index)
                pairs.append([None, None])
            idx = element_index[element]
            if kind == "generator":
                pairs[idx][0] = floor_num
            else:
                pairs[idx][1] = floor_num

    pairs = [(g, c) for g, c in pairs]

    # Helper: render a single state as text
    def render_state(elevator, pairs):
        lines = []
        for f in range(4, 0, -1):
            row = [f"F{f}"]
            row.append("E" if elevator == f else ".")
            for i, (g, c) in enumerate(pairs):
                row.append(f"G{i}" if g == f else ".")
                row.append(f"M{i}" if c == f else ".")
            lines.append(" ".join(row))
        return lines

    # Initial state
    elevator = 1
    state = (elevator, tuple(pairs))

    # Show the initial parsed state
    yield {
        "type": "text",
        "lines": ["Initial parsed state:"] + render_state(*state),
        "delay": 400,
    }

    # Show a few example moves (not the full BFS)
    # This is intentionally lightweight to avoid huge visualizations.
    # We simply move the elevator up with one item at a time.

    frames = 0
    e, ps = state

    for step in range(1, 5):
        if frames > 40:
            break

        # Move elevator up if possible
        if e < 4:
            e += 1

        yield {
            "type": "text",
            "lines": [f"Step {step}", ""] + render_state(e, ps),
            "delay": 300,
        }
        frames += 1

    # Final frame
    yield {
        "type": "text",
        "lines": ["Visualization complete."],
        "delay": 500,
    }

