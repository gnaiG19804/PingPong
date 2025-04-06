import pygame as pg
import random
from define import *  # Đảm bảo các hằng số như WINDOW_WIDTH, WINDOW_HEIGHT, v.v.

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.firstTime = True
        self.angle = 0  # Góc quay ban đầu của bóng

    def display(self, surface):
        """ Hiển thị bóng với hiệu ứng quay """
        # Load hình ảnh bóng
        self.image = pg.image.load("PingPong/images/ball.png")
        
        # Điều chỉnh kích thước của bóng
        self.image = pg.transform.scale(self.image, (self.radius * 4.2, self.radius * 4.2))

        # Xoay bóng theo góc hiện tại
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=(self.posx, self.posy))

        # Vẽ bóng lên màn hình
        surface.blit(self.image, self.rect.topleft)

    def update(self):
        """ Cập nhật vị trí và góc quay của bóng """
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # Cập nhật góc quay
        self.angle += 5  # Thay đổi tốc độ quay (càng lớn càng nhanh)

        # Nếu bóng chạm cạnh trên hoặc dưới -> Đảo hướng Y
        if self.posy <= 0 or self.posy >= WINDOW_HEIGHT:
            self.yFac *= -1

        # Nếu bóng đi ra khỏi màn chơi
        if self.posx <= 0 and self.firstTime:
            self.firstTime = False
            return 1  # Người chơi bên phải ghi điểm
        elif self.posx >= WINDOW_WIDTH and self.firstTime:
            self.firstTime = False
            return -1  # Người chơi bên trái ghi điểm

        return 0  # Nếu chưa ra ngoài thì không tính điểm


    def reset(self, last_winner):
        self.posx = WINDOW_WIDTH // 2
        self.posy = WINDOW_HEIGHT // 2

        # Bóng đi về phía người vừa ghi điểm
        self.xFac = 1 if last_winner == "left" else -1

        # Hướng Y ngẫu nhiên
        self.yFac = random.choice([-1, 1])
        self.firstTime = True
        self.speed = 3

    def hit(self):
        self.xFac *= -1  # Đảo hướng khi chạm vào vợt
        self.speed *= 1.1  # Tăng tốc độ bóng sau mỗi làn chạm

    def getRect(self):
        return pg.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)
