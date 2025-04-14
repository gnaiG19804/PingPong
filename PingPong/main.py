import pygame as pg
from define import *
from modePvP import *
from modePvE import * 
from modeEvE import *  # Thêm import modeEvE
from menu import Menu  # Thêm import menu

pg.init()
WINDOW_GAME = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("PING PONG")

clock = pg.time.Clock()

while True:
    # Hiển thị menu chọn chế độ
    menu = Menu(WINDOW_GAME)
    mode = menu.display()  # Nhận chế độ chơi từ menu

    # Nếu người chơi bấm Quit trong menu
    if mode is None:
        break

    # Khởi tạo chế độ chơi tương ứng
    if mode == "PVP":
        game = modePvP(WINDOW_GAME)
    elif mode == "PvE":
        game = modePvE(WINDOW_GAME)
    elif mode == "AIvsAI":
        game = modeEvE(WINDOW_GAME)
    else:
        break

    game.setup()

    # Vòng lặp chính của mỗi ván game
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        game.key_event()
        game.update()
        pg.display.update()
        clock.tick(60)

        # Kiểm tra nếu có người thắng dựa vào chế độ chơi
        if mode == "PVP":
            # Chế độ PVP: thắng khi có 5 điểm
            if game.score.left_score >= 5 or game.score.right_score >= 5:
                play_again = game.game_over()
                if play_again:
                    game.reset_game()
                else:
                    run = False  # Thoát khỏi vòng chơi hiện tại, quay lại menu
        elif mode == "PvE":
            # Chế độ PvE: thắng nếu AI ghi 1 điểm
            if game.score.left_score >= 1 or game.score.right_score >= 1:
                play_again = game.game_over()
                if play_again:
                    game.reset_game()
                else:
                    run = False  # Thoát khỏi vòng chơi hiện tại, quay lại menu
