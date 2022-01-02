import pygame as pg
# import numpy as np
# import os
import sys
from pygame import time
from params import *


def generate_level(level):
    pass


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    intro_text = ["Tank Duel", "", "",
                  "Нажмите любую клавишу", ""
                  "для начала игры"]  # TODO: заголовок
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


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Tank Duel")
    screen = pg.display.set_mode(SIZE)
    group_sprites = pg.sprite.Group()
    clock = time.Clock()
    tile_images = {

    }
    player_image = pg.image.load(os.path.join(PIC, ''))  # TODO: Поставить игрока

    tiles_group = pg.sprite.Group()


    start_screen()

    # player, level_x, level_y = generate_level(level_map)

    fps = 60
    running = True
    # while running:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             running = False
    #         elif event.type == pg.KEYDOWN:
    #             if event.key == pg.K_UP:
    #                 move_player(player, 'up')
    #             elif event.key == pg.K_DOWN:
    #                 move_player(player, 'down')
    #             elif event.key == pg.K_LEFT:
    #                 move_player(player, 'left')
    #             elif event.key == pg.K_RIGHT:
    #                 move_player(player, 'right')
    #     screen.fill(pg.Color('black'))
    #     tiles_group.draw(screen)
    #     player_group.draw(screen)
    #     pg.display.flip()
    #     clock.tick(fps)
    # terminate()
