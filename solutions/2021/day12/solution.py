"""
Day 12 - Passage Pathing
Year: 2021

Count all paths through a cave system, with small caves visited at most
once (part 1) or with one small cave allowed a second visit (part 2).
"""

from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    graph = defaultdict(list)
    for line in puzzle_input.strip().split("\n"):
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)

    # BFS/DFS counting paths
    # State: (current_cave, visited_small_caves_frozenset, used_double_visit)
    part1 = 0
    part2 = 0
    stack = [("start", frozenset({"start"}), False)]

    while stack:
        cave, visited, used_double = stack.pop()

        for neighbor in graph[cave]:
            if neighbor == "start":
                continue

            if neighbor == "end":
                if not used_double:
                    part1 += 1
                part2 += 1
                continue

            is_small = neighbor.islower()

            if not is_small or neighbor not in visited:
                stack.append((neighbor, visited | {neighbor} if is_small else visited, used_double))
            elif is_small and neighbor in visited and not used_double:
                stack.append((neighbor, visited, True))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing cave path exploration."""
    graph = defaultdict(list)
    for line in puzzle_input.strip().split("\n"):
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)

    caves = sorted(graph.keys())
    small = [c for c in caves if c.islower() and c not in ("start", "end")]
    big = [c for c in caves if c.isupper()]

    yield {
        "type": "text",
        "lines": [
            "  Passage Pathing",
            "",
            f"  Caves: {len(caves)}",
            f"  Big caves: {', '.join(big) if big else 'none'}",
            f"  Small caves: {', '.join(small)}",
            f"  Edges: {sum(len(v) for v in graph.values()) // 2}",
        ],
        "delay": 600,
    }

    part1 = 0
    part2 = 0
    stack = [("start", frozenset({"start"}), False)]
    while stack:
        cave, visited, used_double = stack.pop()
        for neighbor in graph[cave]:
            if neighbor == "start":
                continue
            if neighbor == "end":
                if not used_double:
                    part1 += 1
                part2 += 1
                continue
            is_small = neighbor.islower()
            if not is_small or neighbor not in visited:
                stack.append((neighbor, visited | {neighbor} if is_small else visited, used_double))
            elif is_small and neighbor in visited and not used_double:
                stack.append((neighbor, visited, True))

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (single visit paths)",
            f"  Part 2: {part2} (with one double visit)",
        ],
        "delay": 500,
    }
