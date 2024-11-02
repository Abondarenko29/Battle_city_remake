from classes import *
                                     # Менеджер карты#  
def load_map(filename):
    walls = pg.sprite.Group()
    player = None
    enemy = None

    with open(filename, 'r') as f:
        lines = f.readlines()
        map_width = len(lines[0].strip()) * 50  
        map_height = len(lines) * 50            

    offset_x = (WIDTH - map_width) // 2
    offset_y = (HEIGHT - map_height) // 2
    
                                        # Чтение карты #
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == 'W':
                walls.add(Wall(x * 50 + offset_x, y * 50 + offset_y))
            elif char == 'P':
                player = Player(x * 50 + offset_x, y * 50 + offset_y, "files/Tank.png")
            elif char == 'E':
                enemy = Enemy(x * 50 + offset_x, y * 50 + offset_y, "files/Tank_enemy.png")

    return walls, player, enemy