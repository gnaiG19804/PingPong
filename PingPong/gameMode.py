import pygame as pg
from define import *
from player import Player
from score import Score
from ball import Ball
from setting import sound_manager
import random

class gameMode:
    def __init__(self, window):
        self.window = window
        self.playerLeft = Player(RED, 0, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.playerRight = Player(GREEN, WINDOW_WIDTH - PADDING_WIDTH, WINDOW_HEIGHT / 2 - PADDING_HEIGHT / 2)
        self.score = Score()
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 7, 3, WHITE)

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
            sound_manager.play_hit()
            self.ball.hit()
            self.ball.posx = self.playerLeft.x + PADDING_WIDTH + self.ball.radius
            

        if self.ball.getRect().colliderect(self.playerRight.getRect()):
            sound_manager.play_hit()
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

    def reset(self):
        self.score.left_score = 0
        self.score.right_score = 0
        self.playerLeft.y = self.playerRight.y = (WINDOW_HEIGHT - PADDING_HEIGHT) // 2
        self.ball.reset_game()

    def pause_menu(self):
        paused = True
        clock = pg.time.Clock()
        
        # Lấy ảnh màn hình hiện tại để làm nền
        screenshot = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        screenshot.blit(self.window, (0, 0))
        
        # Màu sắc
        BG_COLOR = (20, 24, 35)  # Xanh đậm
        TEXT_COLOR = (240, 240, 240)  # Trắng nhẹ
        BUTTON_IDLE = (65, 105, 225)  # Royal Blue
        BUTTON_HOVER = (100, 149, 237)  # Cornflower Blue
        
        # Fonts
        title_font = pg.font.SysFont("arialblack", 72)
        button_font = pg.font.SysFont("arial", 32)
        
        while paused:
            # Vẽ ảnh chụp màn hình làm nền
            self.window.blit(screenshot, (0, 0))
            
            # Vẽ lớp overlay mờ
            overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Đen trong suốt
            self.window.blit(overlay, (0, 0))
            
            # Vẽ panel menu
            panel_rect = pg.Rect(WINDOW_WIDTH//2 - 200, 70, 400, 380)
            pg.draw.rect(self.window, BG_COLOR, panel_rect, border_radius=15)
            pg.draw.rect(self.window, BUTTON_IDLE, panel_rect, 2, border_radius=15)  # Viền
            
            # Vẽ tiêu đề với hiệu ứng đổ bóng
            title_shadow = title_font.render("PAUSED", True, (0, 0, 0))
            title = title_font.render("PAUSED", True, TEXT_COLOR)
            title_x = WINDOW_WIDTH//2 - title.get_width()//2
            
            self.window.blit(title_shadow, (title_x + 2, 102))
            self.window.blit(title, (title_x, 100))
            
            # Đường chia
            pg.draw.line(self.window, (100, 100, 120), 
                    (WINDOW_WIDTH//2 - 150, 180), 
                    (WINDOW_WIDTH//2 + 150, 180), 3)
            
            # Vẽ các nút và xử lý sự kiện
            mouse_pos = pg.mouse.get_pos()
            
            # Nút Tiếp tục
            continue_rect = pg.Rect(WINDOW_WIDTH//2 - 130, 220, 260, 55)
            continue_hover = continue_rect.collidepoint(mouse_pos)
            continue_color = BUTTON_HOVER if continue_hover else BUTTON_IDLE
            
            pg.draw.rect(self.window, (20, 20, 20), continue_rect.inflate(4, 4), border_radius=10)
            pg.draw.rect(self.window, continue_color, continue_rect, border_radius=10)
            
            continue_text = button_font.render("Resume", True, TEXT_COLOR)
            self.window.blit(continue_text, (continue_rect.centerx - continue_text.get_width()//2, 
                                        continue_rect.centery - continue_text.get_height()//2))
            
            # Icon play
            pg.draw.polygon(self.window, TEXT_COLOR, 
                        [(continue_rect.x + 30, continue_rect.centery - 8),
                        (continue_rect.x + 30, continue_rect.centery + 8),
                        (continue_rect.x + 45, continue_rect.centery)])
            
            # Nút Reset
            reset_rect = pg.Rect(WINDOW_WIDTH//2 - 130, 300, 260, 55)
            reset_hover = reset_rect.collidepoint(mouse_pos)
            reset_color = BUTTON_HOVER if reset_hover else BUTTON_IDLE
            
            pg.draw.rect(self.window, (20, 20, 20), reset_rect.inflate(4, 4), border_radius=10)
            pg.draw.rect(self.window, reset_color, reset_rect, border_radius=10)
            
            reset_text = button_font.render("Reset", True, TEXT_COLOR)
            self.window.blit(reset_text, (reset_rect.centerx - reset_text.get_width()//2, 
                                        reset_rect.centery - reset_text.get_height()//2))
            
            # Icon reset
            pg.draw.circle(self.window, TEXT_COLOR, (reset_rect.x + 35, reset_rect.centery), 8, 2)
            pg.draw.arc(self.window, TEXT_COLOR, (reset_rect.x + 27, reset_rect.centery - 8, 16, 16), 0, 5, 2)
            pg.draw.polygon(self.window, TEXT_COLOR,
                        [(reset_rect.x + 40, reset_rect.centery - 5),
                        (reset_rect.x + 40, reset_rect.centery + 2),
                        (reset_rect.x + 45, reset_rect.centery - 1.5)])
            
            # Nút Menu chính
            menu_rect = pg.Rect(WINDOW_WIDTH//2 - 130, 380, 260, 55)
            menu_hover = menu_rect.collidepoint(mouse_pos)
            menu_color = BUTTON_HOVER if menu_hover else BUTTON_IDLE
            
            pg.draw.rect(self.window, (20, 20, 20), menu_rect.inflate(4, 4), border_radius=10)
            pg.draw.rect(self.window, menu_color, menu_rect, border_radius=10)
            
            menu_text = button_font.render("Menu chính", True, TEXT_COLOR)
            self.window.blit(menu_text, (menu_rect.centerx - menu_text.get_width()//2, 
                                    menu_rect.centery - menu_text.get_height()//2))
            
            # Icon menu
            for i in range(3):
                pg.draw.line(self.window, TEXT_COLOR,
                        (menu_rect.x + 25, menu_rect.centery - 6 + i*6),
                        (menu_rect.x + 45, menu_rect.centery - 6 + i*6), 2)
            
            # Xử lý sự kiện
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return "resume"
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if continue_hover:
                            return "resume"
                        elif reset_hover:
                            return "reset" 
                        elif menu_hover:
                            return "menu"
            
            pg.display.flip()
            clock.tick(60)
            
def draw_button(surface, text, x, y, w, h, color, hover_color, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(surface, hover_color, (x, y, w, h))
        if click[0] == 1:
                return action
    else:
        pg.draw.rect(surface, color, (x, y, w, h))

    font = pg.font.SysFont(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    surface.blit(text_surface, (x + (w - text_surface.get_width())//2, y + (h - text_surface.get_height())//2))
