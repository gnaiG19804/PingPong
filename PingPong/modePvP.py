# modePvP.py
import pygame as pg
from gameMode import gameMode
import random
from define import *

class modePvP(gameMode):
    def __init__(self, window):
        super().__init__(window)
        self.window = window  # Sửa lại đúng tên biến là self.window
        self.background = pg.image.load("PingPong/images/background.png")  # Tải ảnh nền
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


    def game_over(self):
        font = pg.font.Font(None, 64)
        winner = "Player left Wins!" if self.score.left_score >= 5 else "Player right Wins!"
        self.last_winner = -1 if self.score.left_score >= 5 else 1

        small_font = pg.font.Font(None, 36)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        return True
                    elif exit_rect.collidepoint(event.pos):
                        return False

            text_surface = font.render(winner, True, (255, 105, 180))  # Màu hồng vũ trụ đẹp
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.window.blit(text_surface, text_rect)

            play_again_rect = pg.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2, 240, 50)
            exit_rect = pg.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 70, 240, 50)

            pg.draw.rect(self.window, (50, 200, 120), play_again_rect, border_radius=10)
            pg.draw.rect(self.window, (200, 50, 50), exit_rect, border_radius=10)

            play_text = small_font.render("Play Again", True, (255, 255, 255))
            exit_text = small_font.render("Exit to Menu", True, (255, 255, 255))

            self.window.blit(play_text, play_text.get_rect(center=play_again_rect.center))
            self.window.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

            pg.display.flip()
