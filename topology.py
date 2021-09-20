from math import sqrt

offsets = [
    (0, -1, 1), (1, -1, 0), (1, 0, -1),
    (0, 1, -1), (-1, 1, 0), (-1, 0, 1)]


def get_neighbors(coordinate):
    """Returns cube hex neighbors"""
    x, y, z = coordinate

    for ox, oy, oz in offsets:
        yield x + ox, y + oy, z + oz

def add_coordinates(coordinate1, coordinate2):
    x1, y1, z1 = coordinate1
    x2, y2, z2 = coordinate2

    return x1 + x2, y1 + y2, z1 + z2

def cube_to_oddr(cube):
    x, y, z = cube

    return x + (z - (z & 1)) // 2, z


def cube_to_xy(cube, size):
    w = sqrt(3) * size
    h = 2 * size
    column, row = cube_to_oddr(cube)

    return (column * w + (row & 1) * w / 2, row * (h * 3/4))
