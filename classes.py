import pygame as pg
import sys


WIDTH, HEIGHT = 1980, 1080
BACKGROUND_COLOR = (30, 30, 30)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
HOVER_COLOR = (120, 100, 100)
RESPAWN_DELAY = 3000 
clock = pg.time.Clock()

pg.init()
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
    def init(self, x, y, image_path="files/wall.png"):
        super().__init__()

    def __init__(self, x, y, image_path):
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

    def blit(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


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
