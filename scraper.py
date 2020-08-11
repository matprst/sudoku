import requests
from bs4 import BeautifulSoup

class WebSudokuScraper:
    BASE_URL = "http://nine.websudoku.com/"
    EMPTY_CELL = 0
    def __init__(self):
        pass

    def get_grid(self, level=1):
        page = self._get_page(level)

        soup = BeautifulSoup(page.content, "html.parser")
        grid_elem = soup.find(id='puzzle_grid')

        grid = []
        for row_elem in grid_elem:
            _row = []

            for cell_elem in row_elem:
                try:
                    value = cell_elem.next_element['value']
                    _row.append(int(value))
                except KeyError:
                    _row.append(self.EMPTY_CELL)

            grid.append(_row)

        return grid

    def _get_page(self, level=1):
        level_param = f"level={level}"
        url = f"{self.BASE_URL}?{level_param}"
        page = requests.get(url)
        return page

if __name__ == "__main__":
    sudoku_grid = WebSudokuScraper().get_grid()

    for row in sudoku_grid:
        print(row)
