import os
from gui_elements import Button, Image, Text
from settings import *
from levels import LEVELS, Map
from player import Player
from images import *
from clock import Clock


class Scene:
    def __init__(self, parent):
        self.parent = parent
        self.to_draw = []

    def draw(self, window):
        for d in self.to_draw:
            d.draw(window)

    def clicked(self, x, y):
        for d in self.to_draw:
            if isinstance(d, Button):
                clicked = d.check_clicked(x, y)
                if clicked:
                    break

    def get_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 1:
                self.clicked(x, y)

    def resize(self, w, h):
        pass


class MainMenuScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        btn_width = 0.4 * WINDOW_SIZE[0]
        btn_height = 0.12 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - btn_width / 2
        bt1_y = 0.3 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt1_y, int(btn_width), 120, "Start", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.start_game)
        self.to_draw.append(self.start_btn)

        bt2_y = 0.55 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt2_y, int(btn_width), 120, "Instruction", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.instruction)
        self.to_draw.append(self.start_btn)

        bt3_y = 0.8 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt3_y, int(btn_width), 120, "Exit", BUTTONS_IMAGES["red-button"])
        self.start_btn.connect(self.exit)
        self.to_draw.append(self.start_btn)

    def start_game(self):
        self.parent.change_scene("select_level")

    def instruction(self):
        self.parent.change_scene("instruction_scene")

    def exit(self):
        self.parent.change_scene("exit_scene")


class ExitScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        img_width = 0.8 * WINDOW_SIZE[0]
        img_height = 0.3 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - img_width / 2
        bt1_y = 0.3 * WINDOW_SIZE[1] - img_height / 2

        self.text_bg = Image(b1_x, bt1_y, img_width, img_height, TEXT_BG_IMAGE)
        self.to_draw.append(self.text_bg)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.3 * WINDOW_SIZE[1]

        self.text = Text(text_x, text_y, "Are you sure you want to leave?")
        self.to_draw.append(self.text)

        btn_width = 0.3 * WINDOW_SIZE[0]
        btn_height = 0.15 * WINDOW_SIZE[1]
        b1_x = 0.25 * WINDOW_SIZE[0] - btn_width / 2
        bt1_y = 0.7 * WINDOW_SIZE[1] - btn_height / 2

        self.start_btn = Button(b1_x, bt1_y, btn_width, btn_height, "Back", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.back)
        self.to_draw.append(self.start_btn)

        b2_x = 0.75 * WINDOW_SIZE[0] - btn_width / 2
        self.start_btn = Button(b2_x, bt1_y, btn_width, btn_height, "Exit", BUTTONS_IMAGES["red-button"])
        self.start_btn.connect(self.exit)
        self.to_draw.append(self.start_btn)

        self.previous_scene = None

    def back(self):
        if self.previous_scene:
            self.parent.change_scene(self.previous_scene)
            self.previous_scene = None
        else:
            self.parent.change_scene("main_menu")

    def exit(self):
        self.parent.exit()


class InGameExitMenu(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        btn_width = 0.4 * WINDOW_SIZE[0]
        btn_height = 0.12 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - btn_width / 2
        bt1_y = 0.3 * WINDOW_SIZE[1] - btn_height / 2

        self.start_btn = Button(b1_x, bt1_y, int(btn_width), 120, "Back", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.back)
        self.to_draw.append(self.start_btn)

        bt2_y = 0.55 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt2_y, int(btn_width), 120, "Main Menu", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.main_menu)
        self.to_draw.append(self.start_btn)

        bt3_y = 0.8 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt3_y, int(btn_width), 120, "Exit", BUTTONS_IMAGES["red-button"])
        self.start_btn.connect(self.exit)
        self.to_draw.append(self.start_btn)

        self.previous_scene = None

    def back(self):
        if self.previous_scene:
            self.parent.change_scene(self.previous_scene)
            if self.previous_scene == "game_scene":
                self.parent.scenes["game_scene"].start()
            self.previous_scene = None
        else:
            self.parent.change_scene("main_menu")

    def main_menu(self):
        self.parent.change_scene("main_menu")

    def exit(self):
        self.parent.scenes["exit_scene"].previous_scene = self.parent.current_scene_name
        self.parent.change_scene("exit_scene")


class SelectLevelScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        img_width = 0.6 * WINDOW_SIZE[0]
        img_height = 0.2 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - img_width / 2
        bt1_y = 0.15 * WINDOW_SIZE[1] - img_height / 2

        self.text_bg = Image(b1_x, bt1_y, img_width, img_height, TEXT_BG_IMAGE)
        self.to_draw.append(self.text_bg)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.15 * WINDOW_SIZE[1]

        self.text = Text(text_x, text_y, "Select level")
        self.to_draw.append(self.text)

        self.start_btn = Button(50, 50, 100, 40, "Back", BUTTONS_IMAGES["blue-button"], text_size=20)
        self.start_btn.connect(self.back)
        self.to_draw.append(self.start_btn)

        self.buttons = []

        for i, level in enumerate(LEVELS):
            per_row = 3
            k = i // per_row
            x = 225 + i * 200 - 200 * per_row * k
            y = 200 + 200 * k
            b = Button(x, y, 150, 150, level.name, LEVEL_IMG)

            b.connect(lambda next_level=level: self.select_map(next_level))
            self.to_draw.append(b)
            self.buttons.append(b)

    def back(self):
        self.parent.change_scene("main_menu")

    def select_map(self, level):
        self.parent.load_map(level)

    def get_input(self, event):
        super(SelectLevelScene, self).get_input(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                for b in self.buttons:
                    bx = b.pos_x
                    by = b.pos_y
                    b.change_position(bx, by + 10)
                self.text_bg.pos_y += 10
                self.text.pos_y += 10
            elif event.button == 5:
                for b in self.buttons:
                    bx = b.pos_x
                    by = b.pos_y
                    b.change_position(bx, by - 10)
                self.text_bg.pos_y -= 10
                self.text.pos_y -= 10


class InstructionScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        img_width = 0.7 * WINDOW_SIZE[0]
        img_height = 0.5 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - img_width / 2
        bt1_y = 0.5 * WINDOW_SIZE[1] - img_height / 2

        self.text_bg = Image(b1_x, bt1_y, img_width, img_height, TEXT_BG_IMAGE)
        self.to_draw.append(self.text_bg)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.35 * WINDOW_SIZE[1]

        self.text = Text(text_x, text_y, "Welcome in the maze", size=40)
        self.to_draw.append(self.text)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.5 * WINDOW_SIZE[1]
        self.text1 = Text(text_x, text_y, "Your goal is to find the treasure", size=30)
        self.to_draw.append(self.text1)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.6 * WINDOW_SIZE[1]
        self.text2 = Text(text_x, text_y, "Control: A, W, S, D", size=30)
        self.to_draw.append(self.text2)

        self.start_btn = Button(50, 50, 100, 40, "Back", BUTTONS_IMAGES["blue-button"], text_size=20)
        self.start_btn.connect(self.back)
        self.to_draw.append(self.start_btn)

    def back(self):
        self.parent.change_scene("main_menu")

    def select_map(self, level):
        self.parent.load_map(level)


class WinScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.best_time = ""
        self.last_time = ""

        self.bg = Image(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], BG_IMAGE)
        self.to_draw.append(self.bg)

        img_width = 0.8 * WINDOW_SIZE[0]
        img_height = 0.4 * WINDOW_SIZE[1]
        b1_x = 0.5 * WINDOW_SIZE[0] - img_width / 2
        bt1_y = 0.3 * WINDOW_SIZE[1] - img_height / 2

        self.text_bg = Image(b1_x, bt1_y, img_width, img_height, TEXT_BG_IMAGE)
        self.to_draw.append(self.text_bg)

        text_x = 0.5 * WINDOW_SIZE[0]
        text_y = 0.25 * WINDOW_SIZE[1]

        self.text = Text(text_x, text_y, "Congratulations")
        self.to_draw.append(self.text)

        last_time_text_x = 0.5 * WINDOW_SIZE[0]
        last_time_text_y = 0.37 * WINDOW_SIZE[1]
        self.last_time_text = Text(last_time_text_x, last_time_text_y, "", size=30)
        self.to_draw.append(self.last_time_text)

        best_time_text_x = 0.5 * WINDOW_SIZE[0]
        best_time_text_y = 0.42 * WINDOW_SIZE[1]
        self.best_time_text = Text(best_time_text_x, best_time_text_y, "", size=30)
        self.to_draw.append(self.best_time_text)

        btn_width = 0.4 * WINDOW_SIZE[0]
        btn_height = 0.15 * WINDOW_SIZE[1]

        b1_x = 0.5 * WINDOW_SIZE[0] - btn_width / 2
        bt1_y = 0.6 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt1_y, btn_width, btn_height, "Try again", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.previous)
        self.to_draw.append(self.start_btn)

        b1_x = 0.27 * WINDOW_SIZE[0] - btn_width / 2
        bt1_y = 0.8 * WINDOW_SIZE[1] - btn_height / 2
        self.start_btn = Button(b1_x, bt1_y, btn_width, btn_height, "Main Menu", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.back)
        self.to_draw.append(self.start_btn)

        btn2_width = 0.4 * WINDOW_SIZE[0]
        b2_x = 0.73 * WINDOW_SIZE[0] - btn_width / 2
        self.start_btn = Button(b2_x, bt1_y, btn2_width, btn_height, "Next level", BUTTONS_IMAGES["blue-button"])
        self.start_btn.connect(self.next)
        self.to_draw.append(self.start_btn)

        self.next_lvl = None
        self.previous_lvl = None

    def back(self):
        self.parent.change_scene("main_menu")

    def previous(self):
        if self.previous_lvl is not None:
            self.parent.load_map(self.previous_lvl)
        else:
            self.parent.change_scene("select_level")

    def next(self):
        if self.next_lvl is not None:
            self.parent.load_map(self.next_lvl)
        else:
            self.parent.change_scene("select_level")

    def set_times(self, best, last):
        self.best_time = best
        self.last_time = last
        self.last_time_text.set_text(f"Your time: {self.last_time:.2f}s")
        self.best_time_text.set_text(f"The best time: {self.best_time:.2f}s")


