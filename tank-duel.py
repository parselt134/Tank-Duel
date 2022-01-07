import pygame as pg
import numpy as np
import sys
import random
from pygame import time
from params import *


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direc, im, sign):
        super().__init__(player_group)
        self.direc = direc
        self.image = pg.transform.rotate(im, -90 * self.direc)
        self.pos = (pos_x, pos_y)
        self.sign = sign
        self.lives = 3
        self.score = 0
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1] + height_panel)

    def move(self, x, y, new_direc):
        self.image = pg.transform.rotate(pg.transform.rotate(self.image, 90 * self.direc), -90 * new_direc)
        self.direc = new_direc
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1] + height_panel)
        level_map[y, x] = self.sign


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + height_panel)


class Bonus(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonuses_group)
        self.bonus_type = random.choice(["buster", "life"])
        self.image = bonus_images[self.bonus_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + height_panel)


def generate_bonus():
    if random.random() > 0.95:
        x, y = random.randint(0, 9), random.randint(0, 9)
        while level_map[y, x] != "." and (x != 0 and y != 0 or x != 9 and y != 9):
            x, y = random.randint(0, 9), random.randint(0, 9)
        level_map[y, x] = "b"
        return Bonus(x, y)


def panel(scr, x, y, lvs, temp_score, tank_pic):  # x и у -- отступы от левого верхнего угла
    pg.draw.rect(scr, pg.Color("gray"), (0, y, WIDTH, height_panel))
    for lv in range(lvs):
        rect = tank_pic.get_rect()
        rect.x = x + (30 * lv)
        rect.y = y + 5
        scr.blit(tank_pic, rect)
    font = pg.font.Font(None, 30)
    text = font.render(str(temp_score), True, (0, 0, 0))
    text_x = x + WIDTH // 2
    text_y = y + 5
    scr.blit(text, (text_x, text_y))


def load_level(number):
    try:
        filename = "level-" + str(number) + ".map"
        filename = os.path.join("levels", filename)
        with open(filename, "r") as mapfile:
            levelmap = np.array([list(i) for i in [line.strip() for line in mapfile]])
        return levelmap
    except (FileNotFoundError, IsADirectoryError):
        print("Упс! Что-то пошло не так!")
        terminate()


def generate_level(level):
    new_player, new_player2, x, y = None, None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("bricks", x, y)
            elif level[y][x] == "=":
                Tile("water", x, y)
            elif level[y][x] == "@":
                Tile("empty", x, y)
                level_map[y, x] = "."
                new_player = Player(x, y, 2, player_image, "@")
            elif level[y][x] == "%":
                Tile("empty", x, y)
                level_map[y, x] = "."
                new_player2 = Player(x, y, 0, player2_image, "%")
    return new_player, new_player2, x, y


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    intro_text = ["Tank Duel", "", "",
                  "Нажмите любую клавишу", ""
                  "для начала игры"]
    fon = pg.image.load(os.path.join(PIC, "start_screen.png"))
    screen1 = pg.display.set_mode((500, 500))
    screen1.blit(fon, (0, 0))
    font = pg.font.Font(None, 35)
    text_coords = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coords += 10
        intro_rect.top = text_coords
        intro_rect.x = 10
        text_coords += intro_rect.height
        screen1.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        clock.tick(FPS)


def move_player(pl, movement):  # Здесь pl является сокращением от слова player
    x, y = pl.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1, x] == '.':
            level_map[y, x] = "."
            pl.move(x, y - 1, 0)
    elif movement == 'down':
        if y < level_y - 1 and level_map[y + 1, x] == '.':
            level_map[y, x] = "."
            pl.move(x, y + 1, 2)
    elif movement == 'left':
        if x > 0 and level_map[y, x - 1] == '.':
            level_map[y, x] = "."
            pl.move(x - 1, y, 3)
    elif movement == 'right':
        if x < level_x - 1 and level_map[y, x + 1] == '.':
            level_map[y, x] = "."
            pl.move(x + 1, y, 1)


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Tank Duel")
    clock = time.Clock()
    start_screen()
    screen = pg.display.set_mode(SIZE)
    group_sprites = pg.sprite.Group()
    tile_images = {
        "bricks": pg.image.load(os.path.join(PIC, "bricks.png")),
        "water": pg.image.load(os.path.join(PIC, "water.png")),
        "empty": pg.image.load(os.path.join(PIC, "grass.png"))
    }
    bonus_images = {
        "buster": pg.image.load(os.path.join(PIC, "buster.png")),
        "life": pg.image.load(os.path.join(PIC, "life.png"))
    }

    player_image = pg.image.load(os.path.join(PIC, 'player_1.png'))
    player2_image = pg.image.load(os.path.join(PIC, 'player_2.png'))

    tank_icon = pg.transform.scale(player_image, (30, 30))
    tank_icon2 = pg.transform.scale(player2_image, (30, 30))

    tile_width = tile_height = 50

    # Высота панели (отступ сверху)
    height_panel = 40

    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()
    bonuses_group = pg.sprite.Group()

    number_level = 1

    level_map = load_level(number_level)

    player, player2, level_x, level_y = generate_level(level_map)
    bonus = generate_bonus()

    battle_sound = pg.mixer.Sound(os.path.join(SOUND, "tank_duel_music.ogg"))
    battle_sound.set_volume(0.2)
    battle_sound.play(-1)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_player(player2, 'up')
                elif event.key == pg.K_DOWN:
                    move_player(player2, 'down')
                elif event.key == pg.K_LEFT:
                    move_player(player2, 'left')
                elif event.key == pg.K_RIGHT:
                    move_player(player2, 'right')
                elif event.key == pg.K_w:
                    move_player(player, 'up')
                elif event.key == pg.K_s:
                    move_player(player, 'down')
                elif event.key == pg.K_a:
                    move_player(player, 'left')
                elif event.key == pg.K_d:
                    move_player(player, 'right')
        # Проверка наличия бонуса
        # Вычитать один надо для того, чтобы не проверять тайлы, находящиеся вне игрового окна
        have_a_bonus = False
        for i in range(len(level_map) - 1):
            if "b" in level_map[i]:
                have_a_bonus = True
                break
        if not have_a_bonus:
            bonus = generate_bonus()
        screen.fill(pg.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        bonuses_group.draw(screen)
        panel(screen, 0, 0, player.lives, player.score, tank_icon)
        panel(screen, 0, HEIGHT - height_panel, player2.lives, player2.score, tank_icon2)
        pg.display.flip()
        clock.tick(FPS)
    terminate()
