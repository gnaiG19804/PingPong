import pygame as pg

class Leaderboard:
    def __init__(self, window, width=600, height=500):
        self.window = window
        self.width = width
        self.height = height
        
        # Màu sắc
        self.bg_color = (20, 24, 35)  # Nền tối
        self.title_color = (255, 215, 0)  # Vàng cho tiêu đề
        self.text_color = (240, 240, 240)  # Màu chữ chính
        self.highlight_color = (65, 105, 225)  # Royal Blue
        self.gold_color = (255, 215, 0)  # Vàng cho top 1
        self.silver_color = (192, 192, 192)  # Bạc cho top 2
        self.bronze_color = (205, 127, 50)  # Đồng cho top 3
        self.panel_color = (30, 35, 45)  # Màu panel nền
        self.border_color = (100, 100, 120)  # Màu viền
        
        # Font chữ
        self.title_font = pg.font.SysFont("arialblack", 48)
        self.header_font = pg.font.SysFont("arial", 28)
        self.rank_font = pg.font.SysFont("arialblack", 24)
        self.text_font = pg.font.SysFont("arial", 22)
        
        # Dữ liệu mẫu mặc định
        self.scores = [
            {"name": "Ronaldo", "score": 730, "date": "2023-12-01"},
            {"name": "Messi", "score": 730, "date": "2023-12-02"},
            {"name": "Bủ nô", "score": 100, "date": "2023-12-03"},
            {"name": "Player4", "score": 65, "date": "2023-12-04"},
            {"name": "Player5", "score": 59, "date": "2023-12-05"},
            {"name": "Player6", "score": 52, "date": "2023-12-06"},
            {"name": "Player7", "score": 48, "date": "2023-12-07"},
            {"name": "Player8", "score": 42, "date": "2023-12-08"}
        ]
    
    def draw_medal(self, x, y, rank):
        """Vẽ huy chương cho top 3"""
        radius = 15
        
        if rank == 1:  # Vàng
            color = self.gold_color
            text = "1"
        elif rank == 2:  # Bạc
            color = self.silver_color
            text = "2"
        elif rank == 3:  # Đồng
            color = self.bronze_color
            text = "3"
        
        # Vẽ huy chương
        pg.draw.circle(self.window, color, (x, y), radius)
        pg.draw.circle(self.window, (50, 50, 50), (x, y), radius, 2)
        
        # Vẽ số thứ tự trong huy chương
        rank_text = self.text_font.render(text, True, (50, 50, 50))
        text_rect = rank_text.get_rect(center=(x, y))
        self.window.blit(rank_text, text_rect)
    
    def draw_row_background(self, y, height, rank):
        """Vẽ nền cho mỗi hàng trong bảng"""
        # Lấy kích thước cửa sổ và tính toán vị trí để căn giữa bảng
        window_width, window_height = self.window.get_size()
        x = (window_width - self.width) // 2
        
        # Tính toán kích thước và vị trí của hàng
        row_width = self.width - 40  # Chiều rộng hàng
        row_x = x + 20  # Vị trí x của hàng (20px từ lề trái của bảng)
        
        rect = pg.Rect(row_x, y, row_width, height)
        
        # Màu nền khác nhau cho top 3
        if rank == 0:
            color = self.highlight_color  # Màu cho header
            pg.draw.rect(self.window, color, rect, border_radius=8)
        elif rank == 1:
            # Màu vàng cho top 1
            base_color = (80, 70, 20)
            pg.draw.rect(self.window, base_color, rect, border_radius=8)
            # Thêm viền sáng hơn
            pg.draw.rect(self.window, self.gold_color, rect, 2, border_radius=8)
        elif rank == 2:
            # Màu bạc cho top 2
            base_color = (70, 70, 75)
            pg.draw.rect(self.window, base_color, rect, border_radius=8)
            # Thêm viền sáng hơn
            pg.draw.rect(self.window, self.silver_color, rect, 2, border_radius=8)
        elif rank == 3:
            # Màu đồng cho top 3
            base_color = (75, 60, 45)
            pg.draw.rect(self.window, base_color, rect, border_radius=8)
            # Thêm viền sáng hơn
            pg.draw.rect(self.window, self.bronze_color, rect, 2, border_radius=8)
        else:
            # Hàng chẵn và lẻ có màu khác nhau
            color = (35, 40, 50) if rank % 2 == 0 else (45, 50, 60)
            pg.draw.rect(self.window, color, rect, border_radius=5)
    def display(self):
        """Hiển thị bảng xếp hạng với khung bao quanh thông số người chơi"""
        # Lấy kích thước cửa sổ
        window_width, window_height = self.window.get_size()
        
        # Xác định vị trí để căn giữa bảng
        x = (window_width - self.width) // 2
        y = (window_height - self.height) // 2
        
        # Vẽ panel nền
        panel_rect = pg.Rect(x, y, self.width, self.height)
        pg.draw.rect(self.window, self.panel_color, panel_rect, border_radius=15)
        pg.draw.rect(self.window, self.border_color, panel_rect, 2, border_radius=15)
        
        # Hiệu ứng ánh sáng ở trên cùng
        gradient_height = 50
        for i in range(gradient_height):
            alpha = 100 - i * 2
            if alpha < 0: alpha = 0
            highlight = pg.Surface((self.width - 20, 1), pg.SRCALPHA)
            highlight.fill((255, 255, 255, alpha))
            self.window.blit(highlight, (x + 10, y + 10 + i))
        
        # Tiêu đề
        title = self.title_font.render("RANK", True, self.title_color)
        title_rect = title.get_rect(center=(x + self.width // 2, y + 50))
        self.window.blit(title, title_rect)
        
        # Vẽ đường kẻ dưới tiêu đề
        pg.draw.line(self.window, self.border_color, 
                (x + 50, y + 80), (x + self.width - 50, y + 80), 3)
        
        # Vẽ header của bảng
        header_y = y + 100
        header_height = 40
        self.draw_row_background(header_y, header_height, 0)
        
        # Text header
        rank_header = self.header_font.render("TOP", True, self.text_color)
        name_header = self.header_font.render("NAME", True, self.text_color)
        score_header = self.header_font.render("SCORE", True, self.text_color)
        
        # Căn giữa các cột header
        self.window.blit(rank_header, (x + self.width // 6 - rank_header.get_width() // 2, header_y + 5))
        self.window.blit(name_header, (x + self.width // 2 - name_header.get_width() // 2, header_y + 5))
        self.window.blit(score_header, (x + 5 * self.width // 6 - score_header.get_width() // 2, header_y + 5))
        
        # Vẽ từng hàng dữ liệu
        row_height = 50
        start_y = header_y + header_height + 10
        
        for i, score in enumerate(self.scores):
            row_y = start_y + i * (row_height + 5)
            
            # Bỏ qua nếu hàng vượt quá chiều cao của panel
            if row_y + row_height > y + self.height - 20:
                break
                
            # Vẽ nền cho hàng và căn giữa
            self.draw_row_background(row_y, row_height, i + 1)
            
            # Text thông tin (không hiển thị rank cho top 3)
            name_text = self.text_font.render(score['name'], True, self.text_color)
            score_text = self.text_font.render(f"{score['score']:,}", True, self.text_color)
            
            # Căn giữa các cột
            self.window.blit(name_text, (x + self.width // 2 - name_text.get_width() // 2, row_y + row_height // 2 - name_text.get_height() // 2))
            self.window.blit(score_text, (x + 5 * self.width // 6 - score_text.get_width() // 2, row_y + row_height // 2 - score_text.get_height() // 2))
            
            # Vẽ huy chương cho top 3 và căn giữa
            if i < 3:
                medal_x = x + self.width // 6 - 20  # Điều chỉnh vị trí theo ý muốn
                self.draw_medal(medal_x, row_y + row_height // 2, i + 1)
            
            # Vẽ khung bao quanh thông số player, căn chỉnh đúng vị trí
            player_rect = pg.Rect(x + 10, row_y, self.width - 40, row_height)  # giảm bớt chiều rộng của khung
            pg.draw.rect(self.window, self.border_color, player_rect, 2, border_radius=5)
