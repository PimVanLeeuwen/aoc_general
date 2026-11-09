# Cube coordinates (q, r, s) with q + r + s == 0 for every hex.
# These are flat-topped directions (n, ne, se, s, sw, nw). For pointy-topped
# grids (e, se, sw, w, nw, ne) use the same idea with these rotated by 30 degrees.
HEX_DIRS = {
    "n": (0, -1, 1), "ne": (1, -1, 0), "se": (1, 0, -1),
    "s": (0, 1, -1), "sw": (-1, 1, 0), "nw": (-1, 0, 1),
}


def hex_distance(a, b=(0, 0, 0)):
    """Fewest hex steps between two cube coordinates."""
    return max(abs(x - y) for x, y in zip(a, b))


def walk(steps):
    q = r = s = 0
    for step in steps.split(","):
        dq, dr, ds = HEX_DIRS[step]
        q, r, s = q + dq, r + dr, s + ds
    return q, r, s