class GameScene(Scene):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_map = None
        self.player = None
        self.clock = Clock()

        img_width = 0.15 * WINDOW_SIZE[0]
        img_height = 0.1 * WINDOW_SIZE[1]
        b1_x = 0.1 * WINDOW_SIZE[0] - img_width / 2
        bt1_y = 0.1 * WINDOW_SIZE[1] - img_height / 2

        self.text_bg = Image(b1_x, bt1_y, img_width, img_height, TEXT_BG_IMAGE)
        self.to_draw.append(self.text_bg)

        text_x = 0.1 * WINDOW_SIZE[0]
        text_y = 0.1 * WINDOW_SIZE[1]

        self.time_text = Text(text_x, text_y, str(self.clock.time)+"s", size=30)
        self.to_draw.append(self.time_text)

        self.level = None
        self.started = False

    def back(self):
        self.parent.change_scene("main_menu")

    def load_map(self, level):
        self.level = level
        full_path = os.path.join(LEVELS_ROOT, level.path)
        if os.path.exists(full_path):
            self.current_map = Map(full_path, self.win)
            px, py = self.current_map.player_start_pos
            self.player = Player(px, py, map_obj=self.current_map)
            self.clock.reset_time()
            self.started = False

    def draw(self, window):
        self.clock.tick()
        self.time_text.set_text(f"{self.clock.time:.2f}s")
        window.fill((57, 59, 82))
        if self.current_map:
            self.current_map.draw(window)
            self.player.draw(window)
        super().draw(window)

    def get_input(self, event):
        super(GameScene, self).get_input(event)
        if self.player:
            res = self.player.get_input(event)
            if not self.started and res:
                self.started = True
                self.start()

    def reset(self):
        self.clock.reset_time()

    def start(self):
        self.clock.tick()
        self.clock.start()

    def stop(self):
        self.player.speed_x = 0.0
        self.player.speed_y = 0.0
        self.clock.stop()

    def win(self):
        self.clock.stop()
        self.started = False
        map_name = self.level.path.split(".")[0]
        best = check_result(map_name, self.clock.time)
        self.parent.change_scene("win_scene")
        self.parent.scenes["win_scene"].next_lvl = self.level.next
        self.parent.scenes["win_scene"].previous_lvl = self.level
        self.parent.scenes["win_scene"].set_times(best, self.clock.time)
        self.current_map = None
        self.player = None


def check_result(map_name, time):
    if os.path.exists(BEST_RESULTS):
        with open(BEST_RESULTS, "r+") as f:
            best = time
            dic = {}
            for line in f:
                if line != "":
                    try:
                        map_n, map_t = line.split("-")
                        dic[map_n] = float(map_t)
                    except ValueError:
                        pass
            if map_name in dic:
                if time < dic[map_name]:
                    dic[map_name] = time
                else:
                    best = dic[map_name]
            else:
                dic[map_name] = time
            f.seek(0, 0)
            for k, v in dic.items():
                f.write(f"{k}-{v}\n")
    else:
        with open(BEST_RESULTS, "w") as f:
            best = time
            f.write(f"{map_name}-{time}\n")
    return best
