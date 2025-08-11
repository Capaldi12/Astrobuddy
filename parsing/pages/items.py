import re
import json


from parser import Parser


class ItemsParser(Parser):
    printers = ['Backpack', 'Small Printer', 'Medium Printer', 'Large Printer']

    def __init__(self, custom_url: str | None = None):
        super().__init__('Items', custom_url)

    def parse(self):
        """Parse the Items page."""
        soup = self.get_soup()

        tables = soup.select('table.darktable')

        items = []
        recipes = []

        for table, printer in zip(tables[:-1], self.printers):   # Don't need other objects
            rows = table.select('tr')

            for row in rows[1:-1]:    # Skipping header and total
                item, recipe = self.process_row(row)

                items.append(item)

                if recipe:
                    recipe['station'] = printer
                    recipes.append(recipe)

        with open(self.output_filename, 'w', encoding='utf-8') as file:
            json.dump({'items': items, 'recipes': recipes}, file, indent=4)

    def process_row(self, row):
        """Process a table row and return the item and its recipe."""

        result, size, craft, byte_cost = row.select('td')

        icon = self.get_image_name(result.select('img')[0]['src'])
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

    def get_image_name(self, image_url):
        """Extract image name from url."""

        return re.search(r'/([^/]*\.png)/', image_url)[1]

    def get_unlock(self, byte_cost):
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
                    'Mission': 'TODO'
                }


    def get_materials(self, craft):
        """Get object that describes item's recipe."""

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
