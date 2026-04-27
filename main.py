import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernel.game_logic import GameLogic
from kernel.graphics import Graphics
from kernel.mouse_handler import MouseHandler

def main():
    pygame.init()
    
    graphics = Graphics(window_width=600, window_height=750)
    game_logic = GameLogic()
    mouse_handler = MouseHandler(min_swipe_distance=30)
    
    clock = pygame.time.Clock()
    FPS = 60
    
    game_state = 'idle'
    start_time = 0
    elapsed_time = 0
    won_state = False
    
    running = True
    
    while running:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        if game_state == 'playing':
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                graphics.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = graphics.check_button_click(event.pos)
                
                if button_clicked == 'start' and game_state == 'idle':
                    game_logic.reset()
                    graphics.clear_animations()
                    start_time = pygame.time.get_ticks()
                    elapsed_time = 0
                    won_state = False
                    game_state = 'playing'
                elif button_clicked == 'restart':
                    game_logic.reset()
                    graphics.clear_animations()
                    start_time = pygame.time.get_ticks()
                    elapsed_time = 0
                    won_state = False
                    game_state = 'playing'
                else:
                    mouse_handler.handle_event(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_handler.handle_event(event)
                
                if game_state == 'playing' and not graphics.is_animating:
                    swipe_direction = mouse_handler.get_swipe_direction()
                    if swipe_direction:
                        moved = False
                        if swipe_direction == 'left':
                            moved = game_logic.move_left()
                        elif swipe_direction == 'right':
                            moved = game_logic.move_right()
                        elif swipe_direction == 'up':
                            moved = game_logic.move_up()
                        elif swipe_direction == 'down':
                            moved = game_logic.move_down()
                        
                        if moved:
                            animations = game_logic.get_move_animations()
                            for anim in animations:
                                from_row, from_col, to_row, to_col, value = anim
                                graphics.add_animation(from_row, from_col, to_row, to_col, value)
                            
                            new_tile = game_logic.get_new_tile()
                            if new_tile:
                                row, col, value = new_tile
                                graphics.add_animation(row, col, row, col, value, is_new=True)
                            
                            if game_logic.has_won() and not won_state:
                                won_state = True
                                game_state = 'won'
                            elif game_logic.is_game_over():
                                game_state = 'game_over'
            
            elif event.type == pygame.MOUSEMOTION:
                mouse_handler.handle_event(event)
        
        if graphics.is_animating:
            graphics.update_animations(dt)
        
        current_score = game_logic.get_score()
        current_grid = game_logic.get_grid()
        
        graphics.draw(
            current_grid,
            current_score,
            game_state,
            elapsed_time,
            mouse_pos
        )
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
