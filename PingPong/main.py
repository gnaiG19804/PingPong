import pygame as pg
from define import *
from modePvP import *
from modePvE import * 
from modeEvE import * 
from menu import Menu
from setting import sound_manager

pg.init()
WINDOW_GAME = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("PING PONG")

clock = pg.time.Clock()
sound_manager.play_music()

while True:
    # Hiển thị menu chọn chế độ
    menu = Menu(WINDOW_GAME)
    mode = menu.display()  # Nhận chuỗi: "PvP", "PvE", "AI vs AI"
    # mode = mode.strip().capitalize() if mode else None
    print("Giá trị nhận từ menu:", repr(mode))


    if mode is None:
        break

    # Tạo game tương ứng
    if mode == "PvP":
        game = modePvP(WINDOW_GAME)
        sound_manager.stop_music()
    elif mode == "PvE":
        game = modePvE(WINDOW_GAME)
        sound_manager.stop_music()
    elif mode == "AI vs AI":
        game = modeEvE(WINDOW_GAME)
        sound_manager.stop_music()
    else:
        print("Chế độ không hợp lệ:", mode)
        break

    game.setup()  # Chỉ gọi 1 lần!

    # Vòng lặp chính của game
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

        # Kiểm tra kết thúc theo chế độ
        if mode == "PvP":
            if game.score.left_score >= 5 or game.score.right_score >= 5:
                sound_manager.play_win()
                play_again = game.game_over()
                run = play_again
                if play_again:
                    game.reset_game()
        elif mode == "PvE":
            if game.score.left_score >= 1 or game.score.right_score >= 1:
                sound_manager.play_lose()
                play_again = game.game_over()
                run = play_again
                if play_again:
                    game.reset_game()
        elif mode == "AI vs AI":
            # VD: Dừng sau 3 điểm mỗi bên để demo, bạn có thể chỉnh theo ý muốn
            if game.score.left_score >= 3 or game.score.right_score >= 3:
                play_again = game.game_over()
                run = play_again
                if play_again:
                    game.reset_game()

sound_manager.stop_music()