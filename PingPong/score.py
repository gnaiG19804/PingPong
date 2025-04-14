import pygame as pg
from define import *

class Score:
    def __init__(self):
        # Khởi tạo điểm số cho hai người chơi
        self.left_score = 0
        self.right_score = 0

    def update(self, result):
        """Cập nhật điểm số dựa vào kết quả."""
        if result == 1:
            self.right_score += 1  # Người bên phải ghi điểm
        elif result == -1:
            self.left_score += 1  # Người bên trái ghi điểm
    
    def display_score(self, surface):
        """Hiển thị điểm lên màn hình."""
        font = pg.font.Font(None, 36)
        left_text = font.render(str(self.left_score), True, WHITE)
        right_text = font.render(str(self.right_score), True, WHITE)
        
        # Hiển thị điểm trên màn hình
        surface.blit(left_text, (WINDOW_WIDTH // 4, 20))
        surface.blit(right_text, (WINDOW_WIDTH * 3 // 4 - right_text.get_width(), 20))
