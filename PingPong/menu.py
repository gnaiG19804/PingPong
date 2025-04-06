import pygame as pg
from define import *

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pg.font.Font(None, 40)  # Font chữ mặc định
        self.button_width = 300
        self.button_height = 50
        self.button_color = YELLOW

    def draw_text(self, text, x, y, color=WHITE):
        """ Hiển thị chữ lên màn hình """
        label = self.font.render(text, True, color)
        self.window.blit(label, (x, y))

    def draw_button(self, text, x, y):
        """ Vẽ nút và chữ trên nút """
        pg.draw.rect(self.window, self.button_color, (x, y, self.button_width, self.button_height))
        self.draw_text(text, x + 50, y + 15)  # Vẽ chữ lên nút

    def display(self):
        run_menu = True
        while run_menu:
            self.draw_text("CHON CHE DO CHOI", 120, 100, YELLOW)

            self.draw_button("modePvP", 120, 200)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # ✅ Đây là chỗ quan trọng: dùng MOUSEBUTTONDOWN
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # 1 là chuột trái
                    mouse_x, mouse_y = event.pos
                    if 120 <= mouse_x <= 120 + self.button_width and 200 <= mouse_y <= 200 + self.button_height:
                        return "PVP"
