import pygame as pg
from define import *
import math
import random

class Score:
    def __init__(self):
        # Khởi tạo điểm số cho hai người chơi
        self.left_score = 0
        self.right_score = 0
        
        # Khởi tạo các hiệu ứng đồ họa
        self.init_graphics()
        
        # Biến cho hiệu ứng động
        self.animation_counter = 0
        self.score_animations = {"left": 0, "right": 0}  # Hiệu ứng khi ghi điểm
        self.particles = []  # Hạt cho hiệu ứng ghi điểm
        
    def init_graphics(self):
        """Khởi tạo các tài nguyên đồ họa cho điểm số"""
        # Font đẹp cho điểm số
        try:
            self.font = pg.font.Font("PingPong/fonts/digital-7.ttf", 64)  # Font kiểu digital
            self.small_font = pg.font.Font("PingPong/fonts/digital-7.ttf", 20)
        except:
            # Fallback nếu không có font
            self.font = pg.font.Font(None, 72)
            self.small_font = pg.font.Font(None, 24)
        
        # Màu sắc 
        self.left_color = (0, 191, 255)  # Xanh lam cho người chơi trái
        self.right_color = (255, 105, 180)  # Hồng cho người chơi phải
        
        # Tạo glow surface cho các số
        self.create_glow_surfaces()
        
    def create_glow_surfaces(self):
        """Tạo các hiệu ứng phát sáng cho điểm số"""
        # Tạo các glow surface với các kích cỡ khác nhau
        self.glow_surfaces = {}
        for i in range(10):  # Cho các số từ 0-9
            digit_str = str(i)
            
            # Glow cho người chơi bên trái (xanh)
            blue_glow = self.create_digit_glow(digit_str, self.left_color)
            self.glow_surfaces[f"left_{i}"] = blue_glow
            
            # Glow cho người chơi bên phải (hồng)
            pink_glow = self.create_digit_glow(digit_str, self.right_color)
            self.glow_surfaces[f"right_{i}"] = pink_glow
    
    def create_digit_glow(self, digit, base_color):
        """Tạo hiệu ứng glow cho một chữ số"""
        # Render chữ số với font lớn
        digit_text = self.font.render(digit, True, (255, 255, 255))
        text_width, text_height = digit_text.get_size()
        
        # Tạo surface lớn hơn để chứa glow
        glow_size = 20
        glow_surface = pg.Surface((text_width + glow_size*2, text_height + glow_size*2), pg.SRCALPHA)
        
        # Tạo hiệu ứng glow
        for i in range(glow_size, 0, -2):
            alpha = 20 if i > glow_size//2 else 10
            r, g, b = base_color
            glow_color = (r, g, b, alpha)
            
            # Vẽ số với độ mờ và kích thước giảm dần
            temp_text = self.font.render(digit, True, glow_color)
            temp_rect = temp_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
            glow_surface.blit(temp_text, temp_rect)
        
        # Vẽ chữ số chính lên trên cùng
        text_rect = digit_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
        glow_surface.blit(digit_text, text_rect)
        
        return glow_surface
    
    def update(self, result):
        """Cập nhật điểm số và kích hoạt hiệu ứng animation"""
        old_left = self.left_score
        old_right = self.right_score
        
        if result == 1:
            self.right_score += 1  # Người bên phải ghi điểm
            if old_right != self.right_score:  # Nếu điểm thay đổi
                self.score_animations["right"] = 30  # Kích hoạt animation trong 30 frames
                self.generate_score_particles("right")
        elif result == -1:
            self.left_score += 1  # Người bên trái ghi điểm
            if old_left != self.left_score:  # Nếu điểm thay đổi
                self.score_animations["left"] = 30  # Kích hoạt animation trong 30 frames
                self.generate_score_particles("left")
    
    def generate_score_particles(self, side):
        """Tạo hiệu ứng hạt khi ghi điểm"""
        if side == "left":
            pos_x = WINDOW_WIDTH // 4
            color_base = self.left_color
        else:
            pos_x = WINDOW_WIDTH * 3 // 4
            color_base = self.right_color
        
        pos_y = 50  # Vị trí y của điểm số
        
        # Tạo 30 hạt cho hiệu ứng bắn pháo hoa
        for _ in range(30):
            # Vận tốc ngẫu nhiên theo hướng bắn ra
            angle = math.radians(random.randint(0, 360))
            speed = random.uniform(1, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            # Màu sắc với một chút biến đổi
            r, g, b = color_base
            r = max(0, min(255, r + random.randint(-20, 20)))
            g = max(0, min(255, g + random.randint(-20, 20)))
            b = max(0, min(255, b + random.randint(-20, 20)))
            color = (r, g, b)

            
            # Kích thước và tuổi thọ
            size = random.uniform(2, 5)
            life = random.randint(20, 50)
            
            # Thêm hạt vào danh sách
            self.particles.append([pos_x, pos_y, dx, dy, size, color, life])
    
    def update_animations(self):
        """Cập nhật trạng thái của các hiệu ứng"""
        # Tăng bộ đếm animation
        self.animation_counter += 0.1
        
        # Giảm thời gian hiệu ứng score nếu đang active
        for side in ["left", "right"]:
            if self.score_animations[side] > 0:
                self.score_animations[side] -= 1
        
        # Cập nhật các hạt
        updated_particles = []
        for particle in self.particles:
            x, y, dx, dy, size, color, life = particle
            
            # Di chuyển hạt
            x += dx
            y += dy
            
            # Giảm kích thước và tuổi thọ
            size -= 0.05
            life -= 1
            
            # Giữ lại hạt nếu còn tồn tại
            if life > 0 and size > 0:
                updated_particles.append([x, y, dx, dy, size, color, life])
        
        self.particles = updated_particles
    
    def display_score(self, surface):
        """Hiển thị điểm số lên màn hình với hiệu ứng đẹp mắt"""
        # Cập nhật các hiệu ứng động
        self.update_animations()
        
        # Vẽ đường phân cách giữa hai bên
        pg.draw.line(surface, (100, 100, 100), 
                    (WINDOW_WIDTH//2, 0), 
                    (WINDOW_WIDTH//2, WINDOW_HEIGHT), 
                    2)
        
        # Hiển thị điểm số bên trái
        self.draw_player_score(surface, "left", self.left_score, WINDOW_WIDTH // 4, 50)
        
        # Hiển thị điểm số bên phải
        self.draw_player_score(surface, "right", self.right_score, WINDOW_WIDTH * 3 // 4, 50)
        
        # Vẽ các hiệu ứng hạt
        for particle in self.particles:
            x, y, dx, dy, size, color, life = particle
            pg.draw.circle(surface, color, (int(x), int(y)), int(size))
        
        # Hiển thị nhãn người chơi
        left_label = self.small_font.render("PLAYER 1", True, self.left_color)
        right_label = self.small_font.render("PLAYER 2", True, self.right_color)
        
        surface.blit(left_label, (WINDOW_WIDTH // 4 - left_label.get_width() // 2, 20))
        surface.blit(right_label, (WINDOW_WIDTH * 3 // 4 - right_label.get_width() // 2, 20))
    
    def draw_player_score(self, surface, side, score, x, y):
        """Vẽ điểm số của một người chơi với hiệu ứng"""
        # Chuyển điểm số thành chuỗi
        score_str = str(score)
        
        # Tính toán chiều rộng tổng để căn giữa
        total_width = 0
        for digit in score_str:
            glow_key = f"{side}_{digit}"
            if glow_key in self.glow_surfaces:
                total_width += self.glow_surfaces[glow_key].get_width()
        
        # Vị trí bắt đầu để căn giữa
        current_x = x - total_width // 2
        
        # Đang có hiệu ứng ghi điểm?
        has_animation = self.score_animations[side] > 0
        
        # Vẽ từng chữ số
        for digit in score_str:
            glow_key = f"{side}_{digit}"
            if glow_key in self.glow_surfaces:
                digit_surface = self.glow_surfaces[glow_key]
                
                # Áp dụng hiệu ứng đặc biệt nếu đang có animation
                if has_animation:
                    # Tính toán hiệu ứng scale theo thời gian
                    progress = self.score_animations[side] / 30.0  # 0.0 -> 1.0
                    scale = 1.0 + 0.5 * math.sin(progress * math.pi)
                    
                    # Scale surface
                    scaled_width = int(digit_surface.get_width() * scale)
                    scaled_height = int(digit_surface.get_height() * scale)
                    scaled_surface = pg.transform.scale(digit_surface, (scaled_width, scaled_height))
                    
                    # Tính toán vị trí để giữ điểm số căn giữa ngay cả khi scale
                    scaled_x = current_x - (scaled_width - digit_surface.get_width()) // 2
                    scaled_y = y - (scaled_height - digit_surface.get_height()) // 2
                    
                    # Vẽ lên màn hình
                    surface.blit(scaled_surface, (scaled_x, scaled_y))
                else:
                    # Vẽ bình thường
                    surface.blit(digit_surface, (current_x, y))
                
                # Di chuyển vị trí x cho chữ số tiếp theo
                current_x += digit_surface.get_width()