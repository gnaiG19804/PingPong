import pygame as pg
from define import *
from sound import SettingsScreen  # Import màn hình settings
from setting import sound_manager

class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pg.font.Font(None, 40)  # Font chữ mặc định
        self.button_width = 300
        self.button_height = 50
        self.button_color = RED
        self.background = pg.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Thay đổi kích thước hình nền cho phù hợp
        self.sound_manager = sound_manager

    def draw_text(self, text, x, y, color=WHITE):
        """ Hiển thị chữ lên màn hình """
        label = self.font.render(text, True, color)
        self.window.blit(label, (x, y))

    def draw_button(self, text, x, y, is_hover=False):
        color = (255, 100, 100) if is_hover else self.button_color
        rect = pg.Rect(x, y, self.button_width, self.button_height)
        pg.draw.rect(self.window, color, rect, border_radius=12)  # Bo góc
        pg.draw.rect(self.window, WHITE, rect, 2, border_radius=12)  # Viền trắng

        text_surf = self.font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.window.blit(text_surf, text_rect)


    def display(self):
        run_menu = True
        while run_menu:
            self.window.blit(self.background, (0, 0))  # Vẽ background lên màn hình

            # Các nút chơi
            button_x = (WINDOW_WIDTH - self.button_width) // 2
            buttons = [
                ("PvP", 200),
                ("PvE", 270),
                ("AI vs AI", 340),
                ("Rankings", 410),
                ("Settings", 480)
            ]

            buttons_rects = []
            for i, (text, y) in enumerate(buttons):
                rect = self.draw_button(text, button_x, y)
                buttons_rects.append(rect)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # 1 là chuột trái
                    mouse_x, mouse_y = event.pos
                    for i, rect in enumerate(buttons_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            if i == 0: return "PvP"
                            elif i == 1: return "PvE"
                            elif i == 2: return "AI vs AI"
                            elif i == 3: return "Rankings"
                            elif i == 4:  # Settings
                                settings_screen = SettingsScreen(self.window, self.sound_manager)
                                result = settings_screen.show()
                                if result in ["Back", "Confirm"]:
                                    continue  # Quay lại menu sau khi điều chỉnh
