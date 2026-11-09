def regions(grid):
    """Group neighbouring cells with the same character. Returns a list of sets of (r, c)."""
    rows, cols = len(grid), len(grid[0])
    seen = set()
    result = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue
            region, stack = set(), [(r, c)]
            seen.add((r, c))
            while stack:
                cr, cc = stack.pop()
                region.add((cr, cc))
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    inside = 0 <= nr < rows and 0 <= nc < cols
                    if inside and (nr, nc) not in seen and grid[nr][nc] == grid[r][c]:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            result.append(region)
    return result


class UnionFind:
    """Merge groups as connections arrive, e.g. 'connect the closest pairs one by one'."""

    def __init__(self):
        self.parent = {}

    def find(self, item):
        self.parent.setdefault(item, item)
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]  # path halving
            item = self.parent[item]
        return item

    def union(self, a, b):
        """Join the groups of a and b. Returns False if they were already joined."""
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        self.parent[root_a] = root_b
        return True
