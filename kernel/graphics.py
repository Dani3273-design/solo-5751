import pygame
import sys

class Graphics:
    def __init__(self, window_width=600, window_height=750):
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('2048')
        
        self.grid_size = 4
        self.cell_size = 100
        self.cell_padding = 10
        
        self.grid_width = self.grid_size * self.cell_size + (self.grid_size + 1) * self.cell_padding
        self.grid_height = self.grid_width
        
        self.grid_x = (window_width - self.grid_width) // 2
        self.grid_y = 150
        
        self.background_color = (187, 173, 160)
        self.grid_background_color = (204, 192, 178)
        self.cell_empty_color = (205, 193, 180)
        
        self.button_color = (143, 122, 102)
        self.button_hover_color = (163, 142, 122)
        self.button_text_color = (249, 246, 242)
        
        self.tile_colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            4096: (60, 58, 50),
            8192: (60, 58, 50),
        }
        
        self.text_colors = {
            2: (119, 110, 101),
            4: (119, 110, 101),
            8: (249, 246, 242),
            16: (249, 246, 242),
            32: (249, 246, 242),
            64: (249, 246, 242),
            128: (249, 246, 242),
            256: (249, 246, 242),
            512: (249, 246, 242),
            1024: (249, 246, 242),
            2048: (249, 246, 242),
            4096: (249, 246, 242),
            8192: (249, 246, 242),
        }
        
        self.font_large = pygame.font.SysFont('stheitimedium, songti, arialunicode, arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('stheitimedium, songti, arialunicode, arial', 36, bold=True)
        self.font_small = pygame.font.SysFont('stheitimedium, songti, arialunicode, arial', 24, bold=True)
        self.font_mini = pygame.font.SysFont('stheitimedium, songti, arialunicode, arial', 18, bold=True)
        
        self.animations = []
        self.is_animating = False
        
        self.buttons = {
            'start': {'rect': None, 'text': '开始游戏', 'active': False},
            'restart': {'rect': None, 'text': '重新开始', 'active': False}
        }

    def get_grid_position(self):
        return self.grid_x, self.grid_y

    def get_grid_size(self):
        return self.grid_width, self.grid_height

    def get_cell_position(self, row, col):
        x = self.grid_x + self.cell_padding + col * (self.cell_size + self.cell_padding)
        y = self.grid_y + self.cell_padding + row * (self.cell_size + self.cell_padding)
        return x, y

    def add_animation(self, start_row, start_col, end_row, end_col, value, is_new=False, is_merged=False):
        start_x, start_y = self.get_cell_position(start_row, start_col)
        end_x, end_y = self.get_cell_position(end_row, end_col)
        
        animation = {
            'start_x': start_x,
            'start_y': start_y,
            'end_x': end_x,
            'end_y': end_y,
            'current_x': start_x,
            'current_y': start_y,
            'value': value,
            'is_new': is_new,
            'is_merged': is_merged,
            'progress': 0.0,
            'duration': 200,
            'scale': 1.0 if not is_merged else 0.8
        }
        self.animations.append(animation)
        self.is_animating = True

    def update_animations(self, dt):
        if not self.animations:
            self.is_animating = False
            return
        
        for anim in self.animations:
            anim['progress'] += dt
            if anim['progress'] >= anim['duration']:
                anim['progress'] = anim['duration']
            
            t = anim['progress'] / anim['duration']
            t = t * t * (3 - 2 * t)
            
            anim['current_x'] = anim['start_x'] + (anim['end_x'] - anim['start_x']) * t
            anim['current_y'] = anim['start_y'] + (anim['end_y'] - anim['start_y']) * t
            
            if anim['is_merged']:
                anim['scale'] = 0.8 + 0.2 * t
            elif anim['is_new']:
                anim['scale'] = t
        
        self.animations = [a for a in self.animations if a['progress'] < a['duration']]
        if not self.animations:
            self.is_animating = False

    def clear_animations(self):
        self.animations = []
        self.is_animating = False

    def draw_rounded_rect(self, surface, color, rect, border_radius=5):
        x, y, w, h = rect
        radius = min(border_radius, w // 2, h // 2)
        
        pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
        pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
        
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

    def draw_tile(self, x, y, value, scale=1.0):
        if value == 0:
            return
        
        size = int(self.cell_size * scale)
        offset = (self.cell_size - size) // 2
        
        color = self.tile_colors.get(value, self.tile_colors[8192])
        text_color = self.text_colors.get(value, self.text_colors[8192])
        
        if scale < 1.0:
            x = x + offset
            y = y + offset
        
        self.draw_rounded_rect(self.screen, color, (x, y, size, size), border_radius=3)
        
        if value < 100:
            font = self.font_large
        elif value < 1000:
            font = self.font_medium
        else:
            font = self.font_small
        
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(x + size // 2, y + size // 2))
        self.screen.blit(text, text_rect)

    def draw_button(self, button_key, x, y, width, height, mouse_pos):
        button = self.buttons[button_key]
        rect = pygame.Rect(x, y, width, height)
        button['rect'] = rect
        
        is_hovered = rect.collidepoint(mouse_pos)
        color = self.button_hover_color if is_hovered else self.button_color
        
        self.draw_rounded_rect(self.screen, color, (x, y, width, height), border_radius=5)
        
        text = self.font_small.render(button['text'], True, self.button_text_color)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text, text_rect)
        
        return is_hovered

    def draw_game_over(self, score):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("游戏结束!", True, (119, 110, 101))
        score_text = self.font_medium.render(f"分数: {score}", True, (119, 110, 101))
        
        self.screen.blit(game_over_text, 
                        ((self.window_width - game_over_text.get_width()) // 2, 
                         (self.window_height - game_over_text.get_height()) // 2 - 80))
        
        self.screen.blit(score_text, 
                        ((self.window_width - score_text.get_width()) // 2, 
                         (self.window_height - score_text.get_height()) // 2 - 20))

    def draw_win(self, score):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.font_large.render("你赢了!", True, (119, 110, 101))
        score_text = self.font_medium.render(f"分数: {score}", True, (119, 110, 101))
        continue_text = self.font_mini.render("点击重新开始或继续挑战更高分数", True, (119, 110, 101))
        
        self.screen.blit(win_text, 
                        ((self.window_width - win_text.get_width()) // 2, 
                         (self.window_height - win_text.get_height()) // 2 - 80))
        
        self.screen.blit(score_text, 
                        ((self.window_width - score_text.get_width()) // 2, 
                         (self.window_height - score_text.get_height()) // 2 - 20))
        
        self.screen.blit(continue_text, 
                        ((self.window_width - continue_text.get_width()) // 2, 
                         (self.window_height - continue_text.get_height()) // 2 + 40))

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def draw(self, grid, score, game_state, elapsed_time=0, mouse_pos=(0, 0)):
        self.screen.fill(self.background_color)
        
        title_text = self.font_large.render("2048", True, (119, 110, 101))
        self.screen.blit(title_text, (20, 20))
        
        score_box_x = self.window_width - 130
        score_box_y = 20
        score_box_width = 110
        score_box_height = 60
        
        self.draw_rounded_rect(self.screen, self.grid_background_color, 
                               (score_box_x, score_box_y, score_box_width, score_box_height), 
                               border_radius=5)
        
        score_label = self.font_mini.render("分数", True, (119, 110, 101))
        score_value = self.font_medium.render(str(score), True, (119, 110, 101))
        
        self.screen.blit(score_label, 
                        (score_box_x + (score_box_width - score_label.get_width()) // 2, 
                         score_box_y + 5))
        self.screen.blit(score_value, 
                        (score_box_x + (score_box_width - score_value.get_width()) // 2, 
                         score_box_y + 25))
        
        time_box_x = score_box_x - 120
        time_box_y = 20
        time_box_width = 110
        time_box_height = 60
        
        self.draw_rounded_rect(self.screen, self.grid_background_color, 
                               (time_box_x, time_box_y, time_box_width, time_box_height), 
                               border_radius=5)
        
        time_label = self.font_mini.render("时间", True, (119, 110, 101))
        time_value = self.font_medium.render(self.format_time(elapsed_time), True, (119, 110, 101))
        
        self.screen.blit(time_label, 
                        (time_box_x + (time_box_width - time_label.get_width()) // 2, 
                         time_box_y + 5))
        self.screen.blit(time_value, 
                        (time_box_x + (time_box_width - time_value.get_width()) // 2, 
                         time_box_y + 25))
        
        self.draw_rounded_rect(self.screen, self.grid_background_color, 
                               (self.grid_x, self.grid_y, self.grid_width, self.grid_height), 
                               border_radius=5)
        
        for i in range(4):
            for j in range(4):
                x, y = self.get_cell_position(i, j)
                self.draw_rounded_rect(self.screen, self.cell_empty_color, 
                                       (x, y, self.cell_size, self.cell_size), 
                                       border_radius=3)
        
        if self.is_animating:
            for anim in self.animations:
                if anim['is_new'] and anim['scale'] < 0.1:
                    continue
                self.draw_tile(anim['current_x'], anim['current_y'], anim['value'], anim['scale'])
        else:
            for i in range(4):
                for j in range(4):
                    value = grid[i][j]
                    if value != 0:
                        x, y = self.get_cell_position(i, j)
                        self.draw_tile(x, y, value)
        
        button_width = 120
        button_height = 40
        button_y = self.grid_y + self.grid_height + 20
        
        if game_state == 'idle':
            self.draw_button('start', (self.window_width - button_width) // 2, button_y, 
                           button_width, button_height, mouse_pos)
        elif game_state in ['playing', 'won', 'game_over']:
            self.draw_button('restart', (self.window_width - button_width) // 2, button_y, 
                           button_width, button_height, mouse_pos)
        
        if game_state == 'idle':
            instruction_text = self.font_mini.render("点击「开始游戏」按钮开始", True, (119, 110, 101))
            self.screen.blit(instruction_text, 
                            ((self.window_width - instruction_text.get_width()) // 2, 
                             self.grid_y - 30))
        elif game_state == 'playing':
            instruction_text = self.font_mini.render("鼠标拖动来移动方块", True, (119, 110, 101))
            self.screen.blit(instruction_text, 
                            ((self.window_width - instruction_text.get_width()) // 2, 
                             self.grid_y - 30))
        
        if game_state == 'game_over':
            self.draw_game_over(score)
        elif game_state == 'won':
            self.draw_win(score)
        
        pygame.display.update()

    def check_button_click(self, pos):
        for key, button in self.buttons.items():
            if button['rect'] and button['rect'].collidepoint(pos):
                return key
        return None

    def quit(self):
        pygame.quit()
        sys.exit()
