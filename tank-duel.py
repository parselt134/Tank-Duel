import pygame as pg
import numpy as np
# import os
import sys
from pygame import time
from params import *


class Player(pg.sprite.Sprite):
    pass


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


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
    new_player, x, y = None, None, None
    row, col = level.shape
    for y in range(row):
        for x in range(col):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("bricks", x, y)
            elif level[y][x] == "=":
                Tile("water", x, y)
            elif level[y][x] == "@" or level[y][x] == "%":
                Tile("empty", x, y)
                level_map[y, x] = "."
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    intro_text = ["Tank Duel", "", "",
                  "Нажмите любую клавишу", ""
                  "для начала игры"]
    fon = pg.image.load(os.path.join(PIC, "start_screen.png"))
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 35)
    text_coords = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coords += 10
        intro_rect.top = text_coords
        intro_rect.x = 10
        text_coords += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        clock.tick(FPS)


def move_player(player, movement):
    pass


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Tank Duel")
    screen = pg.display.set_mode(SIZE)
    group_sprites = pg.sprite.Group()
    clock = time.Clock()
    tile_images = {
        "bricks": pg.image.load(os.path.join(PIC, "bricks.png")),
        "water": pg.image.load(os.path.join(PIC, "water.png")),
        "empty": pg.image.load(os.path.join(PIC, "grass.png"))
    }

    # player_image = pg.image.load(os.path.join(PIC, ''))  # TODO: Поставить игрока

    tile_width = tile_height = 50

    player_group = pg.sprite.Group()

    tiles_group = pg.sprite.Group()

    start_screen()

    number_level = 1

    level_map = load_level(number_level)

    player, level_x, level_y = generate_level(level_map)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_player(player, 'up')
                elif event.key == pg.K_DOWN:
                    move_player(player, 'down')
                elif event.key == pg.K_LEFT:
                    move_player(player, 'left')
                elif event.key == pg.K_RIGHT:
                    move_player(player, 'right')
        screen.fill(pg.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pg.display.flip()
        clock.tick(FPS)
    terminate()
