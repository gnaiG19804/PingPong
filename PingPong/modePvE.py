import pygame as pg
import random
from gameMode import gameMode
from define import *
from player import Player
from AI import AI

class modePvE(gameMode):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.background = pg.image.load("PingPong/images/background.jpg")
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Thay thế playerRight bằng AI
        self.ai = AI(GREEN, WINDOW_WIDTH - PADDING_WIDTH, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.playerLeft = Player(RED, 0, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)  # Thêm người chơi trái
        self.playerRight = self.ai  # AI thay thế người chơi phải

    def setup(self):
        """Khởi tạo lại bóng sau mỗi lần ghi điểm"""
        a = random.randint(0, 1)
        if a == 0:
            self.ball.reset("left")
        else:
            self.ball.reset("right")

    def key_event(self):
        """Xử lý sự kiện bàn phím cho người chơi trái"""
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.playerLeft.move_up()  # Di chuyển lên
        if keys[pg.K_s]:
            self.playerLeft.move_down()  # Di chuyển xuống

    def update(self):
        """Cập nhật trò chơi mỗi vòng"""
        result = self.ball.update()  # Cập nhật vị trí bóng
        self.window.blit(self.background, (0, 0))  # Vẽ nền

        # Vẽ các đối tượng
        self.playerLeft.show(self.window)
        self.ai.show(self.window)
        self.ball.display(self.window)

        # Nếu ghi điểm, reset bóng
        if result != 0:
            self.ball.reset("left" if result == 1 else "right")

        # Kiểm tra va chạm
        self.check()

        # Di chuyển AI
        self.ai.auto_move(self.ball)  # AI xử lý di chuyển

        # Hiển thị điểm số
        self.display_score()
        pg.display.update()

    def check(self):
        """Kiểm tra va chạm giữa bóng và các vợt"""
        # Kiểm tra va chạm với playerLeft
        if self.ball.getRect().colliderect(self.playerLeft.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerLeft.x + PADDING_WIDTH + self.ball.radius

        # Kiểm tra va chạm với AI (playerRight)
        if self.ball.getRect().colliderect(self.ai.getRect()):
            self.ball.hit()
            self.ball.posx = self.ai.x - self.ball.radius

    def ai_move(self):
        """Di chuyển AI theo bóng"""
        self.ai.auto_move(self.ball)
