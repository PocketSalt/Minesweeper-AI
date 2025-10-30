import random
import numpy
from tile import Tile

class GameState:
    def __init__(self, grid_size, bomb_count):
        self.gridSize = grid_size
        self.bombCount = bomb_count
        self.grid = numpy.empty((self.gridSize, self.gridSize), dtype=object)

        # initialise all tiles
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                self.grid[row][col] = Tile(0, False)

        self.RandomiseBombs(self.bombCount)
        self.InitTiles()

    def Restart(self):
        # recreate grid with the same settings
        self.__init__(self.gridSize, self.bombCount)
        Tile.correctFlagCount = 0

# old version that actually randomises all without making sure 1,1 is safe
    '''
    def RandomiseBombs(self, numBombs):
        placed = 0
        while placed < numBombs:
            row = random.randint(0, self.gridSize-1)
            col = random.randint(0, self.gridSize-1)
            if self.grid[row][col].value != -1 and not (row == 1 and col == 1):
                self.grid[row][col].value = -1
                placed += 1
    '''

    # this is to ensure 1,1 and its surroundings are safe to eliminate bad starts
    def RandomiseBombs(self, numBombs):
        placed = 0
        safe_coords = [(r, c) for r in range(0, 3) for c in range(0, 3)]  # 3x3 block around (1,1)

        while placed < numBombs:
            row = random.randint(0, self.gridSize-1)
            col = random.randint(0, self.gridSize-1)
            if self.grid[row][col].value != -1 and (row, col) not in safe_coords:
                self.grid[row][col].value = -1
                placed += 1


    def InitTiles(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col].value != -1:
                    self.grid[row][col].value = self.CountAdjacentBombs(row, col)

    def CountAdjacentBombs(self, row, col):
        count = 0
        for rr in [-1, 0, 1]:
            for cc in [-1, 0, 1]:
                # so all around, ignore self
                if not (rr == 0 and cc == 0):
                    r = row + rr
                    c = col + cc
                    # ensure not going beyond array size
                    if 0 <= r < self.gridSize and 0 <= c < self.gridSize:
                        if self.grid[r][c].value == -1:
                            count += 1
        return count

    def Reveal(self, x, y):
        # exit recursion
        if self.grid[x][y].visible:
            return

        self.grid[x][y].reveal()

        # flood reveal neighbours if value = 0
        if self.grid[x][y].value == 0:
            neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for xx, yy in neighbours:
                row = x + xx
                col = y + yy
                if 0 <= row < self.gridSize and 0 <= col < self.gridSize:
                    self.Reveal(row, col)