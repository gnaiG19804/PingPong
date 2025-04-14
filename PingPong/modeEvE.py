import pygame as pg
import random
from gameMode import gameMode
from define import *
from AI import AI

class modeEvE(gameMode):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.background = pg.image.load("PingPong/images/background.png")
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Khởi tạo 2 AI riêng biệt
        self.ai_left = AI(RED, 0, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.ai_right = AI(GREEN, WINDOW_WIDTH - PADDING_WIDTH, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)

        self.playerLeft = self.ai_left
        self.playerRight = self.ai_right

    def setup(self):
        """Khởi tạo lại bóng sau mỗi lần ghi điểm"""
        a = random.randint(0, 1)
        if a == 0:
            self.ball.reset("left")
        else:
            self.ball.reset("right")

    def update(self):
        """Cập nhật trò chơi mỗi vòng"""
        result = self.ball.update()  # Cập nhật vị trí bóng
        self.window.blit(self.background, (0, 0))  # Vẽ nền

        # Vẽ các đối tượng
        self.playerLeft.show(self.window)
        self.playerRight.show(self.window)
        self.ball.display(self.window)

        # Nếu ghi điểm, reset bóng
        if result != 0:
            self.ball.reset("left" if result == 1 else "right")

        # Kiểm tra va chạm
        self.check()

        # Chỉ gọi auto_move nếu bóng đang đi về phía AI đó
        if self.ball.xFac < 0:  # Bóng đang đi về phía AI bên trái
            self.ai_left.auto_move(self.ball)
        if self.ball.xFac > 0:  # Bóng đang đi về phía AI bên phải
            self.ai_right.auto_move(self.ball)

        # Cập nhật màn hình
        pg.display.update()

    def check(self):
        if self.ball.getRect().colliderect(self.playerLeft.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerLeft.x + PADDING_WIDTH + self.ball.radius

        if self.ball.getRect().colliderect(self.playerRight.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerRight.x - self.ball.radius

    def ai_move(self):
        """Di chuyển AI theo bóng"""
        # Chỉ di chuyển AI nếu bóng đang đi về phía nó
        if self.ball.xFac < 0:  # Bóng đang đi về phía AI bên trái
            self.ai_left.auto_move(self.ball)
        elif self.ball.xFac > 0:  # Bóng đang đi về phía AI bên phải
            self.ai_right.auto_move(self.ball)
