import pygame

class MouseHandler:
    def __init__(self, min_swipe_distance=30):
        self.min_swipe_distance = min_swipe_distance
        self.start_pos = None
        self.end_pos = None
        self.swipe_direction = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_pos = event.pos
            self.end_pos = None
            self.swipe_direction = None
        elif event.type == pygame.MOUSEBUTTONUP:
            self.end_pos = event.pos
            self._calculate_direction()
        elif event.type == pygame.MOUSEMOTION and self.start_pos is not None:
            self.end_pos = event.pos

    def _calculate_direction(self):
        if self.start_pos is None or self.end_pos is None:
            self.swipe_direction = None
            return
        
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        
        if abs(dx) < self.min_swipe_distance and abs(dy) < self.min_swipe_distance:
            self.swipe_direction = None
            return
        
        if abs(dx) > abs(dy):
            if dx > 0:
                self.swipe_direction = 'right'
            else:
                self.swipe_direction = 'left'
        else:
            if dy > 0:
                self.swipe_direction = 'down'
            else:
                self.swipe_direction = 'up'

    def get_swipe_direction(self):
        direction = self.swipe_direction
        self.swipe_direction = None
        self.start_pos = None
        self.end_pos = None
        return direction

    def reset(self):
        self.start_pos = None
        self.end_pos = None
        self.swipe_direction = None
