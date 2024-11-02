# import pygame
# import os
# PATH = os.path.dirname(__file__) + os.path.sep

# pygame.init()


# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60

# window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Танчики")

# clock = pygame.time.Clock()

# all_sprites = pygame.sprite.Group()
# player = Player() #класс гравця
# all_sprites.add(player)

# enemy = Enemy(random.randint(0,0), (0,0)) # об'єкт классу ворог, задати розміри і положення(через randint)

# running = True
# while running:

#     window.fill((255, 255, 255))
#     keys = pygame.key.get_pressed()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     player.shoot()#метод класса плеер для вистрела

#     player.move(keys) #переміщення гравця
#     player.update_bullets() #оновлення куль

#     enemy.move() #переміщення ворогів

#     for bullet in player.bullets:
#             if bullet[0].colliderect(enemy.rect):
#                 print("Ворог знищений!")
#                 player.bullets.remove(bullet)#видалення зайвих обьєктів при знищенні ворога
#                 enemy = Enemy(random.randint(0,0), (0,0))#створення нового ворога при знищенні попереднього
                              
#     pygame.draw.rect(window, PLAYER_COLOR, player.rect)#відмалювання гравця
#     pygame.draw.rect(window, ENEMY_COLOR, enemy.rect)#відмалювання ворогів

#     for bullet in player.bullets:
#         pygame.draw.rect(window, BULLET_COLOR, bullet[0])#відмалювання куль

#     clock.tick(FPS)
#     pygame.display.update()
#___________________________________________________________________________________________________________________________________________


import pygame as pg
from classes import PlayerController, ControlScreen, Screen, Player, Enemy, Wall, Button  # Імпортуємо класи з файлу classes

pg.init()

FPS = 30

width, height = 800, 600
background = (0, 0, 0)
title = "танчики"

main_screen = Screen(width, height, title, background)

player = Player(x=width // 2, y=height - 100, image="files/player.png")
enemy = Enemy(x=width // 2, y=100, image="files/enemy.png")
wall = Wall(x=300, y=250, image="files/wall.png")

main_screen.add_object(player)
main_screen.add_object(enemy)
main_screen.add_object(wall)

player_controller = PlayerController()

running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass #стрільба

    main_screen.update()

    player.update()
    player_controller.control_coords(player, width, height)

    wall.collide_rect(player)

    clock.tick(FPS)
    pg.display.update()

pg.quit()