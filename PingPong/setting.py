import pygame
import os
class SoundManager:
    def __init__(self, volume=1.0, sound_enabled=True):
        self.volume = volume
        self.sound_enabled = sound_enabled

        # Lấy đường dẫn thư mục hiện tại (nơi đặt file setting.py)
        base_path = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(base_path, "sounds")

        print(os.path.join(sound_path, "hit.wav"))

        pygame.mixer.init()
        
        if self.sound_enabled:
            try:
                self.hit_sound = pygame.mixer.Sound(os.path.join(sound_path, "hit.wav"))
                self.hit_sound.set_volume(self.volume)

                self.win_sound = pygame.mixer.Sound(os.path.join(sound_path, "win.wav"))
                self.win_sound.set_volume(self.volume)

                self.lose_sound = pygame.mixer.Sound(os.path.join(sound_path, "lose.wav"))
                self.lose_sound.set_volume(self.volume)

                self.score_sound = pygame.mixer.Sound(os.path.join(sound_path,"score.wav"))
                self.score_sound.set_volume(self.volume)
                
                self.winAi = pygame.mixer.Sound(os.path.join(sound_path,"win1.wav"))
                self.winAi.set_volume(self.volume)

                pygame.mixer.music.load(os.path.join(sound_path, "background_music.mp3"))
                pygame.mixer.music.set_volume(self.volume)

            except pygame.error as e:
                print(f"[Sound Error] {e}")
                self.hit_sound = None
                self.win_sound = None
                self.lose_sound = None
                self.score_sound = None
        else:
            self.hit_sound = None
            self.win_sound = None
            self.lose_sound = None
            self.score_sound = None

    def play_hit(self):
        if self.sound_enabled:
            self.hit_sound.play()
    def play_score(self):
        if self.sound_enabled:
            self.score_sound.play()
    def play_win(self):
        if self.sound_enabled and self.win_sound:
            self.win_sound.play()

    def player_win(self):
        if self.sound_enabled and self.winAi:
            self.winAi.play()

    def play_lose(self):
        if self.sound_enabled and self.lose_sound:
            self.lose_sound.play()

    def play_music(self, loop=True):
        if self.sound_enabled:
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume=1.0):
        self.volume = volume
        if self.hit_sound:
            self.hit_sound.set_volume(volume)
        if self.win_sound:
            self.win_sound.set_volume(volume)
        if self.lose_sound:
            self.lose_sound.set_volume(volume)
        pygame.mixer.music.set_volume(volume)
    
    def toggle_sound(self, enabled: bool):
        self.sound_enabled = enabled
        if enabled:
           self.set_volume(self.volume)
           self.play_music()  # Phát lại nhạc nếu bật
        else:
           self.stop_music()


# Instance dùng trong toàn game
sound_manager = SoundManager(volume=0.5, sound_enabled=True)

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, color=(200, 200, 200), handle_color=(100, 100, 255)):
        self.rect = pygame.Rect(x, y, width, 8)  # thân thanh slider
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_radius = 10
        self.color = color
        self.handle_color = handle_color
        self.handle_x = self.value_to_pos(self.value)
        self.dragging = False

    def value_to_pos(self, value):
        """Chuyển giá trị thành vị trí X trên thanh"""
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + int(ratio * self.rect.width)

    def pos_to_value(self, x):
        """Chuyển vị trí X thành giá trị"""
        ratio = (x - self.rect.x) / self.rect.width
        return max(self.min_val, min(self.max_val, self.min_val + ratio * (self.max_val - self.min_val)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < self.handle_radius and abs(event.pos[1] - self.rect.centery) < self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.value = self.pos_to_value(self.handle_x)

    def draw(self, screen):
        # Vẽ thanh
        pygame.draw.rect(screen, self.color, self.rect)
        # Vẽ vòng tròn kéo
        pygame.draw.circle(screen, self.handle_color, (self.handle_x, self.rect.centery), self.handle_radius)

    def get_value(self):
        return self.value
