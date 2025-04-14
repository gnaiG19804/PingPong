import pygame as pg
from define import *
from player import Player
from score import Score
from ball import Ball
import random


class gameMode:
    def __init__(self, window):
        self.window = window
        self.playerLeft = Player(RED, 0, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.playerRight = Player(GREEN, WINDOW_WIDTH - PADDING_WIDTH, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.score = Score()
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 7, 3, WHITE)
        self.last_winner = None  # Biến để lưu người thắng trong lần trước

    def setup(self):
        """Khởi tạo bóng với hướng ngẫu nhiên."""
        a = random.randint(0, 1)
        if a == 0:
            self.ball.reset("left")
        else:
            self.ball.reset("right")

    def key_event(self):
        """Phương thức để xử lý sự kiện bàn phím, sẽ được định nghĩa lại trong các chế độ game cụ thể."""
        pass

    def update(self):
        result = self.ball.update()  # Gọi update một lần duy nhất
        self.score.update(result)

        # Vẽ nền (background) lên màn hình trước khi vẽ các đối tượng khác
        self.window.blit(self.background, (0, 0))  # Vẽ ảnh nền tại vị trí (0,0)

        # Hiển thị vật thể trên màn hình
        self.playerLeft.show(self.window)
        self.playerRight.show(self.window)
        self.ball.display(self.window)

        # Kiểm tra nếu bóng ra khỏi bàn
        if result != 0:
            self.ball.reset("left" if result == 1 else "right")

        # Kiểm tra va chạm với vợt
        self.check()

        self.display_score()
        pg.display.update()

    def check(self):
        """Kiểm tra va chạm giữa bóng và các vợt"""
        if self.ball.getRect().colliderect(self.playerLeft.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerLeft.x + PADDING_WIDTH + self.ball.radius

        if self.ball.getRect().colliderect(self.playerRight.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerRight.x - self.ball.radius


    def display_score(self):
        """Hiển thị điểm số lên màn hình."""
        self.score.display_score(self.window)

    def reset_game(self):
        self.score.left_score = 0
        self.score.right_score = 0
        self.ball.reset("left" if self.last_winner == -1 else "right")
        self.playerLeft.y = self.playerRight.y = (WINDOW_HEIGHT - PADDING_HEIGHT) // 2


    def game_over(self):
        pass
