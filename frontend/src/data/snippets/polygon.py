from math import gcd


def shoelace_area(corners):
    """Area of a simple polygon from its corners in order (shoelace formula)."""
    total = 0
    for (x1, y1), (x2, y2) in zip(corners, corners[1:] + corners[:1]):
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def lattice_points(corners):
    """
    (interior, boundary) grid points of a polygon with integer corners.
    Pick's theorem: area = interior + boundary / 2 - 1. For 'dig a trench
    and count the cubes inside', the answer is interior + boundary.
    """
    boundary = sum(
        gcd(abs(x2 - x1), abs(y2 - y1))
        for (x1, y1), (x2, y2) in zip(corners, corners[1:] + corners[:1])
    )
    interior = int(shoelace_area(corners) - boundary / 2 + 1)
    return interior, boundary
