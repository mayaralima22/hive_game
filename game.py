import pygame
import random
from time import sleep
from shapely.geometry import Point, box

from constants import HAND_TILE_SIZE, WIDTH, HEIGHT, COLORS, WHITE_WINS_IMAGE, BLACK_WINS_IMAGE, BACKGROUNDS
from state import State
from screen import print_board, print_hands, print_selections, get_tile_pos

def hive():
    state = State()

    pygame.init()
    pygame.display.set_caption('Hive')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    selected_tile = None
    BACKGROUND = random.choice(BACKGROUNDS)

    while state.winner() is None:
        white, black = state.players

        if state.player() == black:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    point = Point(pos[0], pos[1])
                    
                    if state.player() == black:
                        # Click on tiles from hand
                        if box(10, 514, 110, 614).contains(point) and black.hand[state.queen] > 0:
                            selected_tile = ('place', state.queen, None)
                        elif box(10, 614, 120, 714).contains(point) and black.hand[state.beetle] > 0:
                            selected_tile = ('place', state.beetle, None)
                        elif box(10, 714, 130, 814).contains(point) and black.hand[state.ant] > 0:
                            selected_tile = ('place', state.ant, None)
                        elif box(10, 814, 130, 914).contains(point) and black.hand[state.grasshopper] > 0:
                            selected_tile = ('place', state.grasshopper, None)
                        elif box(10, 914, 120, 1014).contains(point) and black.hand[state.spider] > 0:
                            selected_tile = ('place', state.spider, None)

                        if len(state.grid) == 1 and selected_tile:
                            state.do(('place', selected_tile[1], (0, -1, 1)))
                            selected_tile = None

                        # Click on tiles from board
                        for coordinate in state.grid.keys():
                            x, y = get_tile_pos(coordinate)
                            player, tile = state.grid[coordinate]
                            tile_box = box(x, y, x + HAND_TILE_SIZE, y + HAND_TILE_SIZE)

                            if tile_box.contains(point) and player == black:
                                selected_tile = ('move', tile, coordinate)

                        # Click on green tiles
                        if selected_tile is not None:
                            for movement in list(filter(lambda move: move[0] == selected_tile[0], state.available_moves())):
                                action_type, arg1, arg2 = movement

                                if action_type == 'move' and arg1 == selected_tile[2]:
                                    x, y = get_tile_pos(arg2)
                                    tile_box = box(x, y, x + HAND_TILE_SIZE, y + HAND_TILE_SIZE)

                                    if tile_box.contains(point):
                                        state.do(('move', arg1, arg2))
                                        selected_tile = None
                                        break
                                elif action_type == 'place' and arg1 == selected_tile[1]:
                                    x, y = get_tile_pos(arg2)
                                    tile_box = box(x, y, x + HAND_TILE_SIZE, y + HAND_TILE_SIZE)

                                    if tile_box.contains(point):
                                        state.do(('place', arg1, arg2))
                                        selected_tile = None
                                        break

                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[pygame.K_SPACE]:
                        state.play_randomized_ai()

        else:
            sleep(1)
            state.play_ai()

        # Clear screen
        screen.blit(BACKGROUND, (0, 0))

        print_hands(screen, state)
        print_selections(screen, state, selected_tile)
        print_board(screen, state)

        # Update the screen
        pygame.display.update()

        # Reduce the display frequence
        clock.tick(60)

    screen.blit(WHITE_WINS_IMAGE if state.winner() == white else BLACK_WINS_IMAGE, (0, 0))
    pygame.display.update()

    sleep(5)

    hive()

if __name__ == "__main__":
    hive()