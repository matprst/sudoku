from grid import Grid
from scraper import WebSudokuScraper

class Solver:
    SIZE = 9
    def __init__(self, grid=None):
        pass

    def solve(self, grid, tabs=0):
        cell = self.get_empty_cell(grid)

        if cell is None:
            return grid

        row, col = cell

        for n in range(1, self.SIZE+1):
            if self.is_valid(grid, row, col, n):
                grid.fill_cell(row, col, n)
                new_grid = self.solve(grid, tabs+1)
                if self.is_solved(new_grid):
                    return new_grid
                else:
                    grid.fill_cell(row, col, None)
        return grid

    def get_empty_cell(self, grid):
        for cell in grid:
            if cell.is_empty():
                return cell.position
        return None

    def is_valid(self, grid, row, col, n):
        return self.row_is_valid(grid, row, n) \
            and self.column_is_valid(grid, col, n) \
            and self.square_is_valid(grid, row, col, n)

    def row_is_valid(self, grid, row, n):
        row_nums = [cell.content for cell in grid[row] if not cell.is_empty()]
        return n not in row_nums

    def column_is_valid(self, grid, col, n):
        col_nums = [grid[j][col].content for j in range(self.SIZE) if not grid[j][col].is_empty()]
        return n not in col_nums

    def square_is_valid(self, grid, row, col, n):
        square_size = int(self.SIZE**0.5)
        row_square = row // square_size
        col_square = col // square_size

        for i in range(square_size):
            for j in range(square_size):
                if n == grid[row_square*square_size+i][col_square*square_size+j].content:
                    return False
        return True

    def is_solved(self, grid):
        nums = list(range(1, self.SIZE+1))
        # check rows
        for row in grid.rows():
            for n in nums:
                if n not in row:
                    return False

        # check columns
        for col in grid.columns():
            for n in nums:
                if n not in col:
                    return False
        
        # check squares
        for square in grid.squares():
            for n in nums:
                if n not in square:
                    return False
        return True

scraper = WebSudokuScraper()
sudoku_grid = Grid(scraper.get_grid())
print(sudoku_grid)

# grid = [
#     [0, 3, 4, 0],
#     [4, 0, 0, 2],
#     [1, 0, 0, 3],
#     [0, 2, 1, 0],
# ]
# grid = Grid(grid)

solver = Solver()
print(solver.solve(sudoku_grid))
