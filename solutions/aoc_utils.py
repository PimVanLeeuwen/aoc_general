"""
Shared helpers for Advent of Code solutions: parsing, grids, search, math and ranges.

Use it from any solution with `from aoc_utils import ...`. The site detects the
import and loads this file next to the solution, and the local runners put the
solutions/ folder on sys.path. Standard library only, so it also runs in Pyodide.
"""

import heapq
import re
from collections import deque
from fractions import Fraction
from itertools import accumulate, count, pairwise
from math import gcd, isqrt, lcm

# ── Parsing ───────────────────────────────────────────────────────────────────


def ints(text):
    """All integers in a string, including negative ones."""
    return [int(number) for number in re.findall(r"-?\d+", text)]


def lines(text):
    """Lines of the input, without the trailing newline."""
    return text.strip("\n").splitlines()


def sections(text):
    """Blocks separated by a blank line."""
    return text.strip("\n").split("\n\n")


# ── Grids ─────────────────────────────────────────────────────────────────────
# Positions are (row, col) tuples; row grows downwards.

DIRS_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left: index + 1 turns right
DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ARROWS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def parse_grid(text):
    """Grid as a dict {(row, col): char}. Bounds checks become `position in grid`."""
    return {(r, c): char for r, line in enumerate(lines(text)) for c, char in enumerate(line)}


def grid_find(grid, char):
    """First position holding char (e.g. the start 'S'), or None."""
    return next((position for position, value in grid.items() if value == char), None)


def grid_find_all(grid, char):
    return [position for position, value in grid.items() if value == char]


def add(a, b):
    """Add two positions or vectors: add((r, c), (dr, dc))."""
    return tuple(x + y for x, y in zip(a, b))


def neighbors(position, grid=None, dirs=DIRS_4):
    """Adjacent positions; with a grid (dict or set), only those inside it."""
    r, c = position
    for dr, dc in dirs:
        next_position = (r + dr, c + dc)
        if grid is None or next_position in grid:
            yield next_position


def rotate_clockwise(rows):
    """Rotate a list-of-strings grid 90 degrees clockwise."""
    return ["".join(column) for column in zip(*rows[::-1])]


def transpose(rows):
    return ["".join(column) for column in zip(*rows)]


def grid_to_str(cells, fill="."):
    """
    Render a dict {(r, c): char} or a set of positions (drawn as '#') for
    debugging. Works with negative coordinates.
    """
    if not cells:
        return ""
    chars = cells if isinstance(cells, dict) else {position: "#" for position in cells}
    rows = [r for r, _ in chars]
    cols = [c for _, c in chars]
    return "\n".join(
        "".join(str(chars.get((r, c), fill)) for c in range(min(cols), max(cols) + 1))
        for r in range(min(rows), max(rows) + 1)
    )


def print_grid(cells, fill="."):
    print(grid_to_str(cells, fill))


def manhattan(a, b=(0, 0)):
    """Taxicab distance in any number of dimensions."""
    return sum(abs(x - y) for x, y in zip(a, b))


# ── Search & graphs ───────────────────────────────────────────────────────────
# `neighbors` arguments are functions: for BFS they yield next nodes, for
# Dijkstra / A* they yield (next_node, step_cost). A `goal` is a node or a
# function node -> bool. Nodes can be any hashable value, including whole states.


def _goal_test(goal):
    return goal if callable(goal) else (lambda node: node == goal)


def bfs(start, goal, neighbors):
    """Fewest steps from start to goal (equal step costs), or None if unreachable."""
    found = bfs_path(start, goal, neighbors)
    return None if found is None else len(found) - 1


def bfs_path(start, goal, neighbors):
    """Shortest list of nodes from start to goal, or None."""
    is_goal = _goal_test(goal)
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if is_goal(node):
            return _walk_back(parent, node)
        for next_node in neighbors(node):
            if next_node not in parent:
                parent[next_node] = node
                queue.append(next_node)
    return None


def bfs_distances(start, neighbors):
    """Steps from start to every reachable node: {node: steps}."""
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for next_node in neighbors(node):
            if next_node not in distance:
                distance[next_node] = distance[node] + 1
                queue.append(next_node)
    return distance


def dijkstra(start, goal, neighbors, heuristic=None):
    """
    Lowest total cost from start to goal, or None. Pass heuristic(node) (never
    overestimating, e.g. manhattan to the target) to turn it into A*.
    """
    found = shortest_path(start, goal, neighbors, heuristic)
    return None if found is None else found[0]


def shortest_path(start, goal, neighbors, heuristic=None):
    """(cost, list of nodes) of a cheapest path from start to goal, or None."""
    is_goal = _goal_test(goal)
    estimate = heuristic or (lambda node: 0)
    best = {start: 0}
    parent = {start: None}
    tie = count()  # keeps the heap from comparing nodes (complex numbers, dicts...)
    heap = [(estimate(start), next(tie), start)]
    done = set()
    while heap:
        _, _, node = heapq.heappop(heap)
        if node in done:
            continue  # stale entry, this node was already expanded more cheaply
        done.add(node)
        cost = best[node]
        if is_goal(node):
            return cost, _walk_back(parent, node)
        for next_node, step_cost in neighbors(node):
            new_cost = cost + step_cost
            if new_cost < best.get(next_node, float("inf")):
                best[next_node] = new_cost
                parent[next_node] = node
                heapq.heappush(heap, (new_cost + estimate(next_node), next(tie), next_node))
    return None


