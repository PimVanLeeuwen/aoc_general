from collections import deque


def bfs(start, goal, neighbors):
    """Fewest steps from start to goal. neighbors(node) yields adjacent nodes."""
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, steps = queue.popleft()
        if node == goal:
            return steps
        for next_node in neighbors(node):
            if next_node not in seen:
                seen.add(next_node)
                queue.append((next_node, steps + 1))
    return None  # goal unreachable


def grid_neighbors(grid, wall="#"):
    """neighbors() for a grid given as a list of strings."""
    rows, cols = len(grid), len(grid[0])

    def neighbors(position):
        r, c = position
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != wall:
                yield nr, nc

    return neighbors
