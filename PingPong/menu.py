import pygame as pg
from define import *

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pg.font.Font(None, 40)  # Font chữ mặc định
        self.button_width = 300
        self.button_height = 50
        self.button_color = RED
        self.background = pg.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Thay đổi kích thước hình nền cho phù hợp
    

    def draw_text(self, text, x, y, color=WHITE):
        """ Hiển thị chữ lên màn hình """
        label = self.font.render(text, True, color)
        self.window.blit(label, (x, y))

    def draw_button(self, text, x, y):
        """ Vẽ nút và chữ trên nút """
        pg.draw.rect(self.window, self.button_color, (x, y, self.button_width, self.button_height))
        self.draw_text(text, x + (self.button_width - self.font.size(text)[0]) // 2, y + (self.button_height - self.font.get_height()) // 2)  # Căn giữa chữ

    def display(self):
        run_menu = True
        while run_menu:
            self.window.blit(self.background, (0, 0))  # Vẽ background lên màn hình

            # Tính toán vị trí căn giữa màn hình cho tiêu đề
            title_x = (WINDOW_WIDTH - self.font.size("CHON CHE DO CHOI")[0]) // 2
            self.draw_text("CHON CHE DO CHOI", title_x, 100, YELLOW)

            # Các nút chơi
            button_x = (WINDOW_WIDTH - self.button_width) // 2
            self.draw_button("PvP", button_x, 200)
            self.draw_button("PvE", button_x, 270)
            self.draw_button("AI vs AI", button_x, 340)
            self.draw_button("Rankings", button_x, 410)
            self.draw_button("Settings", button_x, 480)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # 1 là chuột trái
                    mouse_x, mouse_y = event.pos
                    if button_x <= mouse_x <= button_x + self.button_width and 200 <= mouse_y <= 200 + self.button_height:
                        return "PVP"
                    elif button_x <= mouse_x <= button_x + self.button_width and 270 <= mouse_y <= 270 + self.button_height:
                        return "PvE"
                    elif button_x <= mouse_x <= button_x + self.button_width and 340 <= mouse_y <= 340 + self.button_height:
                        return "AIvsAI"
                    elif button_x <= mouse_x <= button_x + self.button_width and 410 <= mouse_y <= 410 + self.button_height:
                        return "Rankings"
                    elif button_x <= mouse_x <= button_x + self.button_width and 480 <= mouse_y <= 480 + self.button_height:
                        return "Settings"
