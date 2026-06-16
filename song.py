import pygame as pg
from config import f1

class Song:
    songs = []  # здесь будет хранится список всех доступных песен

    def __init__(self, name, notes, duration, rect, interval=0.5):
        self.name = name
        self.notes = notes
        self.duration = duration
        self.color = "red"
        self.rect = pg.Rect(rect)
        self.interval = interval

        self.text = f1.render(self.name, True, pg.Color("white"))
        Song.songs.append(self)
        