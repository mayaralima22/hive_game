from topology import offsets, add_coordinates


class Tile(object):
    name = None

    def __init__(self, state) -> None:
        super().__init__()
        self.state = state

    def moves(self, coordinate):
        return iter(())

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def __deepcopy__(self, memo):
        return self  

class Queen(Tile):
    name = 'queen'

    def moves(self, coordinate, state):
        return state.trace_contour(coordinate, 1)

class Spider(Tile):
    name = 'spider'

    def moves(self, coordinate, state):
        return state.trace_contour(coordinate, 3)


class Beetle(Tile):
    name = 'beetle'

    def moves(self, coordinate, state):
        return state.trace_contour(coordinate, 1)


class Ant(Tile):
    name = 'ant'

    def moves(self, coordinate, state):
        return state.find_contour(exclude=(coordinate,))


class Grasshopper(Tile):
    name = 'grasshopper'

    def moves(self, coordinate, state):
        for direction in offsets:
            p = add_coordinates(coordinate, direction)

            if p in state.grid:
                while p in state.grid:
                    p = add_coordinates(p, direction)
                yield p