import pygame as pg
from define import *

class Player:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color

    def show(self, surface):
        # Vẽ hiệu ứng ánh sáng (Glow)
        glow_color = (255, 255, 255)  # Màu ánh sáng xung quanh
        pg.draw.rect(surface, glow_color, (self.x - 5, self.y - 5, PADDING_WIDTH + 10, PADDING_HEIGHT + 10))  # Vẽ bóng sáng ngoài
        pg.draw.rect(surface, self.color, (self.x, self.y, PADDING_WIDTH, PADDING_HEIGHT))  # Vẽ vợt chính

    def move_up(self):
        self.y -= PADDING_Y
        if self.y < 0:
            self.y = 0

    def move_down(self):
        if self.y + PADDING_HEIGHT <= WINDOW_HEIGHT - PADDING_Y:
            self.y += PADDING_Y

    def getRect(self):
        return pg.Rect(self.x, self.y, PADDING_WIDTH, PADDING_HEIGHT)
