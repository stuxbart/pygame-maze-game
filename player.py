import pygame
from settings import *
from images import *


class Player:
    def __init__(self, x, y, w=BLOCK_SIZE / 2, h=BLOCK_SIZE / 2, map_obj=None):
        self.x = x * BLOCK_SIZE + w / 2
        self.y = y * BLOCK_SIZE + h / 2
        self.w = int(w)
        self.h = int(h)
        self.img = pygame.transform.smoothscale(PLAYER_IMAGE, (self.w, self.h))

        self.map = map_obj

        self.speed = BLOCK_SIZE/50 * 5
        self.speed_x = 0
        self.speed_y = 0

    @property
    def rect(self):
        return [int(self.x + self.map.draw_dx), int(self.y + self.map.draw_dy), self.w, self.h]

    def draw(self, window):
        if self.map:
            if not self.map.check_collision(self.x + self.speed_x, self.y, self.w, self.h):
                self.x += self.speed_x
            if not self.map.check_collision(self.x, self.y + self.speed_y, self.w, self.h):
                self.y += self.speed_y
        self.map.calculate_delta_draw(self.x, self.y, self.w, self.h)
        window.blit(self.img, self.rect)

    def get_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in KEYS["left"]:
                self.speed_x = -self.speed
                return True
            elif event.key in KEYS["right"]:
                self.speed_x = self.speed
                return True
            elif event.key in KEYS["up"]:
                self.speed_y = -self.speed
                return True
            elif event.key in KEYS["down"]:
                self.speed_y = self.speed
                return True
        elif event.type == pygame.KEYUP:
            if event.key in KEYS["left"]:
                self.speed_x = 0
            elif event.key in KEYS["right"]:
                self.speed_x = 0
            elif event.key in KEYS["up"]:
                self.speed_y = 0
            elif event.key in KEYS["down"]:
                self.speed_y = 0
