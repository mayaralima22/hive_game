import pygame
import os

WIDTH, HEIGHT = 1024, 1024
HAND_TILE_SIZE = 100
TILE_RADIUS = 50

# Tiles
WHITE_QUEEN_IMAGE = pygame.image.load(os.path.join('assets', 'white_queen.png'))
WHITE_SPIDER_IMAGE = pygame.image.load(os.path.join('assets', 'white_spider.png'))
WHITE_BEETLE_IMAGE = pygame.image.load(os.path.join('assets', 'white_beetle.png'))
WHITE_ANT_IMAGE = pygame.image.load(os.path.join('assets', 'white_ant.png'))
WHITE_GRASSHOPPER_IMAGE = pygame.image.load(os.path.join('assets', 'white_grasshopper.png'))
BLACK_QUEEN_IMAGE = pygame.image.load(os.path.join('assets', 'black_queen.png'))
BLACK_SPIDER_IMAGE = pygame.image.load(os.path.join('assets', 'black_spider.png'))
BLACK_BEETLE_IMAGE = pygame.image.load(os.path.join('assets', 'black_beetle.png'))
BLACK_ANT_IMAGE = pygame.image.load(os.path.join('assets', 'black_ant.png'))
BLACK_GRASSHOPPER_IMAGE = pygame.image.load(os.path.join('assets', 'black_grasshopper.png'))
GREEN_TILE_IMAGE = pygame.image.load(os.path.join('assets', 'green_tile.png'))

# Messages
WHITE_WINS_IMAGE = pygame.image.load(os.path.join('assets', 'white_wins.png'))
BLACK_WINS_IMAGE = pygame.image.load(os.path.join('assets', 'black_wins.png'))

# Backgrounds
BACKGROUNDS = [
    pygame.image.load(os.path.join('assets', 'bg01.jpg')),
    pygame.image.load(os.path.join('assets', 'bg05.jpg')),
    pygame.image.load(os.path.join('assets', 'bg07.jpg')),
    pygame.image.load(os.path.join('assets', 'bg10.jpg'))
]

COLORS = {
    'black': (0, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'grey': (128, 128, 128),
    'red': (255, 0, 0),
    'white': (255, 255, 255),
    'yellow': (255, 255, 0)
}
