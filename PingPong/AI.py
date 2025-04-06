from player import Player
from define import *
from ball import Ball

class AI(Player):
    def __init__(self, color, x, y, speed=50):
        super().__init__(color, x, y)
        self.speed = speed  # Tốc độ di chuyển của AI

    def predict_ball_position(self, ball):
        """Tính toán vị trí bóng sẽ chạm vợt AI, bao gồm xử lý bóng bật tường và tốc độ."""
        ball_copy = Ball(ball.posx, ball.posy, ball.radius, ball.speed, ball.color)

        # Mô phỏng bóng di chuyển từng frame, bao gồm xử lý khi bóng bật tường
        while True:
            if (ball_copy.xFac < 0 and ball_copy.posx <= self.x) or (ball_copy.xFac > 0 and ball_copy.posx >= self.x):
                break  # Bóng đã đến vợt AI

            ball_copy.posx += ball_copy.xFac * ball_copy.speed
            ball_copy.posy += ball_copy.yFac * ball_copy.speed

            # Xử lý bóng va chạm tường trên và dưới
            if ball_copy.posy <= 0 or ball_copy.posy >= WINDOW_HEIGHT:
                ball_copy.yFac *= -1
                ball_copy.posy = max(0, min(ball_copy.posy, WINDOW_HEIGHT))

        return ball_copy.posy

    def auto_move(self, ball):
        """Di chuyển AI đến vị trí bóng dự đoán một cách chính xác và nhanh chóng."""
        # Dự đoán vị trí bóng mà AI cần đến để đón bóng
        target_y = self.predict_ball_position(ball) - (PADDING_HEIGHT // 2)

        # Tính toán khoảng cách và di chuyển đến vị trí dự đoán
        distance_to_target = target_y - self.y

        # Chỉ di chuyển nếu bóng đang đi về phía AI
        if (ball.xFac < 0 and self.x < ball.posx) or (ball.xFac > 0 and self.x > ball.posx):
            move_distance = 0

            # Nếu khoảng cách giữa vị trí hiện tại và vị trí dự đoán nhỏ, AI sẽ di chuyển ngay lập tức
            if abs(distance_to_target) <= self.speed:
                move_distance = distance_to_target  # Di chuyển đến đúng vị trí
            else:
                move_distance = self.speed if distance_to_target > 0 else -self.speed

            # Di chuyển AI
            self.y += move_distance

            # Giới hạn AI không di chuyển ra ngoài màn hình
            self.y = max(0, min(self.y, WINDOW_HEIGHT - PADDING_HEIGHT))