from scraper import WebSudoluScraper
import copy
import time
import sys

def is_valid(grid):
    return len(grid) == 9 and all(len(row) == 9 for row in grid)

def pretty_print(grid):
    print()
    for row in grid:
        print(row)
    print()

class Solver:
    SIZE = 9
    def __init__(self, grid):
        pass

    def solve(self, old_grid):
        grid = self._solve(old_grid)
        if self.is_solved(grid):
            # print()
            pretty_print(grid)
            # print()
            print('SOLVED')
        else:
            print('NOT SOLVED')

    def _solve(self, old_grid, tabs=0):
        grid = copy.deepcopy(old_grid)
        cell = self.get_empty_cell(grid)

        if cell is None:
            return grid

        row, col = cell

        for n in range(1, self.SIZE+1):
            # print()
            # pretty_print(grid)
            # print(row, col, n)
            # input()
            if self.is_valid(grid, row, col, n):
                # print(f'{row, col, n} VALID')
                grid[row][col] = n
                new_grid = self._solve(grid, tabs+1)
                if self.is_solved(new_grid):
                    return new_grid

            else:
                # print(f'{row, col, n} NOT-VALID')
                pass
                # print(row, col, n)
                # print('Not VALID')
        return grid

    # def _solve(self, old_grid, n):
    #     assert n < self.SIZE**2 # maximum SIZE * SIZE cells
    #     row = n // self.SIZE
    #     col = n % self.SIZE

    def get_empty_cell(self, grid):
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if grid[row][col] == 0:
                    return (row, col)
        return None

    def is_valid(self, grid, row, col, n):
        # print('check valid', row, col, n)
        if not self.row_is_valid(grid, row, col, n):
            # print('Row not valid')
            return False
        elif not self.column_is_valid(grid, row, col, n):
            # print('Col not valid')
            return False
        elif not self.square_is_valid(grid, row, col, n):
            # print('Square not valid')
            return False
        else:
            return True

    def row_is_valid(self, grid, row, col, n):
        row_nums = [n for n in grid[row] if n != 0]
        return n not in row_nums

    def column_is_valid(self, grid, row, col, n):
        # print('check column valid', row, col, n)
        col_nums = [grid[j][col] for j in range(self.SIZE) if grid[j][col] != 0]
        # print(col_nums)
        return n not in col_nums

    def square_is_valid(self, grid, row, col, n):
        row_square = row // int(self.SIZE**0.5)
        col_square = col // int(self.SIZE**0.5)
        # print('square')
        # print(row, col, n, row_square, col_square)
        for i in range(int(self.SIZE**0.5)):
            for j in range(int(self.SIZE**0.5)):
                if n == grid[row_square*int(self.SIZE**0.5)+i][col_square*int(self.SIZE**0.5)+j]:
                    return False
        return True

    def is_solved(self, grid):
        nums = list(range(1, self.SIZE+1))
        # check rows
        for row in grid:
            for n in nums:
                if n not in row:
                    return False

        # check columns
        for col in range(self.SIZE):
            column = [grid[row][col] for row in range(self.SIZE)]
            for n in nums:
                if n not in column:
                    return False

        # check squares
        for row in range(int(self.SIZE**0.5)):
            for col in range(int(self.SIZE**0.5)):
                square = [
                    grid[row*int(self.SIZE**0.5)][col*int(self.SIZE**0.5)],
                    grid[row*int(self.SIZE**0.5)][col*int(self.SIZE**0.5)+1],
                    grid[row*int(self.SIZE**0.5)][col*int(self.SIZE**0.5)+2],
                    grid[row*int(self.SIZE**0.5)+1][col*int(self.SIZE**0.5)],
                    grid[row*int(self.SIZE**0.5)+1][col*int(self.SIZE**0.5)+1],
                    grid[row*int(self.SIZE**0.5)+1][col*int(self.SIZE**0.5)+2],
                    grid[row*int(self.SIZE**0.5)+2][col*int(self.SIZE**0.5)],
                    grid[row*int(self.SIZE**0.5)+2][col*int(self.SIZE**0.5)+1],
                    grid[row*int(self.SIZE**0.5)+2][col*int(self.SIZE**0.5)+2]
                ]
                for n in nums:
                    if n not in square:
                        return False
        return True




grid = [
    [5, 2, 3, 6, 8, 0, 0, 0, 7],
    [0, 0, 9, 0, 0, 1, 0, 6, 0],
    [6, 0, 0, 0, 9, 0, 0, 0, 0],
    [0, 4, 0, 3, 0, 0, 8, 1, 6],
    [0, 6, 0, 0, 0, 0, 0, 7, 0],
    [7, 9, 1, 0, 0, 8, 0, 4, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 1],
    [0, 5, 0, 8, 0, 0, 7, 0, 0],
    [1, 0, 0, 0, 3, 7, 2, 5, 9],
]
parser = WebSudoluScraper()
grid = parser.get_grid(level=1)

# grid = [
#     [0, 3, 4, 0],
#     [4, 0, 0, 2],
#     [1, 0, 0, 3],
#     [0, 2, 1, 0],
# ]

pretty_print(grid)
# assert is_valid(grid)
t = time.time()
Solver(grid).solve(grid)
e = time.time()
print(e - t)
