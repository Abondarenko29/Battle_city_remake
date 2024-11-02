import pygame as pg
import sys


WIDTH, HEIGHT = 1980, 1080
BACKGROUND_COLOR = (30, 30, 30)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
HOVER_COLOR = (120, 100, 100)
RESPAWN_DELAY = 3000 
clock = pg.time.Clock()

                                # Меню #
font = pg.font.Font(None, 50)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, w, h, surface, hover = False):
    color = HOVER_COLOR if hover else BUTTON_COLOR
    pg.draw.rect(surface, color, (x, y, w, h))
    draw_text(text, font, FONT_COLOR, surface, x + w // 2, y + h // 2)


                             # Класс игрока #
class Player(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, speed=3):
        super().__init__()
        self.original_image = pg.transform.scale(pg.image.load(image_path), (45, 45))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 0
        self.shoot_delay = 500
        self.last_shot_time = 0

    def update(self, walls):
        keys = pg.key.get_pressed()
        original_position = self.rect.topleft

        if keys[pg.K_LEFT] and not (keys[pg.K_UP] or keys[pg.K_DOWN]):
            self.rect.x -= self.speed
            self.rotate(90)
            self.direction = 90
        elif keys[pg.K_RIGHT] and not (keys[pg.K_UP] or keys[pg.K_DOWN]):
            self.rect.x += self.speed
            self.rotate(-90)
            self.direction = -90
        elif keys[pg.K_UP] and not (keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
            self.rect.y -= self.speed
            self.rotate(0)
            self.direction = 0
        elif keys[pg.K_DOWN] and not (keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
            self.rect.y += self.speed
            self.rotate(180)
            self.direction = 180

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.topleft = original_position 

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time 
            return Bullet(self.rect.centerx, self.rect.centery, self.direction)
        return None


                                # Класс пули #
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, speed=5):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 180:
            self.rect.y += self.speed
        elif self.direction == 90:
            self.rect.x -= self.speed
        elif self.direction == -90:
            self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


                                    # Класс стены #
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, image_path="files/wall.png"):
        super().__init__()
        self.image = pg.image.load(image_path)  
        self.image = pg.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect(topleft=(x, y))

        
                                        # Класс врага #
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, speed=1):
        super().__init__()
        self.original_image = pg.transform.scale(pg.image.load(image_path), (45, 45))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.alive = True
        self.respawn_timer = None
        self.spawn_pos = (x, y)

    def update(self, player, walls):
        if self.alive:
            original_position = self.rect.topleft 
            if abs(self.rect.x - player.rect.x) > abs(self.rect.y - player.rect.y):
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                    self.rotate(-90)
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
                    self.rotate(90)
            else:
                if self.rect.y < player.rect.y:
                    self.rect.y += self.speed
                    self.rotate(180)
                elif self.rect.y > player.rect.y:
                    self.rect.y -= self.speed
                    self.rotate(0)

            
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.topleft = original_position
        else:
            if self.respawn_timer and pg.time.get_ticks() - self.respawn_timer >= RESPAWN_DELAY:
                self.respawn()

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def kill(self):
        self.alive = False
        self.image.set_alpha(0)
        self.respawn_timer = pg.time.get_ticks()

    def respawn(self):
        self.alive = True
        self.image.set_alpha(255)
        self.rect.topleft = self.spawn_pos
        self.respawn_timer = None
        
        
                                            # Класс взрыва #
class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pg.transform.scale(pg.image.load("files\explosion2.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion3.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion4.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion5.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion6.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion7.png"), (100, 100)),
            pg.transform.scale(pg.image.load("files\explosion8.png"), (100, 100)),
        ]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.frame_duration = 10
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_duration:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]


                                    # Функцонал меню #
def main_menu(screen):
    while True:
        screen.fill(BACKGROUND_COLOR)
        mx, my = pg.mouse.get_pos()

        button_start = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        button_exit = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

        draw_button("Start", button_start.x, button_start.y, button_start.width, button_start.height, screen, button_start.collidepoint((mx, my)))
        draw_button("Exit", button_exit.x, button_exit.y, button_exit.width, button_exit.height, screen, button_exit.collidepoint((mx, my)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_start.collidepoint((mx, my)):
                    return  
                elif button_exit.collidepoint((mx, my)):
                    pg.quit()
                    sys.exit()

        pg.display.flip()
        clock.tick(60)

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
