from enum import Enum
import pygame

from grid import Grid
from scraper import WebSudokuScraper

class Color(Enum):
    DARK_BLUE = (50, 47, 61)
    DARK_GREY = (75, 93, 103)
    DARK_PURPLE = (135, 85, 111)
    GREEN = (0, 255, 127)

class Timer:
    def __init__(self):
        self.started = False
        self.start_time = 0
        self.last_time = 0
    
    def start(self):
        self.started = True
        self.start_time = pygame.time.get_ticks()
    
    def stop(self):
        self.started = False
    
    def time(self):
        if self.started:
            current_time = self._current_time()
            self.last_time = current_time
            return self._format_time(current_time)
        else:
            return self._format_time(self.last_time)

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
    SQUARE_THICKNESS = 5

    def __init__(self):
        self.end_game = True
        self.sudoku_scraper = WebSudokuScraper()
        self.grid = self._init_sudoku()
        self.selected_cell = None
        self.timer = Timer()
    
    def run(self):
        pygame.init()

        self.end_game = False
        self.timer.start()
        screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        while not self.end_game:
            for event in pygame.event.get():
                self.handle_event(event)
            
            screen.fill(Color.DARK_BLUE.value)
            self.draw_grid(screen)
            self.draw_timer(screen)

            if self.grid.is_solved():
                self.draw_solved(screen)
                self.timer.stop()
            
            pygame.display.update()
        
        pygame.quit()
    
    def draw_grid(self, screen):
        square_size = int(self.grid.size ** 0.5)
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(
                    screen, 
                    Color.DARK_GREY.value, 
                    (i*self.CELL_WIDTH*square_size, j*self.CELL_HEIGHT*square_size, self.CELL_WIDTH*square_size, self.CELL_HEIGHT*square_size), 
                    self.SQUARE_THICKNESS
                )
        
        for cell in self.grid:
            self.draw_cell(screen, cell)
    
    def draw_timer(self, screen):
        time = self.timer.time()
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(time, True, Color.GREEN.value)
        screen.blit(text, (460, 20))

    def draw_cell(self, screen, cell):
        col, row = cell.pos
        if not cell.is_fixed or (self.selected_cell and cell.pos == self.selected_cell.pos):
            color = Color.DARK_PURPLE.value
        else:
            color = Color.DARK_GREY.value
        
        pygame.draw.rect(
            screen, 
            Color.DARK_GREY.value, 
            (col*self.CELL_WIDTH, row*self.CELL_HEIGHT, self.CELL_WIDTH, self.CELL_HEIGHT), 
            self.CELL_THICKNESS
        )
        self.write_number(screen, cell.content, col, row, color)
    
    def draw_solved(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render("SOLVED", True, Color.GREEN.value)
        screen.blit(text, (145, 205))

    def write_number(self, screen, number, x, y, color):
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render(str(number) if number is not None else "", True, color)
        text_rect = text.get_rect()
        text_rect.center = (int((x+0.5)*self.CELL_WIDTH), int((y+0.5)*self.CELL_WIDTH))
        screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.end_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = self._cell_position(event.pos)
            if x < self.grid.size and y < self.grid.size:
                self.selected_cell = self.grid[x][y]
        elif event.type == pygame.KEYDOWN:
            key = event.unicode
            if key.isdigit() and not self.selected_cell.is_fixed: # fill digit
                x, y = self.selected_cell.pos
                self.grid.fill_cell(x, y, int(key))
            elif key == "\x08" and not self.selected_cell.is_fixed: # backspace, remove digit
                x, y = self.selected_cell.pos
                self.grid.fill_cell(x, y, "")
    
    def _cell_position(self, mouse_position):
        x, y = mouse_position
        return x // self.CELL_WIDTH, y // self.CELL_HEIGHT
    
    def _init_sudoku(self, level=1):
        grid = self.sudoku_scraper.get_grid(level)
        return Grid(grid)

if __name__ == "__main__":
    game = Game()
    game.run()
