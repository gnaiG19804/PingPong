import pygame as pg
import math
import random
from define import *
from sound import SettingsScreen
from setting import sound_manager

class Menu:
    def __init__(self, window):
        self.window = window
        # Fonts with varied sizes
        self.title_font = pg.font.Font(None, 70)
        self.button_font = pg.font.Font(None, 40)
        self.small_font = pg.font.Font(None, 28)
        
        # Giữ nguyên kích thước nút như code gốc
        self.button_width = 300
        self.button_height = 50
        
        # Color scheme - đổi màu đỏ thành màu vàng
        self.title_color = (255, 215, 0)  # Gold
        self.button_colors = {
            'normal': (255, 52 ,179),     # Màu vàng vừa (Golden Rod)
            'hover': (255, 215, 0),       # Màu vàng sáng hơn khi hover (Gold)
            'active': (255, 223, 80)      # Màu vàng sáng nhất khi active
        }
        
        # Load and scale background
        self.background = pg.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Add overlay for better text visibility
        self.overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 80))  # Semi-transparent black overlay
        
        # Animation variables
        self.animation_counter = 0
        self.button_hover = None
        self.button_active = None
        self.particle_effects = []
        
        # Sound manager
        self.sound_manager = sound_manager
        
        # Game title
        self.game_title = "PONG"

    def draw_text(self, text, font, x, y, color=WHITE, align="center"):
        """ Enhanced text rendering with optional alignment """
        label = font.render(text, True, color)
        text_rect = label.get_rect()
        
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.left = x
            text_rect.centery = y
        elif align == "right":
            text_rect.right = x
            text_rect.centery = y
            
        self.window.blit(label, text_rect)
        return text_rect

    def draw_button(self, text, x, y, index):
        """ Enhanced button drawing with animations and effects """
        is_hover = self.button_hover == index
        is_active = self.button_active == index
        
        # Determine button color based on state
        if is_active:
            color = self.button_colors['active']
        elif is_hover:
            color = self.button_colors['hover']
        else:
            color = self.button_colors['normal']
            
        rect = pg.Rect(x, y, self.button_width, self.button_height)
        
        # Main button body
        pg.draw.rect(self.window, color, rect, border_radius=12)
        
        # Button highlight (top)
        highlight_rect = pg.Rect(rect.left + 2, rect.top + 2, rect.width - 4, rect.height // 3)
        pg.draw.rect(self.window, (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 40, 255)), 
                    highlight_rect, border_radius=12, border_top_left_radius=12, 
                    border_top_right_radius=12, border_bottom_left_radius=0, 
                    border_bottom_right_radius=0)
        
        # Button shadow (subtle dark outline)
        shadow_rect = pg.Rect(rect.left, rect.top + rect.height - 4, rect.width, 4)
        pg.draw.rect(self.window, (color[0]*0.7, color[1]*0.7, color[2]*0.7), 
                     shadow_rect, border_radius=12, border_top_left_radius=0,
                     border_top_right_radius=0, border_bottom_left_radius=12, 
                     border_bottom_right_radius=12)
        
        # Button border - slightly darker gold border
        border_color = (139, 101, 8)  # Darker gold
        pg.draw.rect(self.window, border_color, rect, 2, border_radius=12)
        
        # Button text with shadow
        shadow_pos = (rect.centerx + 2, rect.centery + 2)
        self.draw_text(text, self.button_font, *shadow_pos, (60, 40, 0))  # Dark gold shadow
        self.draw_text(text, self.button_font, rect.centerx, rect.centery, WHITE)
        
        return rect

    def draw_particles(self):
        """ Draw particle effects """
        new_particles = []
        for particle in self.particle_effects:
            x, y, color, size, life, dx, dy = particle
            
            # Update particle position and life
            x += dx
            y += dy
            life -= 1
            size -= 0.1
            
            if life > 0 and size > 0:
                # Draw particle
                pg.draw.circle(self.window, color, (int(x), int(y)), int(size))
                new_particles.append([x, y, color, size, life, dx, dy])
                
        self.particle_effects = new_particles

    def create_hover_particles(self, rect):
        """ Create particles when hovering over buttons - now gold particles """
        for _ in range(2):
            x = rect.left + rect.width * random.random()
            y = rect.centery + (rect.height * 0.5 * (random.random() - 0.5))
            # Gold/yellow particle colors
            color = (255, 215 + random.randint(-30, 30), 0 + random.randint(0, 100))
            size = random.randint(2, 4)
            life = random.randint(5, 15)
            dx = random.uniform(-1, 1)
            dy = random.uniform(-0.5, 0.5)
            
            self.particle_effects.append([x, y, color, size, life, dx, dy])

    def display(self):
        """ Main menu display and interaction loop """
        run_menu = True
        clock = pg.time.Clock()
        
        # Sử dụng các vị trí nút được chỉ định trong code gốc
        button_positions = [
            ("PvP", 260),
            ("PvE", 330),
            ("AI vs AI", 400),
            ("Rankings", 470),
            ("Settings", 540)
        ]
        
        while run_menu:
            # Time-based animation
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            self.animation_counter += dt * 5
            
            # Draw background with overlay
            self.window.blit(self.background, (0, 0))
            self.window.blit(self.overlay, (0, 0))
            
            # Draw animated title
            title_y = 120 + math.sin(self.animation_counter * 0.5) * 5
            title_shadow_pos = (WINDOW_WIDTH // 2 + 3, title_y + 3)
            self.draw_text(self.game_title, self.title_font, *title_shadow_pos, (60, 40, 0))  # Dark gold shadow
            self.draw_text(self.game_title, self.title_font, WINDOW_WIDTH // 2, title_y, self.title_color)
            
            # Draw decorative line under title
            line_y = title_y + 40
            line_width = 400 + math.sin(self.animation_counter * 0.3) * 20
            pg.draw.line(self.window, self.title_color, 
                        (WINDOW_WIDTH//2 - line_width//2, line_y),
                        (WINDOW_WIDTH//2 + line_width//2, line_y), 3)
            
            # Draw buttons at their original positions
            button_x = (WINDOW_WIDTH - self.button_width) // 2
            buttons_rects = []
            
            for i, (text, y) in enumerate(button_positions):
                rect = self.draw_button(text, button_x, y, i)
                buttons_rects.append(rect)
                
                # Create hover particles
                if self.button_hover == i:
                    self.create_hover_particles(rect)
            
            # Draw particles
            self.draw_particles()
            
            # Draw footer text
            
            
            pg.display.update()
            
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                
                # Handle mouse movement for hover effects
                if event.type == pg.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    self.button_hover = None
                    for i, rect in enumerate(buttons_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.button_hover = i
                            break
                
                # Handle mouse clicks
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for i, rect in enumerate(buttons_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.button_active = i
                            # Play button sound
                            if hasattr(self.sound_manager, 'play_button_sound'):
                                self.sound_manager.play_button_sound()
                
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.button_active is not None:
                        for i, rect in enumerate(buttons_rects):
                            if i == self.button_active and rect.collidepoint(mouse_x, mouse_y):
                                # Handle button actions
                                if i == 4:  # Settings
                                    settings_screen = SettingsScreen(self.window, self.sound_manager)
                                    result = settings_screen.show()
                                    if result in ["Back", "Confirm"]:
                                        continue
                                else:
                                    return button_positions[i][0]  # Return the value from the original positions list
                    
                    self.button_active = None