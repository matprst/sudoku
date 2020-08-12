from enum import Enum
import pygame

from grid import Grid
from scraper import WebSudokuScraper

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

# class CellWrapper(Cell):
#     def __init__(self, row, col, content=None, color=1):
#         super().__init__(row, col, content)
#         self.color = color


class Game:
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 450
    CELL_WIDTH = 50
    CELL_HEIGHT = 50
    CELL_THICKNESS = 5

    def __init__(self):
        self.end_game = True
        self.sudoku_scraper = WebSudokuScraper()
        self.grid = self._init_sudoku()
        print(self.grid)
    
    def run(self):
        self.end_game = False
        screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        while not self.end_game:
            for event in pygame.event.get():
                self.handle_event(event)
            
            screen.fill(Color.WHITE.value)
            self.draw_grid(screen)

            pygame.display.update()
    
    def draw_grid(self, screen):
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, Color.BLACK.value, (i*self.CELL_WIDTH, j*self.CELL_HEIGHT, self.CELL_WIDTH, self.CELL_HEIGHT), self.CELL_THICKNESS)
                self.write_number(screen, self.grid[i][j].content, i, j)
    
    def write_number(self, screen, number, x, y):
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf = largeText.render(str(number) if number is not None else "", True, Color.BLACK.value)
        TextRect = TextSurf.get_rect()
        TextRect.center = (((x+0.5)*self.CELL_WIDTH), ((y+0.5)*self.CELL_WIDTH))
        screen.blit(TextSurf, TextRect)
    
    def handle_event(self, event):
        print(event)
        if event.type == pygame.QUIT:
            self.end_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(self._cell_position(event.pos))
    
    def _cell_position(self, mouse_position):
        x, y = mouse_position
        return x // self.CELL_WIDTH, y // self.CELL_HEIGHT
    
    def _init_sudoku(self, level=1):
        grid = self.sudoku_scraper.get_grid(level)
        return Grid(grid)

    




def cell_position(mouse_position):
    x, y = mouse_position
    return x // 50, y // 50

def main():
    pygame.init()
    game = Game()
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
