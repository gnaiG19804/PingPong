import pygame as pg

# Khởi tạo Pygame
pg.init()

# Tạo cửa sổ hiển thị
screen = pg.display.set_mode((800, 600))

# Tải ảnh paddle
image = pg.image.load("PingPong/images/paddle.png").convert_alpha()

# Kiểm tra kích thước gốc của ảnh
print(image.get_size())  # In ra kích thước của ảnh paddle

# Thay đổi kích thước ảnh theo yêu cầu của bạn (ví dụ PADDING_WIDTH và PADDING_HEIGHT)
PADDING_WIDTH = 20
PADDING_HEIGHT = 100

# Điều chỉnh kích thước ảnh paddle cho phù hợp
image = pg.transform.scale(image, (PADDING_WIDTH, PADDING_HEIGHT))

# In ra kích thước mới của ảnh paddle
print(image.get_size())  # Kích thước sau khi scale

# Đóng Pygame khi không còn cần thiết
pg.quit()
