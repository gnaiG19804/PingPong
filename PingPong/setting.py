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
                self.hit_sound = pygame.mixer.Sound(os.path.join(sound_path, "hit4.wav"))
                self.hit_sound.set_volume(self.volume)

                self.win_sound = pygame.mixer.Sound(os.path.join(sound_path, "win.wav"))
                self.win_sound.set_volume(self.volume)

                self.lose_sound = pygame.mixer.Sound(os.path.join(sound_path, "lose.wav"))
                self.lose_sound.set_volume(self.volume)

                pygame.mixer.music.load(os.path.join(sound_path, "background_music.mp3"))
                pygame.mixer.music.set_volume(self.volume)
            except pygame.error as e:
                print(f"[Sound Error] {e}")
                self.hit_sound = None
                self.win_sound = None
                self.lose_sound = None
        else:
            self.hit_sound = None
            self.win_sound = None
            self.lose_sound = None

    def play_hit(self):
        if self.sound_enabled and self.hit_sound:
            self.hit_sound.play()

    def play_win(self):
        if self.sound_enabled and self.win_sound:
            self.win_sound.play()

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
