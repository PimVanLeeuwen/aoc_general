def manhattan(a, b):
    """Taxicab distance in any number of dimensions."""
    return sum(abs(x - y) for x, y in zip(a, b))


def walk(instructions):
    """
    Complex numbers make turning trivial: position and heading are complex,
    with y growing downwards. Turn right = heading * 1j, turn left = heading * -1j.
    """
    position, heading = 0, -1j  # start at the origin facing up (north)
    for step in instructions.split(", "):
        heading *= 1j if step[0] == "R" else -1j
        position += heading * int(step[1:])
    return int(abs(position.real) + abs(position.imag))


def row_coverage(sensors, row):
    """
    Spans of one row within Manhattan range of each sensor (x, y, radius).
    Merge the result with the intervals snippet instead of storing every cell.
    """
    spans = []
    for x, y, radius in sensors:
        half_width = radius - abs(y - row)
        if half_width >= 0:
            spans.append((x - half_width, x + half_width))
    return spans
