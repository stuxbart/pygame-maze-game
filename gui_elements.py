import pygame


class Text:
    def __init__(self, x: int = 0, y: int = 0, text: str = "", size: int = 50,
                 color: tuple = (0, 0, 0), centered: bool = True):
        self.pos_x = int(x)
        self.pos_y = int(y)
        self.width = 0
        self.height = 0
        self.centered = centered
        self.font = pygame.font.SysFont('Arial', size)
        self.color = color
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.width, self.height = self.font.size(self.text)

    @property
    def x(self):
        if self.centered:
            return self.pos_x - int(self.width / 2)
        else:
            return self.pos_x

    @property
    def y(self):
        if self.centered:
            return self.pos_y - int(self.height / 2)
        else:
            return self.pos_y

    def draw(self, window):
        window.blit(self.surface, (int(self.x), int(self.y)))

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.width, self.height = self.font.size(self.text)


class Button:
    def __init__(self, x, y, w, h, text, bg_image, text_size=50):
        self.pos_x = int(x)
        self.pos_y = int(y)
        self.width = int(w)
        self.height = int(h)

        text_x = self.pos_x + self.width / 2
        text_y = self.pos_y + self.height / 2
        self.text = Text(int(text_x), int(text_y), text, centered=True, size=text_size)

        self.img = bg_image
        self.img_scaled = pygame.transform.smoothscale(self.img, (self.width, self.height))

        self.callback = None

    @property
    def rect(self):
        return [self.pos_x, self.pos_y, self.width, self.height]

    def connect(self, callback):
        self.callback = callback

    def draw(self, window):
        window.blit(self.img_scaled, self.rect)
        self.text.draw(window)

    def check_clicked(self, x, y):
        if self.pos_x < x < self.pos_x + self.width and self.pos_y < y < self.pos_y + self.height:
            if self.callback is not None:
                self.callback()
            return True
        return False

    def change_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.text.pos_x = self.pos_x + self.width / 2
        self.text.pos_y = self.pos_y + self.height / 2


class Image:
    def __init__(self, x, y, w, h, image):
        self.pos_x = int(x)
        self.pos_y = int(y)
        self.width = int(w)
        self.height = int(h)
        self.img = image
        self.img_scaled = pygame.transform.smoothscale(self.img, (self.width, self.height))

    @property
    def rect(self):
        return [self.pos_x, self.pos_y, self.width, self.height]

    def draw(self, window):
        window.blit(self.img_scaled, self.rect)
