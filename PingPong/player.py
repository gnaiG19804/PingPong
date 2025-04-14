import pygame as pg
from define import *  # Đảm bảo các hằng số như PADDING_WIDTH, PADDING_HEIGHT, v.v.

class Player:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        

        self.image = pg.image.load("PingPong/images/paddle.png").convert_alpha()

        
        self.image = pg.transform.scale(self.image, (PADDING_WIDTH, PADDING_HEIGHT))


    def show(self, surface):
        """Vẽ paddle với hiệu ứng glow nhẹ và hình ảnh"""
    
        # Tạo surface riêng cho glow (vùng glow nhỏ hơn)
        glow_surface = pg.Surface((PADDING_WIDTH + 8, PADDING_HEIGHT + 8), pg.SRCALPHA)

        # Màu viền sáng (cyan nhạt và trong suốt)
        glow_color = 		(255, 105, 180)

        # Vẽ viền sáng mềm bo góc nhẹ
        pg.draw.rect(glow_surface, glow_color, (0, 0, PADDING_WIDTH + 8, PADDING_HEIGHT + 8), border_radius=12)

        # Blit glow vào phía sau paddle, canh lùi 4px mỗi cạnh
        surface.blit(glow_surface, (self.x - 4, self.y - 4))

        # Vẽ paddle hình ảnh chính
        surface.blit(self.image, (self.x, self.y))


    def move_up(self):
        """Di chuyển paddle lên"""
        self.y -= PADDING_Y
        if self.y < 0:
            self.y = 0

    def move_down(self):
        """Di chuyển paddle xuống"""
        if self.y + PADDING_HEIGHT <= WINDOW_HEIGHT - PADDING_Y:
            self.y += PADDING_Y

    def getRect(self):
        """Lấy vị trí và kích thước của paddle"""
        return pg.Rect(self.x, self.y, PADDING_WIDTH, PADDING_HEIGHT)
