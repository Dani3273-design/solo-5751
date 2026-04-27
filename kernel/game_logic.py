import random

class GameLogic:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.new_tile_pos = None

    def reset(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.new_tile_pos = None
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

    def _compress(self, row):
        new_row = [i for i in row if i != 0]
        while len(new_row) < 4:
            new_row.append(0)
        return new_row

    def _merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                if row[i] == 2048:
                    self.won = True
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(4):
            original = self.grid[i][:]
            self.grid[i] = self._compress(self.grid[i])
            self.grid[i] = self._merge(self.grid[i])
            self.grid[i] = self._compress(self.grid[i])
            if self.grid[i] != original:
                moved = True
        if moved:
            self._add_new_tile()
            self._check_game_over()
        return moved

    def move_right(self):
        moved = False
        for i in range(4):
            original = self.grid[i][:]
            self.grid[i] = self.grid[i][::-1]
            self.grid[i] = self._compress(self.grid[i])
            self.grid[i] = self._merge(self.grid[i])
            self.grid[i] = self._compress(self.grid[i])
            self.grid[i] = self.grid[i][::-1]
            if self.grid[i] != original:
                moved = True
        if moved:
            self._add_new_tile()
            self._check_game_over()
        return moved

    def move_up(self):
        moved = False
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            original = column[:]
            column = self._compress(column)
            column = self._merge(column)
            column = self._compress(column)
            for i in range(4):
                self.grid[i][j] = column[i]
            if [self.grid[i][j] for i in range(4)] != original:
                moved = True
        if moved:
            self._add_new_tile()
            self._check_game_over()
        return moved

    def move_down(self):
        moved = False
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            original = column[:]
            column = column[::-1]
            column = self._compress(column)
            column = self._merge(column)
            column = self._compress(column)
            column = column[::-1]
            for i in range(4):
                self.grid[i][j] = column[i]
            if [self.grid[i][j] for i in range(4)] != original:
                moved = True
        if moved:
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

    def copy_grid(self):
        return [row[:] for row in self.grid]
