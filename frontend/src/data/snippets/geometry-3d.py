DIRS_3D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def surface_area(cubes):
    """Faces not touching another cube. cubes is a set of (x, y, z)."""
    return sum(
        (x + dx, y + dy, z + dz) not in cubes
        for x, y, z in cubes
        for dx, dy, dz in DIRS_3D
    )


def exterior_surface(cubes):
    """Faces reachable from outside: flood fill the air in a box one larger than the shape."""
    low = min(min(cube) for cube in cubes) - 1
    high = max(max(cube) for cube in cubes) + 1
    start = (low, low, low)
    seen, stack, faces = {start}, [start], 0
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in DIRS_3D:
            neighbour = (x + dx, y + dy, z + dz)
            if not all(low <= v <= high for v in neighbour):
                continue
            if neighbour in cubes:
                faces += 1  # air touching a cube face from outside
            elif neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return faces
