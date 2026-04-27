import random

class GameLogic:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.new_tile_pos = None
        self.move_animations = []

    def reset(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.new_tile_pos = None
        self.move_animations = []
        self._add_new_tile()
        self._add_new_tile()

    def _add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            self.new_tile_pos = (i, j, self.grid[i][j])

    def get_new_tile(self):
        pos = self.new_tile_pos
        self.new_tile_pos = None
        return pos

    def get_move_animations(self):
        anims = self.move_animations
        self.move_animations = []
        return anims

    def _compress_with_tracking(self, row, row_idx, is_column=False, reverse=False):
        non_zero = [(val, idx) for idx, val in enumerate(row) if val != 0]
        result = [0] * 4
        movements = []
        
        for new_pos, (val, old_pos) in enumerate(non_zero):
            result[new_pos] = val
            if new_pos != old_pos:
                if reverse:
                    old_pos = 3 - old_pos
                    new_pos = 3 - new_pos
                if is_column:
                    movements.append((old_pos, row_idx, new_pos, row_idx, val))
                else:
                    movements.append((row_idx, old_pos, row_idx, new_pos, val))
        
        return result, movements

    def _merge_with_tracking(self, row, row_idx, is_column=False, reverse=False):
        movements = []
        merged_values = []
        
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                if row[i] == 2048:
                    self.won = True
                
                from_pos = i + 1
                to_pos = i
                val = row[i]
                
                if reverse:
                    from_pos = 3 - from_pos
                    to_pos = 3 - to_pos
                
                if is_column:
                    movements.append((from_pos, row_idx, to_pos, row_idx, val // 2))
                else:
                    movements.append((row_idx, from_pos, row_idx, to_pos, val // 2))
                
                merged_values.append((to_pos, row_idx, val) if is_column else (row_idx, to_pos, val))
                row[i + 1] = 0
        
        return row, movements, merged_values

    def move_left(self):
        moved = False
        all_movements = []
        all_merged = []
        
        for i in range(4):
            original = self.grid[i][:]
            row, compress_moves = self._compress_with_tracking(self.grid[i], i, is_column=False, reverse=False)
            all_movements.extend(compress_moves)
            
            row, merge_moves, merged = self._merge_with_tracking(row, i, is_column=False, reverse=False)
            all_movements.extend(merge_moves)
            all_merged.extend(merged)
            
            row, final_compress = self._compress_with_tracking(row, i, is_column=False, reverse=False)
            all_movements.extend(final_compress)
            
            self.grid[i] = row
            
            if self.grid[i] != original:
                moved = True
        
        if moved:
            self.move_animations = all_movements
            self._add_new_tile()
            self._check_game_over()
        
        return moved

    def move_right(self):
        moved = False
        all_movements = []
        all_merged = []
        
        for i in range(4):
            original = self.grid[i][:]
            reversed_row = self.grid[i][::-1]
            
            row, compress_moves = self._compress_with_tracking(reversed_row, i, is_column=False, reverse=True)
            all_movements.extend(compress_moves)
            
            row, merge_moves, merged = self._merge_with_tracking(row, i, is_column=False, reverse=True)
            all_movements.extend(merge_moves)
            
            row, final_compress = self._compress_with_tracking(row, i, is_column=False, reverse=True)
            all_movements.extend(final_compress)
            
            self.grid[i] = row[::-1]
            
            if self.grid[i] != original:
                moved = True
        
        if moved:
            self.move_animations = all_movements
            self._add_new_tile()
            self._check_game_over()
        
        return moved

    def move_up(self):
        moved = False
        all_movements = []
        all_merged = []
        
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            original = column[:]
            
            col, compress_moves = self._compress_with_tracking(column, j, is_column=True, reverse=False)
            all_movements.extend(compress_moves)
            
            col, merge_moves, merged = self._merge_with_tracking(col, j, is_column=True, reverse=False)
            all_movements.extend(merge_moves)
            
            col, final_compress = self._compress_with_tracking(col, j, is_column=True, reverse=False)
            all_movements.extend(final_compress)
            
            for i in range(4):
                self.grid[i][j] = col[i]
            
            new_column = [self.grid[i][j] for i in range(4)]
            if new_column != original:
                moved = True
        
        if moved:
            self.move_animations = all_movements
            self._add_new_tile()
            self._check_game_over()
        
        return moved

    def move_down(self):
        moved = False
        all_movements = []
        all_merged = []
        
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            original = column[:]
            reversed_col = column[::-1]
            
            col, compress_moves = self._compress_with_tracking(reversed_col, j, is_column=True, reverse=True)
            all_movements.extend(compress_moves)
            
            col, merge_moves, merged = self._merge_with_tracking(col, j, is_column=True, reverse=True)
            all_movements.extend(merge_moves)
            
            col, final_compress = self._compress_with_tracking(col, j, is_column=True, reverse=True)
            all_movements.extend(final_compress)
            
            final_col = col[::-1]
            for i in range(4):
                self.grid[i][j] = final_col[i]
            
            new_column = [self.grid[i][j] for i in range(4)]
            if new_column != original:
                moved = True
        
        if moved:
            self.move_animations = all_movements
            self._add_new_tile()
            self._check_game_over()
        
        return moved

    def _check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return
        self.game_over = True

    def get_grid(self):
        return self.grid

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.game_over

    def has_won(self):
        return self.won
