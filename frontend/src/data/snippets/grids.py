DIRS_4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left (clockwise)
DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def parse_grid(text):
    """Grid as a dict {(row, col): char}. Out of bounds is simply 'not in grid'."""
    return {(r, c): ch for r, line in enumerate(text.splitlines()) for c, ch in enumerate(line)}


def find(grid, char):
    """First position of a character, e.g. the start 'S'."""
    return next(pos for pos, ch in grid.items() if ch == char)


def neighbors(grid, position, directions=DIRS_4):
    r, c = position
    for dr, dc in directions:
        if (r + dr, c + dc) in grid:
            yield r + dr, c + dc


def turn_right(direction_index):
    return (direction_index + 1) % 4  # index into DIRS_4; turn left is - 1


def rotate_clockwise(rows):
    """Rotate a list-of-strings grid 90 degrees clockwise (tilting, tile puzzles)."""
    return ["".join(column) for column in zip(*rows[::-1])]


def transpose(rows):
    return ["".join(column) for column in zip(*rows)]
