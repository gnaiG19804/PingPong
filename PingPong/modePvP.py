# modePvP.py
import pygame as pg
from gameMode import gameMode
import random
from define import *

class modePvP(gameMode):
    def __init__(self, window):
        super().__init__(window)
        self.window = window  # Sửa lại đúng tên biến là self.window
        self.background = pg.image.load("PingPong/images/background.jpg")  # Tải ảnh nền
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def setup(self):
        a = random.randint(0, 1)
        if a == 0:
            self.ball.reset("left")
        else:
            self.ball.reset("right")
  
    def key_event(self):
        keys = pg.key.get_pressed()  # Lấy trạng thái của tất cả phím

        if keys[pg.K_UP]:  # Di chuyển vợt phải lên
            self.playerRight.move_up()
        if keys[pg.K_DOWN]:  # Di chuyển vợt phải xuống
            self.playerRight.move_down()
        if keys[pg.K_w]:  # Di chuyển vợt trái lên
            self.playerLeft.move_up()
        if keys[pg.K_s]:  # Di chuyển vợt trái xuống
            self.playerLeft.move_down()



