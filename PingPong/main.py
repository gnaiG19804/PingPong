import pygame as pg
from define import *
from modePvP import *
from menu import Menu  # Thêm import menu

pg.init()
WINDOW_GAME = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("PING PONG")

# Hiển thị menu chọn chế độ
menu = Menu(WINDOW_GAME)
mode = menu.display()  # Nhận chế độ chơi từ menu

if mode == "PVP":
    game = modePvP(WINDOW_GAME)
    game.setup()
elif mode == "PvE":
    # Chế độ này có thể bỏ qua nếu chưa có
    pass
else:
    pg.quit()
    exit()

clock = pg.time.Clock()

# Game loop
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Gọi các phương thức game
    game.key_event()  # Xử lý sự kiện bàn phím
    game.update()  # Cập nhật game (bao gồm cả vẽ lại màn hình)
    game.display_score()  # Hiển thị điểm số

    pg.display.update()  # Cập nhật màn hình hiển thị
    pg.time.delay(15)  # Tạo tốc độ 60 FPS
    clock.tick(60)  # Điều chỉnh tốc độ khung hình

pg.quit()
