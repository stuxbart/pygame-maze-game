import os
from settings import *
from images import *


class LevelsList:
    class LevelListElement:
        def __init__(self, path):
            self.path = path
            self.name = path.split(".")[0][:5]
            self.next = None

    def __init__(self):
        self._list = []

        try:
            levels = os.listdir(LEVELS_ROOT)
            for i, filename in enumerate(levels):
                self._list.append(LevelsList.LevelListElement(filename))
                if i != 0:
                    self._list[i - 1].next = self._list[i]
        except FileNotFoundError:
            print("maps not found")
            exit()

    def __getitem__(self, item):
        return self._list[item]


LEVELS = LevelsList()


def load_map(filename):
    if os.path.exists(filename):
        array = []
        objective_pos = []
        player_pos = []
        with open(filename, "r") as file:
            for i, line in enumerate(file):
                row = []
                for j, field in enumerate(line):
                    if field == "S":
                        objective_pos = j, i
                    elif field == "A":
                        player_pos = j, i
                    row.append(field)
                array.append(row)
        return array, objective_pos, player_pos
    return None, None, None


class Map:
    def __init__(self, filename, win_callback):
        self.win_callback = win_callback
        self.arr, _, self.player_start_pos = load_map(filename)
        if self.arr is None:
            print("cannot load the map")
            exit()

        self.map_width = len(self.arr[0]) * BLOCK_SIZE
        self.map_height = len(self.arr) * BLOCK_SIZE

        if self.map_width < WINDOW_SIZE[0]:
            self.draw_dx = (WINDOW_SIZE[0] - self.map_width) / 2 + BLOCK_SIZE / 2
        else:
            self.draw_dx = 0

        if self.map_height < WINDOW_SIZE[1]:
            self.draw_dy = (WINDOW_SIZE[1] - self.map_height) / 2
        else:
            self.draw_dy = 0

        self.block_img = pygame.transform.smoothscale(BLOCK_IMAGE, (BLOCK_SIZE, BLOCK_SIZE))
        self.chest_img = pygame.transform.smoothscale(TREASURE_IMAGE, (BLOCK_SIZE, BLOCK_SIZE))

    def calculate_delta_draw(self, player_x, player_y, player_w, player_h):
        if player_x + self.draw_dx > WINDOW_SIZE[0] - 200 - player_w:
            self.draw_dx = (WINDOW_SIZE[0] - 200 - player_w) - player_x

        elif player_x + self.draw_dx < 200:
            self.draw_dx = 200 - player_x

        if player_y + self.draw_dy > WINDOW_SIZE[1] - 200 - player_h:
            self.draw_dy = (WINDOW_SIZE[1] - 200 - player_h) - player_y

        elif player_y + self.draw_dy < 200:
            self.draw_dy = 200 - player_y

    def draw(self, window):
        for i, row in enumerate(self.arr):
            for j, block in enumerate(row):
                if block == "#":
                    window.blit(self.block_img,
                                [int(j * BLOCK_SIZE + self.draw_dx),
                                 int(i * BLOCK_SIZE + self.draw_dy), BLOCK_SIZE, BLOCK_SIZE])
                elif block == "S":
                    window.blit(self.chest_img,
                                [int(j * BLOCK_SIZE + self.draw_dx),
                                 int(i * BLOCK_SIZE + self.draw_dy), BLOCK_SIZE, BLOCK_SIZE])

    def check_collision(self, new_x, new_y, w, h):
        for i, row in enumerate(self.arr):
            for j, block in enumerate(row):
                if block == "#":
                    if new_x < j * BLOCK_SIZE + BLOCK_SIZE and new_x + w > j * BLOCK_SIZE and \
                            new_y < i * BLOCK_SIZE + BLOCK_SIZE and new_y + h > i * BLOCK_SIZE:
                        return True
                elif block == "S":
                    if new_x < j * BLOCK_SIZE + BLOCK_SIZE and new_x + w > j * BLOCK_SIZE and \
                            new_y < i * BLOCK_SIZE + BLOCK_SIZE and new_y + h > i * BLOCK_SIZE:
                        self.win_callback()
                        return True
        return False
