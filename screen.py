from constants import HAND_TILE_SIZE, WIDTH, HEIGHT, WHITE_ANT_IMAGE, \
    WHITE_BEETLE_IMAGE, WHITE_GRASSHOPPER_IMAGE, WHITE_QUEEN_IMAGE, \
    WHITE_SPIDER_IMAGE, BLACK_ANT_IMAGE, BLACK_BEETLE_IMAGE, \
    BLACK_GRASSHOPPER_IMAGE, BLACK_QUEEN_IMAGE, BLACK_SPIDER_IMAGE, \
    GREEN_TILE_IMAGE, TILE_RADIUS
from topology import cube_to_xy

def print_hands(screen, state):
    white, black = state.players
    
    # White hand
    for i in range(0, white.hand[state.queen]):
        screen.blit(WHITE_QUEEN_IMAGE, (10 + (i * 10), 10))
    for i in range(0, white.hand[state.beetle]):
        screen.blit(WHITE_BEETLE_IMAGE, (10 + (i * 10), 110))
    for i in range(0, white.hand[state.ant]):
        screen.blit(WHITE_ANT_IMAGE, (10 + (i * 10), 210))
    for i in range(0, white.hand[state.grasshopper]):
        screen.blit(WHITE_GRASSHOPPER_IMAGE, (10 + (i * 10), 310))
    for i in range(0, white.hand[state.spider]):
        screen.blit(WHITE_SPIDER_IMAGE, (10 + (i * 10), 410))

    # Black hand
    for i in range(0, black.hand[state.queen]):
        screen.blit(BLACK_QUEEN_IMAGE, (10 + (i * 10), 514))
    for i in range(0, black.hand[state.beetle]):
        screen.blit(BLACK_BEETLE_IMAGE, (10 + (i * 10), 614))
    for i in range(0, black.hand[state.ant]):
        screen.blit(BLACK_ANT_IMAGE, (10 + (i * 10), 714))
    for i in range(0, black.hand[state.grasshopper]):
        screen.blit(BLACK_GRASSHOPPER_IMAGE, (10 + (i * 10), 814))
    for i in range(0, black.hand[state.spider]):
        screen.blit(BLACK_SPIDER_IMAGE, (10 + (i * 10), 914))

def get_tile_pos(coord):
    x, y = cube_to_xy(coord, TILE_RADIUS)

    return (HEIGHT // 2 + x, WIDTH // 2 + y)

def print_selections(screen, state, selected_tile):
    if not selected_tile:
        return

    action_type, tile, tile_coord = selected_tile
    
    if action_type == 'place':
        coordinates = state.placeable()

        for coordinate in coordinates:
            pos = get_tile_pos(coordinate)
            screen.blit(GREEN_TILE_IMAGE, pos)
    elif action_type == 'move':
        movements = list(filter(lambda move: move[0] == 'move' and move[1] == tile_coord , state.available_moves()))
        
        for movement in movements:
            pos = get_tile_pos(movement[2])
            screen.blit(GREEN_TILE_IMAGE, pos)

def print_board(screen, state):
    for coord in state.grid.keys():
        white, black = state.players
        player, tile = state.grid[coord]
        pos = get_tile_pos(coord)

        if player == white:
            if tile == state.queen:
                screen.blit(WHITE_QUEEN_IMAGE, pos)
            elif tile == state.ant:
                screen.blit(WHITE_ANT_IMAGE, pos)
            elif tile == state.spider:
                screen.blit(WHITE_SPIDER_IMAGE, pos)
            elif tile == state.grasshopper:
                screen.blit(WHITE_GRASSHOPPER_IMAGE, pos)
            elif tile == state.beetle:
                screen.blit(WHITE_BEETLE_IMAGE, pos)
        else:
            if tile == state.queen:
                screen.blit(BLACK_QUEEN_IMAGE, pos)
            elif tile == state.ant:
                screen.blit(BLACK_ANT_IMAGE, pos)
            elif tile == state.spider:
                screen.blit(BLACK_SPIDER_IMAGE, pos)
            elif tile == state.grasshopper:
                screen.blit(BLACK_GRASSHOPPER_IMAGE, pos)
            elif tile == state.beetle:
                screen.blit(BLACK_BEETLE_IMAGE, pos)