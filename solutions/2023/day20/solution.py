"""
Day 20 - Pulse Propagation
Year: 2023

Simulate a network of flip-flop and conjunction modules
processing low/high pulses.
"""

import math
from collections import deque


def parse_modules(text):
    """Parse module definitions into a dict."""
    modules = {}
    for line in text.split("\n"):
        name, targets = line.split(" -> ")
        targets = targets.split(", ")
        if name == "broadcaster":
            modules[name] = ("broadcaster", targets)
        elif name[0] == "%":
            modules[name[1:]] = ("flip-flop", targets)
        elif name[0] == "&":
            modules[name[1:]] = ("conjunction", targets)
    return modules


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    modules = parse_modules(puzzle_input.strip())

    # Build adjacency and initialize state
    flip_state = {}  # name -> bool (False = off)
    conj_memory = {}  # name -> {input_name: last_pulse}

    for name, (kind, _) in modules.items():
        if kind == "flip-flop":
            flip_state[name] = False
        elif kind == "conjunction":
            conj_memory[name] = {}

    # Initialize conjunction memories with all inputs
    for name, (_, targets) in modules.items():
        for t in targets:
            if t in conj_memory:
                conj_memory[t][name] = False  # low

    # Find the module feeding 'rx' for part 2
    rx_feeder = None
    for name, (_, targets) in modules.items():
        if "rx" in targets:
            rx_feeder = name
            break

    # Track cycle lengths for inputs to the rx feeder
    cycle_inputs = {}
    if rx_feeder and rx_feeder in conj_memory:
        cycle_inputs = {inp: 0 for inp in conj_memory[rx_feeder]}

    low_count = 0
    high_count = 0
    part1 = 0
    part2 = 0

    for press in range(1, 10001):
        queue = deque([("button", "broadcaster", False)])

        while queue:
            source, dest, pulse = queue.popleft()

            if pulse:
                high_count += 1
            else:
                low_count += 1

            if dest not in modules:
                continue

            kind, targets = modules[dest]

            if kind == "broadcaster":
                for t in targets:
                    queue.append((dest, t, pulse))

            elif kind == "flip-flop":
                if not pulse:  # only react to low pulses
                    flip_state[dest] = not flip_state[dest]
                    out = flip_state[dest]
                    for t in targets:
                        queue.append((dest, t, out))

            elif kind == "conjunction":
                conj_memory[dest][source] = pulse
                out = not all(conj_memory[dest].values())
                for t in targets:
                    queue.append((dest, t, out))

                # Part 2: track when feeder inputs send high
                if dest == rx_feeder and pulse:
                    if source in cycle_inputs and cycle_inputs[source] == 0:
                        cycle_inputs[source] = press

        if press == 1000:
            part1 = low_count * high_count

        # Check if we found all cycles for part 2
        if cycle_inputs and all(v > 0 for v in cycle_inputs.values()):
            part2 = math.lcm(*cycle_inputs.values())
            if press >= 1000:
                break

    if not cycle_inputs:
        part2 = 0

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing pulse propagation."""
    modules = parse_modules(puzzle_input.strip())

    flip_flops = sum(1 for _, (k, _) in modules.items() if k == "flip-flop")
    conjunctions = sum(1 for _, (k, _) in modules.items() if k == "conjunction")

    yield {
        "type": "text",
        "lines": [
            "  Pulse Propagation",
            "",
            f"  Modules: {len(modules)}",
            f"  Flip-flops: {flip_flops}",
            f"  Conjunctions: {conjunctions}",
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
            f"  Part 1: {part1} (low × high)",
            f"  Part 2: {part2} (presses for rx)",
        ],
        "delay": 500,
    }
