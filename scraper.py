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
            row = []

            for cell_elem in row_elem:
                try:
                    value = cell_elem.next_element['value']
                    row.append(int(value))
                except KeyError:
                    row.append(self.EMPTY_CELL)

            grid.append(row)

        return grid

    def _get_page(self, level=1):
        level_param = f"level={level}"
        url = f"{self.BASE_URL}?{level_param}"
        page = requests.get(url)
        return page

if __name__ == "__main__":
    grid = WebSudoluScraper().get_grid()

    for row in grid:
        print(row)
