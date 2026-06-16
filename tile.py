import pygame as pg
import random
from config import *
from main import play_note

class Tile(pg.sprite.Sprite):
    # загрузка всех картинок для плиток
    short_tile = pg.image.load("short_tile.png")
    short_tile = pg.transform.scale(short_tile, (SIZE[0] // 4, SIZE[1] // 3.5))
    short_tile_pressed = pg.image.load("short_tile_pressed.png")
    short_tile_pressed = pg.transform.scale(short_tile_pressed, (SIZE[0] // 4, SIZE[1] // 3.5))

    long_tile = pg.image.load("long_tile.png")
    long_tile = pg.transform.scale(long_tile, (SIZE[0] // 4, SIZE[1] // 2.2))
    long_tile_pressed = pg.image.load("long_tile_pressed.png")
    long_tile_pressed = pg.transform.scale(long_tile_pressed, (SIZE[0] // 4, SIZE[1] // 2.2))

    def __init__(self, screen_notes = None, long=False):
        '''
        Класс плитки может создавать их двух разных размеров: короткие и длинные.
        Если нужно создать длинную плитку, параметр long должен иметь значение True. По умолчанию плитки короткие.

        Длинная плитка имеет дополнительную переменную count - это сколько тиков уже прошло до того,
        как она посчитается сыгранной. Пока это время не прошло, длинную плитку нужно зажимать мышкой.
        '''
        super().__init__()

        if long:
            self.long = True
            self.image = Tile.long_tile
            self.count = 0
        else:
            self.long = False
            self.image = Tile.short_tile

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 3) * SIZE[0] // 4  # создаём плитку на случайной дорожке
        self.rect.y = -SIZE[1]

        # если плитка соприкасается с другими плитками, переставить её на свободную дорожку
        while pg.sprite.spritecollide(self, screen_notes, False):
             self.rect.x = random.randint(0, 3) * SIZE[0] // 4

        self.played = False

    def update(self):
        super().update()
        self.rect.y += 1

        # ставим длинные плитки в начальный цвет, чтобы если их перестали нажимать слишком рано,
        # они не застыли в нажатом положении
        if self.long and self.count > 0 and not self.played:
            self.image = Tile.long_tile

        mouse_pos = pg.mouse.get_pos()

        if pg.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_pos):
                self.press()


        if self.rect.y >= SIZE[1]:  # если плитка за пределами окна, она удаляется
            self.kill()

    def press(self):
        # нота плитки проигрывается если
        # 1. она на была проиграна раньше
        # 2. это длинная плитка и она ещё не отыграла ни одного тика
        # 3. это короткая плитка
        if not self.played:
            if self.long and self.count == 0:
                play_note()
            if not self.long:
                play_note()

        if self.long:
            # каждые несколько тиков при нажатии на длинную плитку её цвет меняется
            # когда нужное количество тиков пройдёт, то она навсегда поменяет цвет
            # и будет считаться нажатой

            self.count += 1
            if self.count % 5 == 0 and self.count * 2 < 255:
                self.image = Tile.long_tile_pressed
            else:
                self.image = Tile.long_tile
            if self.count >= 120:
                self.image = Tile.long_tile_pressed
                self.played = True
        else:
            # короткие плитки сразу меняют цвет и считаются сыгранными
            self.image = Tile.short_tile_pressed
            self.played = True