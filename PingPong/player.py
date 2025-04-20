import pygame as pg
from define import *
import math
import random

class Player:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        
        # Tải hình ảnh paddle cơ bản
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Ghép đường dẫn đến hình ảnh paddle.png
        image_path = os.path.join(base_dir, "images", "paddle.png")

        # Tải hình ảnh paddle
        self.base_image = pg.image.load(image_path).convert_alpha()
        self.base_image = pg.transform.scale(self.base_image, (PADDING_WIDTH, PADDING_HEIGHT))
        
        # Tạo các hiệu ứng bổ sung
        self.create_effects()
        
        # Biến cho hiệu ứng động
        self.animation_counter = 0
        self.last_moved = 0
        self.motion_trail = []  # Lưu vị trí trước đó cho hiệu ứng trail
        self.particle_effects = []  # Cho hiệu ứng hạt
        self.is_moving = False
        
    def create_effects(self):
        """Tạo các surface hiệu ứng cho paddle"""
        # Tạo một bản sao của ảnh gốc để chỉnh sửa
        self.image = self.base_image.copy()
        
        # Tạo hiệu ứng ánh sáng trên paddle
        width, height = self.image.get_size()
        for y in range(height):
            brightness = 1 - (y / height * 0.7)  # Độ sáng giảm dần từ trên xuống dưới
            for x in range(width):
                pixel = self.image.get_at((x, y))
                # Tăng độ sáng cho pixel
                r = min(255, int(pixel[0] * brightness + 40))
                g = min(255, int(pixel[1] * brightness + 40))
                b = min(255, int(pixel[2] * brightness + 40))
                a = pixel[3]
                self.image.set_at((x, y), (r, g, b, a))
        
        # Tạo hiệu ứng phản chiếu
        self.reflection = pg.Surface((PADDING_WIDTH, PADDING_HEIGHT // 3), pg.SRCALPHA)
        reflection_color = (255, 255, 255, 60)  # Trắng trong suốt
        pg.draw.rect(self.reflection, reflection_color, (0, 0, PADDING_WIDTH, PADDING_HEIGHT // 3))
        
        # Tạo các hiệu ứng glow
        self.create_glow_effects()
    
    def create_glow_effects(self):
        """Tạo các hiệu ứng phát sáng khác nhau"""
        # Glow chính
        self.glow_surface = pg.Surface((PADDING_WIDTH + 12, PADDING_HEIGHT + 12), pg.SRCALPHA)
        
        # Tạo gradient cho glow từ trong ra ngoài
        for i in range(6):
            alpha = 120 - i * 20  # Độ trong suốt giảm dần
            size_offset = i * 2
            glow_rect = pg.Rect(size_offset, size_offset, 
                               PADDING_WIDTH + 12 - size_offset*2, 
                               PADDING_HEIGHT + 12 - size_offset*2)
            
            # Màu glow dựa trên màu của người chơi
            if self.color == "blue":
                glow_color = (0, 191, 255, alpha)  # Xanh lam sáng
            else:  # Red player
                glow_color = (255, 105, 180, alpha)  # Hồng sáng
                
            pg.draw.rect(self.glow_surface, glow_color, glow_rect, border_radius=12)
    
    def add_particles(self, direction):
        """Thêm hiệu ứng hạt khi paddle di chuyển"""
        if self.color == "blue":
            particle_color_base = (0, 191, 255)  # Xanh lam
        else:
            particle_color_base = (255, 105, 180)  # Hồng
            
        for _ in range(3):
            # Vị trí ngẫu nhiên dọc theo paddle
            x = self.x + PADDING_WIDTH // 2
            y = self.y + random.randint(0, PADDING_HEIGHT)
            
            # Điều chỉnh vận tốc theo hướng di chuyển
            dx = random.uniform(-0.5, 0.5)
            if direction == "up":
                dy = random.uniform(1, 3)  # Hạt bay xuống khi paddle đi lên
            else:
                dy = random.uniform(-3, -1)  # Hạt bay lên khi paddle đi xuống
                
            # Điều chỉnh màu sắc ngẫu nhiên
            r = min(255, particle_color_base[0] + random.randint(-20, 20))
            g = min(255, particle_color_base[1] + random.randint(-20, 20))
            b = min(255, particle_color_base[2] + random.randint(-20, 20))
            color = (r, g, b)
            
            size = random.uniform(1, 3)
            life = random.randint(5, 15)
            
            self.particle_effects.append([x, y, color, size, life, dx, dy])
    
    def update_effects(self):
        """Cập nhật các hiệu ứng động"""
        self.animation_counter += 0.1
        
        # Cập nhật hiệu ứng hạt
        new_particles = []
        for particle in self.particle_effects:
            x, y, color, size, life, dx, dy = particle
            
            # Cập nhật vị trí và tuổi thọ
            x += dx
            y += dy
            life -= 1
            size -= 0.1
            
            if life > 0 and size > 0:
                new_particles.append([x, y, color, size, life, dx, dy])
                
        self.particle_effects = new_particles
        
        # Cập nhật motion trail
        self.motion_trail = [pos for pos in self.motion_trail if pos[2] > 0]
        for i in range(len(self.motion_trail)):
            self.motion_trail[i] = (self.motion_trail[i][0], self.motion_trail[i][1], self.motion_trail[i][2] - 1)
    
    def show(self, surface):
        """Vẽ paddle với các hiệu ứng nâng cao"""
        self.update_effects()
        
        # Vẽ motion trail nếu paddle đang di chuyển
        if self.is_moving:
            for pos_x, pos_y, alpha in self.motion_trail:
                trail_alpha = min(150, alpha * 10)
                trail_surface = pg.Surface((PADDING_WIDTH, PADDING_HEIGHT), pg.SRCALPHA)
                if self.color == "blue":
                    trail_color = (0, 120, 215, trail_alpha)
                else:
                    trail_color = (215, 60, 120, trail_alpha)
                pg.draw.rect(trail_surface, trail_color, (0, 0, PADDING_WIDTH, PADDING_HEIGHT), border_radius=10)
                surface.blit(trail_surface, (pos_x, pos_y))
        
        # Vẽ các hiệu ứng hạt
        for particle in self.particle_effects:
            x, y, color, size, life, dx, dy = particle
            pg.draw.circle(surface, color, (int(x), int(y)), int(size))
        
        # Vẽ hiệu ứng glow
        glow_x = self.x - 6
        glow_y = self.y - 6
        pulse = (math.sin(self.animation_counter) + 1) * 0.2 + 0.8  # Hiệu ứng nhịp đập (0.8-1.2)
        scaled_glow = pg.transform.scale(self.glow_surface, 
                                       (int((PADDING_WIDTH + 12) * pulse), 
                                        int((PADDING_HEIGHT + 12) * pulse)))
        glow_x -= int(((pulse - 1) * (PADDING_WIDTH + 12)) / 2)
        glow_y -= int(((pulse - 1) * (PADDING_HEIGHT + 12)) / 2)
        surface.blit(scaled_glow, (glow_x, glow_y))
        
        # Vẽ paddle chính
        surface.blit(self.image, (self.x, self.y))
        
        # Vẽ hiệu ứng phản chiếu ánh sáng
        reflection_y = self.y + PADDING_HEIGHT // 8
        surface.blit(self.reflection, (self.x, reflection_y))
        
        # Reset trạng thái di chuyển
        self.is_moving = False
    
    def move_up(self):
        """Di chuyển paddle lên"""
        self.is_moving = True
        old_y = self.y
        self.y -= PADDING_Y
        if self.y < 0:
            self.y = 0
        
        # Thêm vị trí cũ vào trail nếu đã di chuyển
        if old_y != self.y:
            self.motion_trail.append((self.x, old_y, 15))  # 15 là thời gian tồn tại
            self.add_particles("up")
    
    def move_down(self):
        """Di chuyển paddle xuống"""
        self.is_moving = True
        old_y = self.y
        if self.y + PADDING_HEIGHT <= WINDOW_HEIGHT - PADDING_Y:
            self.y += PADDING_Y
        
        # Thêm vị trí cũ vào trail nếu đã di chuyển
        if old_y != self.y:
            self.motion_trail.append((self.x, old_y, 15))
            self.add_particles("down")
    
    def getRect(self):
        """Lấy vị trí và kích thước của paddle"""
        return pg.Rect(self.x, self.y, PADDING_WIDTH, PADDING_HEIGHT)
