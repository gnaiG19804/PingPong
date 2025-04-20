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
        self.background = pg.image.load("PingPong/images/background.png")
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ai = AI(GREEN, WINDOW_WIDTH - PADDING_WIDTH, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.playerLeft = Player(RED, 0, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.playerRight = self.ai  # dùng chung để dễ gọi lại sau này

    def setup(self):
        a = random.randint(0, 1)
        if a == 0:
            self.ball.reset("left")
        else:
            self.ball.reset("right")

    def key_event(self):
        keys = pg.key.get_pressed()  # Lấy tất cả các phím đã nhấn
        if keys[pg.K_v]:  # Nếu phím 'V' được nhấn
            self.ai.reverse()  # Đảo ngược trạng thái stop của AI
        if keys[pg.K_w]:  # Nếu phím 'W' được nhấn
            self.playerLeft.move_up()  # Di chuyển playerLeft lên
        if keys[pg.K_s]:  # Nếu phím 'S' được nhấn
            self.playerLeft.move_down()  # Di chuyển playerLeft xuống


    def update(self):
        result = self.ball.update()
        self.score.update(result)
        self.window.blit(self.background, (0, 0))

        self.playerLeft.show(self.window)
        self.ai.show(self.window)
        self.ball.display(self.window)

        if result != 0:
            self.ball.reset("left" if result == 1 else "right")
            if(self.ai.stop==True):
                self.ai.reverse()

        self.check()
        self.ai.auto_move(self.ball)
        self.display_score()
        pg.display.update()

    def check(self):
        if self.ball.getRect().colliderect(self.playerLeft.getRect()):
            self.ball.hit()
            self.ball.posx = self.playerLeft.x + PADDING_WIDTH + self.ball.radius

        if self.ball.getRect().colliderect(self.ai.getRect()):
            self.ball.hit()
            self.ball.posx = self.ai.x - self.ball.radius

    def game_over(self):
        font = pg.font.Font(None, 64)
        winner = "You Win!" if self.score.left_score >= 1 else "AI Wins!"
        self.last_winner = -1 if self.score.left_score >= 1 else 1

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

            text_surface = font.render(winner, True, (255, 105, 180))
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
