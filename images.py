import pygame
import os
from settings import IMAGES_ROOT

try:
    BUTTONS_IMAGES = {
        "blue-button": pygame.image.load(os.path.join(IMAGES_ROOT, "button1-blue.png")),
        "red-button": pygame.image.load(os.path.join(IMAGES_ROOT, "button1-red.png"))
    }
    BG_IMAGE = pygame.image.load(os.path.join(IMAGES_ROOT, "main-background.png"))
    LEVEL_IMG = pygame.image.load(os.path.join(IMAGES_ROOT, "level-bg.png"))
    BLOCK_IMAGE = pygame.image.load(os.path.join(IMAGES_ROOT, "block.png"))
    TREASURE_IMAGE = pygame.image.load(os.path.join(IMAGES_ROOT, "treasure.png"))
    PLAYER_IMAGE = pygame.image.load(os.path.join(IMAGES_ROOT, "player.png"))
    TEXT_BG_IMAGE = pygame.image.load(os.path.join(IMAGES_ROOT, "text_bg.png"))

except pygame.error:
    print("Missing images")
    exit()
