import pygame

WINDOW_SIZE = (1000, 600)
BLOCK_SIZE = 50

KEYS = {
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT],
}
LEVELS_ROOT = './levels'
IMAGES_ROOT = "./img"
BEST_RESULTS = "best_results.txt"
