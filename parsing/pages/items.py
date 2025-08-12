from bs4 import BeautifulSoup, Tag

from parser import Parser
from helpers import get_image_name


class ItemsParser(Parser):
    """Parser for Items page"""

    printers = ['Backpack', 'Small Printer', 'Medium Printer', 'Large Printer']

    def __init__(self, custom_url: str | None = None):
        super().__init__('Items', custom_url)

    def do_parse(self, soup: BeautifulSoup):
        """Parse the Items page."""

        tables = soup.select('table.darktable')

        items = []
        recipes = []

        table: Tag
        printer: str

        for table, printer in zip(tables[:-1], self.printers):   # Don't need other objects
            rows = table.select('tr')

            for row in rows[1:-1]:    # Skipping header and total
                item, recipe = self.process_row(row)

                items.append(item)

                if recipe:
                    recipe['station'] = printer
                    recipes.append(recipe)

        return {
            'items': items,
            'recipes': recipes
        }

    def process_row(self, row: Tag):
        """Process a table row and return the item and its recipe."""

        result, size, craft, byte_cost = row.select('td')

        icon = get_image_name(result.select('img')[0]['src'])
        name = result.text.strip()
        tier = size.text.strip()
        unlock = self.get_unlock(byte_cost.text.strip())
        materials = self.get_materials(craft)

        if materials:
            recipe = {
                'type': 'printing',
                'result': name,
                'materials': materials,
            }
        else:
            recipe = None

        return {
            'icon': icon,
            'name': name,
            'tier': tier,
            'unlock': unlock,
        }, recipe

    def get_unlock(self, byte_cost: str):
        """Make object that describes item unlocking method."""

        byte_cost = byte_cost.replace(',', '')

        try:
            return {
                'bytes': int(byte_cost)
            }
        except ValueError:
            if byte_cost == 'Unlocked':
                return {
                    'bytes': 0
                }
            elif byte_cost == 'N/A':
                return None
            else:
                return {
                    'mission': byte_cost
                }

    def get_materials(self, craft: Tag):
        """Get object's list of materials."""

        if 'N/A' in craft.text or 'Missions' in craft.text:
            return None

        if len(craft) == 2:
            material, _ = craft
            materials = [material.text.strip()]

        elif len(craft) % 3 == 0:
            materials = []

            while craft:
                count, material, _, *craft = craft
                count = int(count.text.strip()[0])
                materials.extend([material.text.strip()] * count)

        else:
            print('Bad line:', craft)
            return None

        return materials
