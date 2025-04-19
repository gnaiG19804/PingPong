import os
import pygame as pg

# Kích thước
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (238, 255, 3)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Đường dẫn ảnh
PATH_IMAGES = os.path.dirname(__file__)
PATH_IMAGES = os.path.join(PATH_IMAGES, "images/")


# Tải các hình ảnh
# background = pg.image.load(os.path.join(PATH_IMAGES, "background.jpg"))
# ball_image = pg.image.load(os.path.join(PATH_IMAGES, "ball.jpg"))
menu_image = pg.image.load(os.path.join(PATH_IMAGES, "menu.jpg"))
# Biến
PADDING_WIDTH = 20
PADDING_HEIGHT = 100
PADDING_LINE = 10
PADDING_Y = 10
def set_padding_y(value):
    global PADDING_Y
    PADDING_Y = value

def get_padding_y():
    return PADDING_Y
# Đích
MAX_SCORE = 5

BALL_SIZE = 20
BALL_X = 20
BALL_RADIUS = 10

last_winner = None
