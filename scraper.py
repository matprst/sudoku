import requests
from bs4 import BeautifulSoup


base_url = "https://www.websudoku.com/"
level_param = "level=1"
url = f"{base_url}?{level_param}"
url = "http://nine.websudoku.com/?level=1"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id='puzzle_grid')

print(results.prettify())

grid = []
for i, row_elem in enumerate(results):
    row = []

    for j, cell_elem in enumerate(row_elem):
        try:
            if cell_elem.next_element['value']:
                row.append(int(cell_elem.next_element['value']))
        except KeyError:
            row.append(0)

    grid.append(row)

for row in grid:
    print(row)
