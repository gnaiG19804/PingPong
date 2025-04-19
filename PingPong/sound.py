import pygame as pg
from setting import sound_manager 
from define import *

class SettingsScreen:
    def __init__(self, window, sound_manager):
        self.background = pg.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window = window
        self.font = pg.font.Font(None, 40)
        self.button_width = 300
        self.button_height = 50
        self.button_color = RED
        self.volume = sound_manager.volume  # Dùng âm lượng từ SoundManager
        self.sound_manager = sound_manager

    def draw_text(self, text, x, y, color=WHITE):
        """ Hiển thị chữ lên màn hình """
        label = self.font.render(text, True, color)
        self.window.blit(label, (x, y))

    def draw_button(self, text, x, y):
        """ Vẽ nút và chữ trên nút """
        pg.draw.rect(self.window, self.button_color, (x, y, self.button_width, self.button_height))
        self.draw_text(text, x + (self.button_width - self.font.size(text)[0]) // 2, y + (self.button_height - self.font.get_height()) // 2)  # Căn giữa chữ

    def draw_slider(self, x, y, width, height, value):
        """ Vẽ thanh trượt điều chỉnh âm lượng """
        pg.draw.rect(self.window, WHITE, (x, y, width, height))  # Nền
        handle_x = x + value * (width - height)
        pg.draw.rect(self.window, YELLOW, (handle_x, y, height, height))  # Nút trượt
        return pg.Rect(handle_x, y, height, height)  # Trả về vị trí nút để kiểm tra va chạm


    def show(self):
        """ Màn hình Settings để điều chỉnh âm lượng và bật/tắt âm thanh """
        run_settings = True
        slider_width = 400
        slider_height = 20
        slider_x = (WINDOW_WIDTH - slider_width) // 2  # Căn giữa
        slider_y = 250
        dragging = False  # Biến để kiểm tra xem có kéo chuột trên thanh trượt không

        while run_settings:
            self.window.blit(self.background, (0, 0))  # Vẽ background lên màn hình

            # Tiêu đề
            title_x = (WINDOW_WIDTH - self.font.size("SETTINGS")[0]) // 2
            self.draw_text("SETTINGS", title_x, 100, YELLOW)

            # Vẽ thanh trượt âm lượng
            self.draw_text("Volume", (WINDOW_WIDTH - self.font.size("Volume")[0]) // 2, 200)
            self.draw_slider(slider_x, slider_y, slider_width, slider_height, self.volume)

            # Vẽ nút bật/tắt âm thanh
            sound_button_text = "Turn Off" if self.sound_manager.sound_enabled else "Turn On"
            self.draw_button(sound_button_text, (WINDOW_WIDTH - self.button_width) // 2, 300)

            # Các nút điều khiển: Back và Confirm
            button_x = (WINDOW_WIDTH - self.button_width) // 2
            self.draw_button("Back", button_x, 400)
            self.draw_button("Confirm", button_x, 470)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # 1 là chuột trái
                    mouse_x, mouse_y = event.pos
                    if button_x <= mouse_x <= button_x + self.button_width and 400 <= mouse_y <= 400 + self.button_height:
                        return "Back"  # Quay lại menu chính
                    elif button_x <= mouse_x <= button_x + self.button_width and 470 <= mouse_y <= 470 + self.button_height:
                        self.sound_manager.set_volume(self.volume)  # Lưu âm lượng
                        return "Confirm"  # Lưu cài đặt và quay lại menu chính
                    elif (WINDOW_WIDTH - self.button_width) // 2 <= mouse_x <= (WINDOW_WIDTH - self.button_width) // 2 + self.button_width and 300 <= mouse_y <= 300 + self.button_height:
                        # Chuyển đổi trạng thái bật/tắt âm thanh
                        self.sound_manager.toggle_sound(not self.sound_manager.sound_enabled)

                if event.type == pg.MOUSEMOTION:
                    # Kiểm tra xem chuột có di chuyển trên thanh trượt không
                    if 200 <= event.pos[0] <= 600 and 250 <= event.pos[1] <= 270:
                        self.volume = (event.pos[0]-250) / 400  # Cập nhật âm lượng
                        self.sound_manager.set_volume(self.volume)  # Cập nhật âm lượng trong SoundManager
