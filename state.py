import math
import random
from collections import defaultdict
from copy import deepcopy

from topology import get_neighbors
from tiles import Queen, Ant, Beetle, Grasshopper, Spider
from player import Player

class State:
    def __init__(self) -> None:
        self.queen = Queen(self)
        self.spider = Spider(self)
        self.grasshopper = Grasshopper(self)
        self.ant = Ant(self)
        self.beetle = Beetle(self)
        self.players = (
            Player('white', self.queen, self.spider, self.beetle, self.grasshopper, self.ant),
            Player('black', self.queen, self.spider, self.beetle, self.grasshopper, self.ant)
        )
        self.grid = {}
        self.move_number = 0

    def find_contour(self, exclude=None):
        """Returns all contour coordinates of the hive"""
        contour = set()

        for coordinate in self.grid:
            if coordinate not in exclude:
                for neighbor in get_neighbors(coordinate):
                    contour.add(neighbor)

        contour.difference_update(set(self.grid.keys()))

        return contour

    def trace_contour(self, coordinate, steps=1):
        """Returns the two coordinates n steps away from coordinate along
        the hive contour."""
        contour = self.find_contour(exclude=(coordinate,))
        visited = set()
        todo = [(coordinate, 0)]

        while todo:
            c, n = todo.pop()

            for neighbor in get_neighbors(c):
                if neighbor in contour and neighbor not in visited:
                    visited.add(neighbor)

                    if n == steps:
                        yield c
                    else:
                        todo.append((neighbor, n + 1))

    def round(self):
        return self.move_number // 2

    def player(self):
        return self.players[self.move_number % len(self.players)]

    def opponent(self):
        return self.players[(self.move_number + 1) % len(self.players)]

    def do(self, move):
        player = self.player()
        action, arg1, arg2 = move

        if action == 'place':
            tile, coordinate = arg1, arg2
            self.grid[coordinate] = player, tile
            player.hand[tile] -= 1
        elif action == 'move':
            value = self.grid.pop(arg1)
            self.grid[arg2] = value
        elif action == 'nothing':
            pass
        else:
            print("UNKNOWN MOVE")

        self.move_number += 1

    def undo(self, move):
        white, black = self.players
        player = white if self.player() == black else black
        action, arg1, arg2 = move

        if action == 'place':
            tile, coordinate = arg1, arg2
            del self.grid[coordinate]
            player.hand[tile] += 1
        elif action == 'move':
            value = self.grid.pop(arg2)
            self.grid[arg1] = value
        elif action == 'nothing':
            pass
        else:
            print("UNKNOWN MOVE")

        self.move_number -= 1

    def find(self, player_needle, tile_needle):
        for c, v in self.grid.items():
            player, tile = v

            if tile == tile_needle and player == player_needle:
                return c

        return None

    def is_looser(self, player):
        queen_coordinate = self.find(player, self.queen)

        if queen_coordinate:
            if all(n in self.grid for n in get_neighbors(queen_coordinate)):
                return True

        return False

    def winner(self):
        white, black = self.players

        if self.is_looser(white):
            return black

        if self.is_looser(black):
            return white

        return None

    def placeable(self):
        """Returns all coordinates where the given player can
        _place_ a tile."""
        players = defaultdict(set)

        for coordinate, value in self.grid.items():
            player, _ = value

            for n in get_neighbors(coordinate):
                players[player].add(n)

        # All neighbors to any tile placed by current player...
        coordinates = players[self.player()]

        # ...except where the opponent is neighbour...
        for p in players:
            if p != self.player():
                coordinates.difference_update(players[p])

        # ...and you cannot place on top of another tile.
        coordinates.difference_update(self.grid.keys())

        return coordinates

    def one_hive(self, coordinates):
        unvisited = set(coordinates)
        todo = [unvisited.pop()]

        while todo:
            node = todo.pop()

            for neighbor in get_neighbors(node):
                if neighbor in unvisited:
                    unvisited.remove(neighbor)
                    todo.append(neighbor)

        return not unvisited

    def movements(self):
        for coordinate, value in self.grid.items():
            player, tile = value

            if player == self.player():
                coordinates = set(self.grid.keys())
                coordinates.remove(coordinate)

                if self.one_hive(coordinates):
                    for target in tile.moves(coordinate, self):
                        yield ('move', coordinate, target)

    def enumerate_hand(self, player, coordinates):
        """For a given iterable of coordinates, enumerate all available tiles"""
        for tile, count in player.hand.items():
            if count > 0:
                for c in coordinates:
                    yield 'place', tile, c

    def available_moves(self):
        if not self.grid:
            # If nothing is placed, one must place something anywhere
            anywhere = (0, 0, 0)

            return self.enumerate_hand(self.player(), [anywhere])

        if len(self.grid) == 1:
            # If single tile is placed, opponent places at neighbor
            start_tile = next(iter(self.grid))

            return self.enumerate_hand(self.player(), list(get_neighbors(start_tile)))

        placements = self.placeable()

        # If queen is still on hand...
        if self.player().hand[self.queen] > 0:
            # ...it must be placed on round 4
            if self.round() + 1 == 4:
                return [('place', self.queen, c) for c in placements]

            # ...otherwise only placements...
            return list(self.enumerate_hand(self.player(), placements))

        # ...but normally placements and movements
        available = list(self.enumerate_hand(self.player(), placements)) + list(self.movements())

        if not available:
            return [('nothing', None, None)]

        return available

    def evaluate(self):
        white, black = self.players

        white_queen = self.find(white, self.queen)
        black_queen = self.find(black, self.queen)

        white_free = len([n for n in get_neighbors(white_queen) if n not in self.grid]) if white_queen else 0
        black_free = len([n for n in get_neighbors(black_queen) if n not in self.grid]) if black_queen else 0

        return white_free - 2 * black_free

    def minimax(self, depth, alpha, beta):
        white, _ = self.players

        if depth <= 0:
            return None, self.evaluate(), 1

        the_winner = self.winner()

        if the_winner:
            return None, 1 if the_winner == white else -1, 1

        maximizing = True if self.player() == white else False
        f = max if maximizing else min
        evaluations = {}
        nn = 0
        random.shuffle(self.available_moves())
        moves = self.available_moves()

        for move in moves:
            self.do(move)
            _, e, n = self.minimax(depth - 1, alpha, beta)
            self.undo(move)

            if maximizing:
                alpha = f(alpha, e)
            else:
                beta = f(beta, e)

            evaluations[move] = e
            nn += n

            if beta <= alpha:
                break

        best = f(evaluations, key=evaluations.get)

        return best, evaluations[best], nn

    def play_randomized_ai(self):
        if not self.grid:
            moves = self.available_moves()
            move = ('place', random.choice([
                self.queen,
                self.ant,
                self.grasshopper,
                self.spider,
                self.beetle
            ]), (0, 0, 0))

            if move in moves:
                self.do(move)

        elif len(self.grid) == 1:
            moves = self.available_moves()
            move = ('place', random.choice([
                self.queen,
                self.ant,
                self.grasshopper,
                self.spider,
                self.beetle
            ]), (0, 1, -1))

            if move in moves:
                self.do(move)

        else:
            moves = self.available_moves()
            move = random.choice(moves)

            if move in moves:
                self.do(move)

        print(f'NÚMERO DE JOGADAS -------> {self.move_number} <----------')

    def play_ai(self):
        if not self.grid:
            moves = self.available_moves()
            move = ('place', random.choice([
                self.queen,
                self.ant,
                self.grasshopper,
                self.spider,
                self.beetle
            ]), (0, 0, 0))

            if move in moves:
                self.do(move)

        elif len(self.grid) == 1:
            moves = self.available_moves()
            move = ('place', random.choice([
                self.queen,
                self.ant,
                self.grasshopper,
                self.spider,
                self.beetle
            ]), (0, 1, -1))

            if move in moves:
                self.do(move)

        else:
            depth = 2

            move, _, n = self.minimax(depth, -math.inf, math.inf)

            self.do(move)

        print(f'NÚMERO DE JOGADAS -------> {self.move_number} <----------')