"""
Day 11 - Signal Router
Year: 2025

Route signals through a DAG of devices. Part 1: count all
paths from 'you' to 'out'. Part 2: count paths from 'svr'
to 'out' that visit both 'dac' and 'fft'.
"""

from collections import deque


def parse_devices(text):
    devices = {}
    for line in text.strip().split("\n"):
        name, rest = line.split(":")
        targets = rest.strip().split()
        devices[name.strip()] = targets
    return devices


def topological_order(devices):
    """Kahn's algorithm. Returns ordered list or None if cycles."""
    all_nodes = set(devices.keys())
    for targets in devices.values():
        all_nodes.update(targets)

    in_deg = {n: 0 for n in all_nodes}
    for targets in devices.values():
        for t in targets:
            in_deg[t] += 1

    queue = deque(n for n in all_nodes if in_deg[n] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        if node in devices:
            for t in devices[node]:
                in_deg[t] -= 1
                if in_deg[t] == 0:
                    queue.append(t)
    return order if len(order) == len(all_nodes) else None


def solve(puzzle_input: str) -> tuple[str, str]:
    devices = parse_devices(puzzle_input)

    # Part 1: count all paths from 'you' to 'out' via topological DP
    order = topological_order(devices)
    if order is not None:
        path_count = {"you": 1}
        for node in order:
            if node not in devices or node not in path_count:
                continue
            for t in devices[node]:
                path_count[t] = path_count.get(t, 0) + path_count[node]
        part1 = path_count.get("out", 0)
    else:
        # Fallback BFS (original approach — works because graph is a DAG)
        part1 = 0
        queue = deque(["you"])
        while queue:
            node = queue.popleft()
            for t in devices[node]:
                if t == "out":
                    part1 += 1
                else:
                    queue.append(t)

    # Part 2: count paths from 'svr' to 'out' visiting both 'dac' and 'fft'
    required = frozenset({"dac", "fft"})
    memo = {}

    def count_paths(node, visited_req):
        if node == "out":
            return 1 if visited_req == required else 0

        state = (node, visited_req)
        if state in memo:
            return memo[state]

        total = 0
        for neighbor in devices[node]:
            if neighbor in required:
                new_visited = visited_req | frozenset([neighbor])
            else:
                new_visited = visited_req
            total += count_paths(neighbor, new_visited)

        memo[state] = total
        return total

    part2 = count_paths("svr", frozenset())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    devices = parse_devices(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Signal Router",
            "",
            f"  Devices: {len(devices)}",
            f"  Source:  you",
        ],
        "delay": 800,
    }

    sample = list(devices.items())[:8]
    wiring_lines = ["  Device wiring (first 8):"]
    for name, targets in sample:
        wiring_lines.append(f"    {name} -> {', '.join(targets)}")

    yield {
        "type": "text",
        "lines": wiring_lines,
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
            f"  Part 1: {part1} (total paths to out)",
            f"  Part 2: {part2} (constrained paths)",
        ],
        "delay": 500,
    }
