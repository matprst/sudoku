from enum import Enum
import pygame

from grid import Grid
from scraper import WebSudokuScraper

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (255, 0, 0)
    DARK_BLUE = (50, 47, 61)
    DARK_GREY = (75, 93, 103)
    # DARK_PURPLE = (89, 64, 92)
    DARK_PURPLE = (135, 85, 111)
    GREEN = (0, 255, 127)

class Timer:
    def __init__(self):
        self.started = False
        self.start_time = 0
    
    def start(self):
        self.started = True
        self.start_time = pygame.time.get_ticks()
    
    def time(self):
        return self._format_time(self._current_time())

    def _current_time(self):
        current_time = pygame.time.get_ticks()
        total = current_time - self.start_time
        return total
    
    @staticmethod
    def _format_time(time_ms):
        time_h = time_ms // (1000*60*60)
        time_min = time_ms % (1000*60*60) // (1000*60)
        time_s = time_ms % (1000*60*60) % (1000*60) // (1000)
        return f"{time_h:02d}:{time_min:02d}:{time_s:02d}"

class Game:
    WINDOW_WIDTH = 635
    WINDOW_HEIGHT = 450
    CELL_WIDTH = 50
    CELL_HEIGHT = 50
    CELL_THICKNESS = 1

    def __init__(self):
        self.end_game = True
        self.sudoku_scraper = WebSudokuScraper()
        self.grid = self._init_sudoku()
        self.selected_cell = None
        self.timer = Timer()
    
    def run(self):
        self.end_game = False
        self.timer.start()
        screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        while not self.end_game:
            for event in pygame.event.get():
                self.handle_event(event)
            
            screen.fill(Color.DARK_BLUE.value)
            self.draw_grid(screen)
            self.draw_timer(screen)

            pygame.display.update()
    
    def draw_grid(self, screen):
        for cell in self.grid:
            self.draw_cell(screen, cell)
    
    def draw_timer(self, screen):
        time = self.timer.time()
        largeText = pygame.font.Font('freesansbold.ttf', 40)
        text = largeText.render(time, True, Color.GREEN.value)
        screen.blit(text, (460, 20))

    def draw_cell(self, screen, cell):
        x, y = cell.pos
        if self.selected_cell and cell.pos == self.selected_cell.pos:
            # color = Color.GREY.value
            color = Color.DARK_PURPLE.value
        else:
            # color = Color.BLACK.value
            color = Color.DARK_GREY.value
        # color = Color.BLACK.alue if cell.pos != self.selected_cell.pos else Color.GREY.value
        pygame.draw.rect(screen, color, (x*self.CELL_WIDTH, y*self.CELL_HEIGHT, self.CELL_WIDTH, self.CELL_HEIGHT), self.CELL_THICKNESS)
        self.write_number(screen, cell.content, x, y, color)

    def write_number(self, screen, number, x, y, color):
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf = largeText.render(str(number) if number is not None else "", True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (((x+0.5)*self.CELL_WIDTH), ((y+0.5)*self.CELL_WIDTH))
        screen.blit(TextSurf, TextRect)
    
    def handle_event(self, event):
        print(event)
        if event.type == pygame.QUIT:
            self.end_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = self._cell_position(event.pos)
            if x < 10 and y < 10:
                self.selected_cell = self.grid[x][y]
        elif event.type == pygame.KEYDOWN:
            key = event.unicode
            if key.isdigit() and not self.selected_cell.is_fixed:
                x, y = self.selected_cell.pos
                self.grid.fill_cell(x, y, int(key))
    
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
