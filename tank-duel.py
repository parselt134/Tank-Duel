import pygame as pg
import numpy as np
import sys
from pygame import time
from params import *


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direc, im, sign):
        super().__init__(player_group)
        self.direc = direc
        self.image = pg.transform.rotate(im, -90 * self.direc)
        self.pos = (pos_x, pos_y)
        self.sign = sign
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1])
        self.life = True

    def move(self, x, y, new_direc):
        if self.life:
            self.image = pg.transform.rotate(pg.transform.rotate(self.image, 90 * self.direc), -90 * new_direc)
            self.direc = new_direc
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                   tile_height * self.pos[1])
            level_map[y, x] = self.sign

    def shot(self):
        if self.life:
            if self.direc == 0 and (level_map[self.pos[1] - 1, self.pos[0]] == '.'
                                    or level_map[self.pos[1] - 1, self.pos[0]] == '='):
                Bullet(self.pos[0], self.pos[1] - 1, (0, -1))
            elif self.direc == 1 and (level_map[self.pos[1], self.pos[0] + 1] == '.'
                                      or level_map[self.pos[1], self.pos[0] + 1] == '='):
                Bullet(self.pos[0] + 1, self.pos[1], (1, 0))
            elif self.direc == 2 and (level_map[self.pos[1] + 1, self.pos[0]] == '.'
                                      or level_map[self.pos[1] + 1, self.pos[0]] == '='):
                Bullet(self.pos[0], self.pos[1] + 1, (0, 1))
            elif self.direc == 3 and (level_map[self.pos[1], self.pos[0] - 1] == '.'
                                      or level_map[self.pos[1], self.pos[0] - 1] == '='):
                Bullet(self.pos[0] - 1, self.pos[1], (-1, 0))

    def death(self):
        self.life = False


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, v):
        super().__init__(bullet_group)
        self.v = v
        self.image = bullet_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)

    def update(self):
        if time_bullet >= 0.3:
            if level_map[self.pos[1] + self.v[1], self.pos[0] + self.v[0]] == '@':
                player.death()
                player.kill()
                self.kill()
                level_map[self.pos[1] + self.v[1], self.pos[0] + self.v[0]] = '.'
            elif level_map[self.pos[1] + self.v[1], self.pos[0] + self.v[0]] == '%':
                player2.death()
                player2.kill()
                self.kill()
                level_map[self.pos[1] + self.v[1], self.pos[0] + self.v[0]] = '.'
            elif 10 > self.pos[0] + self.v[0] > -1 and 10 > self.pos[1] + self.v[1] > -1 and\
                    level_map[self.pos[1] + self.v[1], self.pos[0] + self.v[0]] != '#':
                self.pos = (self.pos[0] + self.v[0], self.pos[1] + self.v[1])
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height * self.pos[1])
            else:
                self.kill()
        if level_map[self.pos[1], self.pos[0]] == '@':
            player.death()
            player.kill()
            self.kill()
            level_map[self.pos[1], self.pos[0]] = '.'
        elif level_map[self.pos[1], self.pos[0]] == '%':
            player2.death()
            player2.kill()
            self.kill()
            level_map[self.pos[1], self.pos[0]] = '.'


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
                new_player = Player(x, y, 2, player_image, "@")
            elif level[y][x] == "%":
                Tile("empty", x, y)
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
    screen = pg.display.set_mode(SIZE)
    group_sprites = pg.sprite.Group()
    clock = time.Clock()
    time_bullet = 0
    tile_images = {
        "bricks": pg.image.load(os.path.join(PIC, "bricks.png")),
        "water": pg.image.load(os.path.join(PIC, "water.png")),
        "empty": pg.image.load(os.path.join(PIC, "grass.png"))
    }

    player_image = pg.image.load(os.path.join(PIC, 'player_1.png'))
    player2_image = pg.image.load(os.path.join(PIC, 'player_2.png'))

    bullet_image = pg.image.load(os.path.join(PIC, 'bullet.png'))

    tile_width = tile_height = 50

    player_group = pg.sprite.Group()

    tiles_group = pg.sprite.Group()

    bullet_group = pg.sprite.Group()

    start_screen()

    number_level = 1

    level_map = load_level(number_level)

    player, player2, level_x, level_y = generate_level(level_map)

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

                elif event.key == pg.K_KP1:
                    player2.shot()
                elif event.key == pg.K_e:
                    player.shot()
        screen.fill(pg.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        bullet_group.update()

        if time_bullet >= 0.3:
            time_bullet = 0
        time_bullet += clock.tick() / 1000

        pg.display.flip()
        clock.tick(FPS)
    terminate()
