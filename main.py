import pygame
from settings import *
from scenes import MainMenuScene, ExitScene, SelectLevelScene, GameScene, WinScene, InGameExitMenu, InstructionScene

pygame.init()
pygame.font.init()


class Window:
    def __init__(self):
        self.width = WINDOW_SIZE[0]
        self.height = WINDOW_SIZE[1]

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")

        self.running = True

        self.scenes = {
            "main_menu": MainMenuScene(self),
            "exit_scene": ExitScene(self),
            "in_game_exit_scene": InGameExitMenu(self),
            "select_level": SelectLevelScene(self),
            "game_scene": GameScene(self),
            "win_scene": WinScene(self),
            "instruction_scene": InstructionScene(self),
        }
        self.current_scene_name = "main_menu"
        self.current_scene = self.scenes["main_menu"]

        self.current_map = None
        self.next_level_filename = ""

        self.clock = pygame.time.Clock()

    def run(self):

        while self.running:
            self.clock.tick(60)
            self.check_input()
            self.draw()
            pygame.display.update()

    def check_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.current_scene_name != "exit_scene":
                    if self.current_scene_name == "game_scene":
                        self.current_scene.stop()
                        self.scenes["in_game_exit_scene"].previous_scene = self.current_scene_name
                        self.change_scene("in_game_exit_scene")
                    else:
                        self.scenes["exit_scene"].previous_scene = self.current_scene_name

                        self.change_scene("exit_scene")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_scene_name != "exit_scene":
                        if self.current_scene_name == "game_scene":
                            self.current_scene.stop()
                            self.scenes["in_game_exit_scene"].previous_scene = self.current_scene_name
                            self.change_scene("in_game_exit_scene")
                        else:
                            self.scenes["exit_scene"].previous_scene = self.current_scene_name

                            self.change_scene("exit_scene")

            self.current_scene.get_input(event)

    def draw(self):
        self.current_scene.draw(self.win)

    def change_scene(self, name):
        if name in self.scenes:
            self.current_scene_name = name
            self.current_scene = self.scenes[name]
        else:
            print("the scene doesn't exist")

    def load_map(self, level):
        if "game_scene" in self.scenes:
            self.scenes["game_scene"].load_map(level)
            self.change_scene("game_scene")

    def exit(self):
        self.running = False
        pygame.quit()
        quit()


def main():
    window = Window()
    window.run()


if __name__ == "__main__":
    main()
