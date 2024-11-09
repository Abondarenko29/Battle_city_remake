import pygame as pg
from classes import *
from mapmanager import load_map

pg.mixer.init()
pg.init()
pg.font.init()

                            # Звуки #  
maps = ("levels/level1.txt", "levels/level2.txt")
background_music = pg.mixer.music.load("files/background_music.mp3")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)
shoot_sound = pg.mixer.Sound("files/bullet_sound.mp3")

                            # Экран #
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Battle City Remake")
clock = pg.time.Clock()


                            # Сам Цикл #
def game_loop():  
    i = 0                                 
    walls, player, enemies = load_map("levels/level1.txt")  # Загрузка карты #

    bullets = pg.sprite.Group()
    explosions = pg.sprite.Group()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bullet = player.shoot(bullets)

                if event.key == pg.K_ESCAPE:
                    pause_menu(screen)

        player.update(walls)
        for enemy in enemies:
            enemy.update(player, walls)
        bullets.update()
        explosions.update()
        for enemy in enemies:
            enemy.ai(player, bullets)
        for enemy in all_enemies:
            enemy.update(player, walls)
        pg.sprite.groupcollide(bullets, walls, True, False)
        for enemy in enemies:
            if enemy.alive:
                for bullet in bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        explosion = Explosion(enemy.rect.centerx,
                                            enemy.rect.centery)
                        explosions.add(explosion)
                        bullet.kill()
                        enemy.kill()
                        conditional = True
                        if conditional and (i + 1) != len(maps):
                            i += 1
                            walls, player, enemy = load_map(maps[i])
                        else:
                            win(screen)
        if player.alive:
            for bullet in bullets:
                if bullet.rect.colliderect(player.rect):
                    explosion = Explosion(player.rect.centerx,
                                          player.rect.centery)
                    explosions.add(explosion)
                    bullet.kill()
                    player.kill()
                    game_over(screen)
                    
        screen.fill(BACKGROUND_COLOR)
        if player.alive:
            screen.blit(player.image, player.rect)
        
        for enemy in enemies:
            if enemy.alive:
                screen.blit(enemy.image, enemy.rect)
            
        walls.draw(screen)
        bullets.draw(screen)
        explosions.draw(screen)
        pg.display.flip()
        clock.tick(60)


main_menu(screen)
game_loop()