from collections import Counter

DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def step(alive, rule):
    """
    One generation on an unbounded grid. alive is a set of (r, c); only live
    cells and their neighbours can change, so this scales to sparse and 3D/4D
    grids (just use longer tuples and offsets). rule(is_alive, live_neighbours) -> bool.
    """
    counts = Counter((r + dr, c + dc) for r, c in alive for dr, dc in DIRS_8)
    candidates = alive | counts.keys()
    return {cell for cell in candidates if rule(cell in alive, counts[cell])}


def game_of_life(is_alive, live_neighbours):
    return live_neighbours == 3 or (is_alive and live_neighbours == 2)