def dijkstra_costs(start, neighbors):
    """Cheapest cost from start to every reachable node: {node: cost}."""
    best = {start: 0}
    tie = count()
    heap = [(0, next(tie), start)]
    while heap:
        cost, _, node = heapq.heappop(heap)
        if cost > best[node]:
            continue  # stale entry
        for next_node, step_cost in neighbors(node):
            new_cost = cost + step_cost
            if new_cost < best.get(next_node, float("inf")):
                best[next_node] = new_cost
                heapq.heappush(heap, (new_cost, next(tie), next_node))
    return best


def _walk_back(parent, node):
    path = []
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def regions(grid, same=lambda a, b: a == b):
    """Flood fill a dict grid into groups of 4-connected cells with matching values."""
    seen = set()
    groups = []
    for start in grid:
        if start in seen:
            continue
        group = set(bfs_distances(start, lambda p: (
            n for n in neighbors(p, grid) if same(grid[n], grid[start])
        )))
        seen |= group
        groups.append(group)
    return groups


class UnionFind:
    """Disjoint sets: union(a, b) joins groups, find(a) names a's group, size(a) counts it."""

    def __init__(self, items=()):
        self.parent = {}
        self.sizes = {}
        for item in items:
            self.find(item)

    def find(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.sizes[item] = 1
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]  # path halving
            item = self.parent[item]
        return item

    def union(self, a, b):
        """Join the groups of a and b. Returns False if they were already one group."""
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self.sizes[root_a] < self.sizes[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.sizes[root_a] += self.sizes.pop(root_b)
        return True

    def size(self, item):
        return self.sizes[self.find(item)]

    def groups(self):
        """Number of separate groups."""
        return len(self.sizes)


def topological_sort(nodes, edges):
    """Order nodes so every (before, after) edge holds; ties go to the smallest node. Raises on a cycle."""
    successors = {node: [] for node in nodes}
    incoming = {node: 0 for node in nodes}
    for before, after in edges:
        successors[before].append(after)
        incoming[after] += 1
    ready = [node for node in nodes if incoming[node] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for next_node in successors[node]:
            incoming[next_node] -= 1
            if incoming[next_node] == 0:
                heapq.heappush(ready, next_node)
    if len(order) != len(incoming):
        raise ValueError("the edges contain a cycle")
    return order


# ── Math & cycles ─────────────────────────────────────────────────────────────


def crt(remainders, moduli):
    """Smallest t >= 0 with t % m == r for every pair (sieving; moduli need not be prime)."""
    t, step = 0, 1
    for remainder, modulus in zip(remainders, moduli):
        for _ in range(modulus):
            if t % modulus == remainder % modulus:
                break
            t += step
        else:
            raise ValueError("no solution: the congruences contradict each other")
        step = lcm(step, modulus)
    return t


def state_after(state, step, n):
    """State after n applications of step(), skipping ahead once a state repeats. State must be hashable."""
    seen = {}
    history = []
    for i in range(n):
        if state in seen:
            cycle_start = seen[state]
            return history[cycle_start + (n - cycle_start) % (i - cycle_start)]
        seen[state] = i
        history.append(state)
        state = step(state)
    return state


def extrapolate(sequence):
    """Next value of a polynomial sequence, by repeated differences."""
    if all(value == 0 for value in sequence):
        return 0
    return sequence[-1] + extrapolate([b - a for a, b in pairwise(sequence)])


def quadratic_at(y0, y1, y2, n):
    """Value at step n of a quadratic known at steps 0, 1 and 2."""
    first, second = y1 - y0, y2 - 2 * y1 + y0
    return y0 + first * n + second * n * (n - 1) // 2


def shoelace_area(corners):
    """Area of a simple polygon from its corners in order."""
    total = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(corners, corners[1:] + corners[:1]))
    return abs(total) / 2


def lattice_points(corners):
    """(interior, boundary) grid points of a polygon with integer corners (Pick's theorem)."""
    boundary = sum(
        gcd(abs(x2 - x1), abs(y2 - y1)) for (x1, y1), (x2, y2) in zip(corners, corners[1:] + corners[:1])
    )
    return int(shoelace_area(corners) - boundary / 2 + 1), boundary


def solve_linear(matrix, rhs):
    """Exact solution of a square linear system as Fractions (check .denominator == 1 for whole numbers)."""
    n = len(matrix)
    rows = [[Fraction(v) for v in row] + [Fraction(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular system: no unique solution")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def divisors(n):
    small = [d for d in range(1, isqrt(n) + 1) if n % d == 0]
    return sorted(set(small + [n // d for d in small]))


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


# ── Ranges ────────────────────────────────────────────────────────────────────
# Intervals are inclusive (start, end) tuples.


def merge_intervals(intervals):
    """Merge overlapping or touching intervals into a sorted list."""
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def overlap(a, b):
    """Intersection of two intervals, or None."""
    start, end = max(a[0], b[0]), min(a[1], b[1])
    return (start, end) if start <= end else None


def subtract(a, b):
    """Parts of interval a not covered by b (zero, one or two intervals)."""
    cut = overlap(a, b)
    if cut is None:
        return [a]
    parts = []
    if a[0] < cut[0]:
        parts.append((a[0], cut[0] - 1))
    if cut[1] < a[1]:
        parts.append((cut[1] + 1, a[1]))
    return parts


def total_length(intervals):
    """Number of integers covered by the intervals, counting overlaps once."""
    return sum(end - start + 1 for start, end in merge_intervals(intervals))


def prefix_sums(values):
    """sums[j] - sums[i] == sum(values[i:j])."""
    return [0, *accumulate(values)]
