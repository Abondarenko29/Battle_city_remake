import pygame as pg
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Battle_city")


class PlayerController:  # Клас-контролер, design-pattern
    def control_coords(self, player, width, height):
        max_x = width - 50
        max_y = height - 50
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.x > max_x:
            player.rect.x = max_x
        if player.rect.y < 0:
            player.rect.y = 0
        if player.rect.y > max_y:
            player.rect.y = max_y


class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, image, speed=3):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image),
                                        (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def route(self, vector):
        vector = vector.replace("left", "1")
        vector = vector.replace("right", "-1")
        vector = int(vector)
        self.image = pg.transform.rotate(self.image, vector * self.speed)


class ControlScreen:
    def __init__(self):
        self.screens = []
        self.index = 0

    def add_screen(self, screen):
        self.screens.append(screen)
        self.screens[self.index].set_values()

    def next_screen(self):
        self.index += 1
        self.screens[self.index].set_values()

    def last_screen(self):
        self.index -= 1
        self.screens[self.index].set_values()

    def update(self):
        self.screens[self.index].update()


class Screen:  # Екран
    def __init__(self, width, height, title, color, icon=None):
        self.window = pg.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.title = title
        self.color = color
        self.icon = icon
        self.objects = []

    def set_values(self):
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        if self.icon is not None:
            pg.display.set_icon(pg.image.load(self.icon))
        self.window.fill(self.color)

    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        for object in self.objects:
            self.window.blit(object.image, (object.rect.x, object.rect.y))
            pg.display.update()
        self.window.fill(self.color)


class Player(Sprite):
    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.route("left")
        if key[pg.K_RIGHT]:
            self.route("right")
        if key[pg.K_UP]:
            self.rect.y -= self.speed
        if key[pg.K_DOWN]:
            self.rect.y += self.speed


class Enemy(Sprite):
    def __init__(self):
        super().__init__()


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        self.image = pg.transform.scale(pg.image.load(image),
                                        (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collide_rect(self, object):  # Дотик
        if pg.sprite.collide_rect(self, object):
            if self.rect.x >= object.rect.x:
                object.rect.x -= object.speed
            elif self.rect.x <= object.rect.x:
                object.rect.x += object.speed

            if self.rect.y >= object.rect.y:
                object.rect.y -= object.speed
            elif self.rect.y <= object.rect.y:
                object.rect.y += object.speed


class Button:
    def __init__(self, text, x, y, width, height,
                 button_color, text_color):
        self.rect = pg.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.color = button_color
        self.text = pg.font.Font(None, 50)
        self.text = self.text.render(text, True, text_color)

    def check(self, event, alghoritm):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.rect.collidepoint(x, y):
                alghoritm()
