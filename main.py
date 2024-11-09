import pygame as pg
from classes import *
from mapmanager import load_map
from tkinter import messagebox
pg.mixer.init()
pg.init()
pg.font.init()
# Звуки #
background_music = pg.mixer.music.load("files/background_music.mp3")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)

shoot_sound = pg.mixer.Sound("files/bullet_sound.mp3")
# Экран #
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Battle City Remake")
clock = pg.time.Clock()

def game_over_screen(screen):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        mx, my = pg.mouse.get_pos()

        # Отображение текста "Tank Destroyed"
        draw_text("Tank Destroyed", font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 2 - 100)

        # Кнопка "Start Again"
        button_restart = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        draw_button("Start Again", button_restart.x, button_restart.y, button_restart.width, button_restart.height, screen, button_restart.collidepoint((mx, my)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_restart.collidepoint((mx, my)):
                    return  # Завершает экран окончания и перезапускает игру

        pg.display.flip()
        clock.tick(60)
                            # Сам Цикл #
def game_loop():
    walls, player, enemy = load_map("map.txt")
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
        enemy.update(player, walls)
        bullets.update()
        explosions.update()
        enemy.ai(player, bullets)

        pg.sprite.groupcollide(bullets, walls, True, False)
        if enemy.alive:
            for bullet in bullets:
                if bullet.rect.colliderect(enemy.rect):
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                    explosions.add(explosion)
                    bullet.kill()
                    enemy.kill()
        if player.alive:
            for bullet in bullets:
                if bullet.rect.colliderect(player.rect):
                    explosion = Explosion(player.rect.centerx, player.rect.centery)
                    explosions.add(explosion)
                    bullet.kill()
                    player.kill()
                    game_over_screen(screen)  # Переход на экран окончания
                    return  # Завершение игрового цикла

        screen.fill(BACKGROUND_COLOR)
        if enemy.alive:
            screen.blit(enemy.image, enemy.rect)
        if player.alive:
            screen.blit(player.image, player.rect)
        walls.draw(screen)
        bullets.draw(screen)
        explosions.draw(screen)
        pg.display.flip()
        clock.tick(60)


def main():
    while True:
        main_menu(screen)
        game_loop()

if __name__ == "__main__":
    main()
