import pygame as pg
from define import *
from modePvP import *
from modePvE import * 
from modeEvE import * 
from menu import Menu
from setting import sound_manager
from ranking import Leaderboard


pg.init()
WINDOW_GAME = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("PING PONG")
clock = pg.time.Clock()
sound_manager.play_music()
leaderboard = Leaderboard(WINDOW_GAME)

def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return "pause"
    return None

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
    elif mode == "Rankings":
        running_leaderboard = True
        while running_leaderboard:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # Nếu nhấn ESC quay lại menu
                        running_leaderboard = False
            
            leaderboard.display()  # Hiển thị bảng xếp hạng
            pg.display.update()  # Cập nhật màn hình
            clock.tick(60)  # Giới hạn FPS
        continue  # Quay lại menu khi thoát khỏi bảng xếp hạng
    else:
        print("Chế độ không hợp lệ:", mode)
        break

    game.setup()  # Chỉ gọi 1 lần!

    # Vòng lặp chính của game
    run = True
    while run:
        result = key_event()  # Xử lý phím ESC
        if result == "pause":
            action = game.pause_menu()
            if action == "resume":
                continue
            elif action == "reset":
                game.reset()
                continue
            elif action == "menu":
                break

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
            if game.score.left_score >= 1 or game.score.right_score >= 10000:
                sound_manager.play_lose()
                play_again = game.game_over()
                run = play_again
                if play_again:
                    game.reset_game()

sound_manager.stop_music()