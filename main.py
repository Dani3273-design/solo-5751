import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernel.game_logic import GameLogic
from kernel.graphics import Graphics
from kernel.mouse_handler import MouseHandler

def main():
    pygame.init()
    
    graphics = Graphics(window_width=600, window_height=700)
    game_logic = GameLogic()
    mouse_handler = MouseHandler(min_swipe_distance=30)
    
    game_logic.reset()
    
    clock = pygame.time.Clock()
    FPS = 60
    
    running = True
    won = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                graphics.quit()
                sys.exit()
            
            mouse_handler.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_logic.reset()
                    won = False
                elif event.key == pygame.K_LEFT:
                    game_logic.move_left()
                elif event.key == pygame.K_RIGHT:
                    game_logic.move_right()
                elif event.key == pygame.K_UP:
                    game_logic.move_up()
                elif event.key == pygame.K_DOWN:
                    game_logic.move_down()
        
        swipe_direction = mouse_handler.get_swipe_direction()
        if swipe_direction and not game_logic.is_game_over():
            if swipe_direction == 'left':
                game_logic.move_left()
            elif swipe_direction == 'right':
                game_logic.move_right()
            elif swipe_direction == 'up':
                game_logic.move_up()
            elif swipe_direction == 'down':
                game_logic.move_down()
        
        if game_logic.has_won() and not won:
            won = True
        
        graphics.draw(
            game_logic.get_grid(),
            game_logic.get_score(),
            game_logic.is_game_over(),
            won
        )
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
