import pygame
import sys

class Graphics:
    def __init__(self, window_width=600, window_height=700):
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('2048')
        
        self.grid_size = 4
        self.grid_padding = 15
        self.cell_size = 100
        self.cell_padding = 10
        
        self.grid_width = self.grid_size * self.cell_size + (self.grid_size + 1) * self.cell_padding
        self.grid_height = self.grid_width
        
        self.grid_x = (window_width - self.grid_width) // 2
        self.grid_y = 120
        
        self.background_color = (187, 173, 160)
        self.grid_background_color = (204, 192, 178)
        self.cell_empty_color = (205, 193, 180)
        
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
        
        self.font_large = pygame.font.SysFont('arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 36, bold=True)
        self.font_small = pygame.font.SysFont('arial', 24, bold=True)

    def get_grid_position(self):
        return self.grid_x, self.grid_y

    def get_grid_size(self):
        return self.grid_width, self.grid_height

    def draw_game_over(self, score):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("Game Over!", True, (119, 110, 101))
        score_text = self.font_medium.render(f"Score: {score}", True, (119, 110, 101))
        restart_text = self.font_small.render("Press R to Restart", True, (119, 110, 101))
        
        self.screen.blit(game_over_text, 
                        ((self.window_width - game_over_text.get_width()) // 2, 
                         (self.window_height - game_over_text.get_height()) // 2 - 80))
        
        self.screen.blit(score_text, 
                        ((self.window_width - score_text.get_width()) // 2, 
                         (self.window_height - score_text.get_height()) // 2 - 20))
        
        self.screen.blit(restart_text, 
                        ((self.window_width - restart_text.get_width()) // 2, 
                         (self.window_height - restart_text.get_height()) // 2 + 40))

    def draw_win(self, score):
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.font_large.render("You Win!", True, (119, 110, 101))
        score_text = self.font_medium.render(f"Score: {score}", True, (119, 110, 101))
        continue_text = self.font_small.render("Press R to Restart or Continue Playing", True, (119, 110, 101))
        
        self.screen.blit(win_text, 
                        ((self.window_width - win_text.get_width()) // 2, 
                         (self.window_height - win_text.get_height()) // 2 - 80))
        
        self.screen.blit(score_text, 
                        ((self.window_width - score_text.get_width()) // 2, 
                         (self.window_height - score_text.get_height()) // 2 - 20))
        
        self.screen.blit(continue_text, 
                        ((self.window_width - continue_text.get_width()) // 2, 
                         (self.window_height - continue_text.get_height()) // 2 + 40))

    def draw(self, grid, score, game_over=False, won=False):
        self.screen.fill(self.background_color)
        
        title_text = self.font_large.render("2048", True, (119, 110, 101))
        self.screen.blit(title_text, (20, 20))
        
        score_surface = pygame.Surface((150, 50))
        score_surface.fill(self.grid_background_color)
        score_label = self.font_small.render("SCORE", True, (255, 255, 255))
        score_value = self.font_medium.render(str(score), True, (255, 255, 255))
        
        score_surface.blit(score_label, 
                          ((150 - score_label.get_width()) // 2, 5))
        score_surface.blit(score_value, 
                          ((150 - score_value.get_width()) // 2, 20))
        
        self.screen.blit(score_surface, (self.window_width - 170, 20))
        
        pygame.draw.rect(self.screen, self.grid_background_color, 
                        (self.grid_x, self.grid_y, self.grid_width, self.grid_height), 
                        border_radius=5)
        
        for i in range(4):
            for j in range(4):
                value = grid[i][j]
                x = self.grid_x + self.cell_padding + j * (self.cell_size + self.cell_padding)
                y = self.grid_y + self.cell_padding + i * (self.cell_size + self.cell_padding)
                
                color = self.tile_colors.get(value, self.tile_colors[8192])
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size), border_radius=3)
                
                if value != 0:
                    text_color = self.text_colors.get(value, self.text_colors[8192])
                    if value < 100:
                        font = self.font_large
                    elif value < 1000:
                        font = self.font_medium
                    else:
                        font = self.font_small
                    
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)
        
        if won:
            self.draw_win(score)
        elif game_over:
            self.draw_game_over(score)
        
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()
