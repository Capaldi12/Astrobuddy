from bs4 import BeautifulSoup

from parser import Parser
from helpers import get_image_name
from merging import merge


class ResourcesParser(Parser):
    """Parser for Resources page"""

    def __init__(self, custom_url: str | None = None):
        super().__init__('Resources', custom_url)

    def do_parse(self, soup):
        universal = self.get_universal(soup)
        planet_specific = self.get_planet_specific(soup)
        refined, refining_recipes = self.get_refined(soup)
        atmospheric = self.get_atmospheric(soup)
        composite, chemistry_recipes = self.get_composite(soup)
        special = self.get_special(soup)

        items = merge(
            universal,
            planet_specific,
            refined,
            atmospheric,
            composite,
            special,

            key='items'
        )
        recipes = merge(
            refining_recipes,
            chemistry_recipes,

            key='recipes'
        )

        return {
            'items': items,
            'recipes': recipes,
        }

    def get_universal(self, soup: BeautifulSoup):
        """Parse universal resources list"""

        data = []

        for dd in soup.select('dd'):
            data.append(self.get_item(dd) | {
                'tags': ['Natural'],
                'found_on': 'All',
            })

        return {item['name']: item for item in data}

    def get_planet_specific(self, soup: BeautifulSoup):
        """Parse planet-specific resources table"""

        table = soup.select('.darktable')[0]
        header, *rows = table.select('tr')

        planets = [planet.text.strip() for planet in header.select('th')[1:-1]]

        items = {}

        for row in rows:
            resource, *cols, _ = row.select('td')

            item = self.get_item(resource) | {
                'tags': ['Natural'],
                'found_on': [
                    planets[i]
                    for i, col in enumerate(cols)
                    if col.text.strip() == '✔️'
                ],
            }

            items[item['name']] = item

        return items

    def get_refined(self, soup: BeautifulSoup):
        """Parse refined resources table"""

        table = soup.select('.darktable')[1]
        rows = table.select('tr')[1:]

        items = {}
        recipes = []

        for row in rows:
            refined, raw = row.select('td')

            item = self.get_item(refined) | {'tags': ['Refined']}
            items[item['name']] = item

            raw_name = raw.text.strip()

            items[raw_name] = {'tags': ['Raw']}

            recipes.append({
                'result': item['name'],
                'type': 'refining',
                'materials': [raw_name],
            })

        return items, recipes

    def get_atmospheric(self, soup: BeautifulSoup):
        """Parse atmospheric resources table"""

        table = soup.select('.darktable')[2]
        header, *rows = table.select('tr')

        planets = [planet.text.strip() for planet in header.select('th')[1:]]

        items = {}

        for row in rows:
            resource, *cols = row.select('td')

            item = self.get_item(resource) | {
                'tags': ['Atmospheric'],
                'found_on': [
                    planets[i]
                    for i, col in enumerate(cols)
                    if col.text.strip() != '×'
                ],
            }

            # TODO PPU for planets

            items[item['name']] = item

        return items

    def get_composite(self, soup: BeautifulSoup):
        """Parse composite resources table"""

        table = soup.select('.darktable')[3]
        rows = table.select('tr')[1:]

        items = {}
        recipes = []

        for row in rows:
            composite, *materials = row.select('td')

            item = self.get_item(composite) | {'tags': ['Composite']}
            items[item['name']] = item

            recipes.append({
                'result': item['name'],
                'type': 'chemistry',
                'materials': [
                    mat.text.strip()
                    for mat in materials
                    if mat.text.strip() != 'n/a'
                ],
            })

        return items, recipes

    def get_special(self, soup: BeautifulSoup):
        """Parse special resources list"""

        ul = soup.select('.mw-body-content>div>ul')[0]

        items = {}

        for li in ul.select('li'):
            item = self.get_item(li) | {'tags': ['Special']}

            # We don't really need others
            if item['name'] in ['Scrap', 'EXO Chip']:
                items[item['name']] = item

        return items

    def get_item(self, element):
        """Get item data from page element"""

        return {
            'name': element.text.strip(),
            'icon': get_image_name(element.select('img')[0]['src']),
            'tier': 'Small',
        }
