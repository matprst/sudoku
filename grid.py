class Cell:
    def __init__(self, row, col, content=None):
        self.fixed = content is not None # if init with content, not allowed to modify it
        self.content = content
        self.pos = (row, col)
    
    @property
    def is_fixed(self):
        return self.fixed
 
    @property
    def val(self):
        return self.content
    
    @property
    def position(self):
        return self.pos
    
    def is_empty(self):
        return self.content is None
    
    def fill(self, content):
        assert not self.is_fixed # cannot modify fixed cell
        self.content = content
    
    def __str__(self):
        return str(self.content) if self.content is not None else str(0)
    
    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.val == other.val
        elif isinstance(other, int):
            return self.val == other
        else:
            return False

class Grid:
    def __init__(self, grid):
        self.size = len(grid)
        self.grid = []
        for i, row in enumerate(grid):
            new_row = []
            for j, cell in enumerate(row):
                content = None if cell == 0 else cell
                new_row.append(Cell(i, j, content))
            self.grid.append(new_row)
    
    def is_solved(self):
        errors = 0
        nums = list(range(1, self.size+1))
        # check rows
        for row in self.grid:
            for n in nums:
                if n not in row:
                    errors += 1
                    # return False

        # check columns
        for col in range(self.size):
            column = [self.grid[row][col] for row in range(self.size)]
            for n in nums:
                if n not in column:
                    errors += 1
                    # return False
        
        # check squares
        square_size = int(self.size**0.5)
        for row in range(square_size): # iterate square by square
            for col in range(square_size):
                # gather the cells in a given square
                square = []
                for i in range(square_size):
                    for j in range(square_size):
                        cell = self.grid[row*square_size+i][col*square_size+j]
                        square.append(cell)
                for n in nums:
                    if n not in square:
                        errors += 1
                        # return False
        return errors == 0
    
    def fill_cell(self, row, col, content):
        assert 0 <= row < self.size and 0 <= col < self.size
        self.grid[row][col].fill(content) 
    
    def columns(self):
        return GridColIterator(self.grid)
    
    def rows(self):
        return GridRowIterator(self.grid)
    
    def squares(self):
        return GridSquareIterator(self.grid)
    
    def __iter__(self):
        return GridCellIterator(self.grid)
    
    def __getitem__(self, index):
        return self.grid[index]
    
    def __str__(self):
        s = ''
        for row in self.grid:
            s += f"{' '.join([str(cell) for cell in row])}\n"
        return s
    
class GridCellIterator:
    def __init__(self, grid):
        self.grid = grid
        self.row = 0
        self.col = 0
    
    def __next__(self):
        row, col = self.row, self.col

        self.col += 1

        if self.col == len(self.grid[0]):
            self.col = 0
            self.row += 1
        
        if row >= len(self.grid) or col >= len(self.grid[0]):
            raise StopIteration
        
        return self.grid[row][col]

class GridRowIterator:
    def __init__(self, grid):
        self.grid = grid
        self.row = 0
    
    def __next__(self):
        row = self.row
        self.row += 1

        if row >= len(self.grid):
            raise StopIteration
        
        return self.grid[row]
    
    def __iter__(self):
        return self

class GridColIterator:
    def __init__(self, grid):
        self.grid = grid
        self.col = 0
    
    def __next__(self):
        col = self.col
        self.col += 1

        if col >= len(self.grid[0]):
            raise StopIteration
        
        return [self.grid[row][col] for row in range(len(self.grid))]
    
    def __iter__(self):
        return self

class GridSquareIterator:
    def __init__(self, grid):
        self.grid = grid
        self.square_size = int(len(self.grid)**0.5) # assumes grid is a sudoku
        self.row = 0
        self.col = 0
    
    def __next__(self):
        row, col = self.row, self.col

        self.col += 1

        if self.col == self.square_size:
            self.col = 0
            self.row += 1
        
        if row >= self.square_size or col >= self.square_size:
            raise StopIteration
        
        return [self.grid[row*self.square_size+i][col*self.square_size+j] for i in range(self.square_size) for j in range(self.square_size)]
    
    def __iter__(self):
        return self
    


if __name__ == "__main__":
    # grid = [
    #     [5, 2, 3, 6, 8, 0, 0, 0, 7],
    #     [0, 0, 9, 0, 0, 1, 0, 6, 0],
    #     [6, 0, 0, 0, 9, 0, 0, 0, 0],
    #     [0, 4, 0, 3, 0, 0, 8, 1, 6],
    #     [0, 6, 0, 0, 0, 0, 0, 7, 0],
    #     [7, 9, 1, 0, 0, 8, 0, 4, 0],
    #     [0, 0, 0, 0, 2, 0, 0, 0, 1],
    #     [0, 5, 0, 8, 0, 0, 7, 0, 0],
    #     [1, 0, 0, 0, 3, 7, 2, 5, 9],
    # ]

    grid = [
        [0, 3, 4, 0],
        [4, 0, 0, 2],
        [1, 0, 0, 3],
        [0, 2, 1, 0],
    ]
    sqr_it = GridSquareIterator(grid)

    for col in sqr_it:
        print(col)