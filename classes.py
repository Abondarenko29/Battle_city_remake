import pygame as pg
import sys
from random import randint


WIDTH, HEIGHT = 1980, 1080
BACKGROUND_COLOR = (30, 30, 30)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
HOVER_COLOR = (120, 100, 100)
RESPAWN_DELAY = 3000
BASE_COUNTER = 0
COUNT_TO_WIN = 10
clock = pg.time.Clock()
all_enemies = pg.sprite.Group()

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

                        # Освной класс танков#
class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, speed):
        self.original_image = pg.transform.scale(pg.image.load(image_path), (45, 45))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.alive = True
        self.direction = 0
        self.controller = ShootingTank(self, 0, 2000)

    def kill(self):
        self.alive = False
        self.image.set_alpha(0)
        del self

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, bullets, plus_x=0, plus_y=0):
        self.controller.shoot(bullets, self.direction,
                              plus_x=plus_x, plus_y=plus_y)


                             # Класс игрока #
class Player(Tank):
    def __init__(self, x, y, image_path, speed=3):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image_path, speed)

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

    def shoot(self, bullets):
        plus = {0: {"plus_y": -50},
                90: {"plus_x": -50},
                -90: {"plus_x": 50},
                180: {"plus_y": 50}}
        return self.controller.shoot(bullets, self.direction,
                                     **plus[self.direction])


class ShootingTank:
    def __init__(self, object, last_shot_time, shot_delay):
        self.object = object
        self.last_shot_time = last_shot_time
        self.shoot_delay = shot_delay

    def shoot(self, bullets, direction, plus_x=0, plus_y=0):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:

            self.last_shot_time = current_time
            bullet = Bullet(self.object.rect.centerx + plus_x,
                          self.object.rect.centery + plus_y,
                          "files/bullet.png", direction)
            pg.mixer.Sound("files/bullet_sound.mp3").play()
            bullets.add(bullet)
            self.last_shot_time = current_time


                                # Класс пули #
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, direction, speed=5):
        super().__init__()
        self.original_image = pg.transform.scale(pg.image.load(image_path), (10, 10))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = direction
        self.rotate(direction)

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

                                    # Класс врага #
class Enemy(Tank):
    def __init__(self, x, y, image_path, speed=1):
        pg.sprite.Sprite.__init__(self)
        super().__init__(x, y, image_path, speed)
        self.respawn_timer = None
        self.spawn_pos = (x, y)
        self.controller = ShootingTank(self, 0, 2000)

    def update(self, player, walls):
        if self.alive:
            original_position = self.rect.topleft
            if abs(self.rect.x - player.rect.x) > abs(self.rect.y - player.rect.y):
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                    self.rotate(-90)
                    self.direction = -90
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
                    self.rotate(90)
                    self.direction = 90
            else:
                if self.rect.y < player.rect.y:
                    self.rect.y += self.speed
                    self.rotate(180)
                    self.direction = 180
                elif self.rect.y > player.rect.y:
                    self.rect.y -= self.speed
                    self.rotate(0)
                    self.direction = 0

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.topleft = original_position
        else:
            if self.respawn_timer and pg.time.get_ticks() - self.respawn_timer >= RESPAWN_DELAY:
                self.respawn()
   
    def spawn_enemies(all_enemies, enemy_count=5):
        for i in range(enemy_count):
            x = randint(100, WIDTH - 100)
            y = randint(100, HEIGHT - 100)
            enemy = Enemy(x, y, "files\Tank_enemy.png")
            all_enemies.add(enemy)
        
    def kill(self):
        self.alive = False
        self.image.set_alpha(0)
        self.respawn_timer = pg.time.get_ticks()

    def respawn(self):
        self.alive = True
        self.image.set_alpha(255)
        self.rect.topleft = self.spawn_pos
        self.respawn_timer = None
        all_enemies.add(self)

    def ai(self, player, bullets):
        if self.alive:
            if self.direction == 0 and self.rect.y < player.rect.y and self.rect.x // 10 == player.rect.x // 10:
                self.shoot(bullets, plus_y=50)
            elif self.direction == 90 and self.rect.x > player.rect.x and self.rect.y // 10 == player.rect.y // 10:
                self.shoot(bullets, plus_x=-50)
            elif self.direction == -90 and self.rect.x < player.rect.x and self.rect.y // 10 == player.rect.y // 10:
                self.shoot(bullets, plus_x=50)
            elif self.direction == 180 and self.rect.y > player.rect.y and self.rect.x // 10 == player.rect.x // 10:
                self.shoot(bullets, plus_y=-50)
                
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
                
                                    # Функцонал Паузы #
          
def pause_menu(screen):
    paused = True
    while paused:
        screen.fill(BACKGROUND_COLOR)
        mx, my = pg.mouse.get_pos()
        
        button_return = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
        button_main_menu = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        button_exit = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

        draw_button("Return", button_return.x, button_return.y, button_return.width, button_return.height, screen, button_return.collidepoint((mx, my)))
        draw_button("Main Menu", button_main_menu.x, button_main_menu.y, button_main_menu.width, button_main_menu.height, screen, button_main_menu.collidepoint((mx, my)))
        draw_button("Exit", button_exit.x, button_exit.y, button_exit.width, button_exit.height, screen, button_exit.collidepoint((mx, my)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_return.collidepoint((mx, my)):
                    paused = False 
                elif button_main_menu.collidepoint((mx, my)):
                    main_menu(screen) 
                    paused = False
                    return
                elif button_exit.collidepoint((mx, my)):
                    pg.quit()
                    sys.exit()  

        pg.display.flip()
        clock.tick(60)
        
                                                # Смерть #
                                                
def game_over(screen):
    screen.fill(BACKGROUND_COLOR)
    draw_text("Game Over", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
    pg.display.flip()
    pg.time.wait(2000)
    main_menu(screen)
    
                                                # Победа #
                                                
def win(screen):
    screen.fill(BACKGROUND_COLOR)
    draw_text("Yesss you win!", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2)
    pg.display.flip()
    pg.time.wait(1000)
    pg.quit()
    sys.exit()