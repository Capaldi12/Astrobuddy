import json

from merging import merge
from parser import Parser
from pages.items import ItemsParser
from pages.resources import ResourcesParser


parsers: list[Parser] = [
    ResourcesParser(),    # Resources and where to find them
    ItemsParser(),  # Printed (mostly) items and their recipes

    # TODO
    Parser('Soil_Centrifuge'),  # Centrifuge recipes
    Parser('Scrap'),            # Item scrap values
    Parser('Trade_Platform'),   # Trading recipes
    Parser('Bytes'),            # Byte values for resources
    Parser('Power'),            # Power production, consumption and storage
    Parser('Planets'),          # Planets, resources, power, gateways
    Parser('Widgets'),          # Which items are widgets
    Parser('Platforms'),        # Attachment slots and power connectors

    # TODO Anything else?
    # Backpack, Terrain tool?
]


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

END = '\033[0m'
BOLD = '\33[1m'
ITALIC = '\33[3m'


def main():
    data = []

    for parser in parsers:
        try:
            data.append(parser.parse())
            print(
                f'{GREEN}{BOLD}{ITALIC}{parser.name}:{END} done'
            )
        except NotImplementedError:
            print(
                f'{YELLOW}{BOLD}{ITALIC}{parser.name}:{END} not implemented'
            )
        except Exception as e:
            print(
                f'{RED}{BOLD}{ITALIC}{parser.name}:{END} error - {e}'
            )

    merged_data = merge(*data)

    # TODO tagging

    final_data = merged_data

    with open('output/data.json', 'w', encoding='utf-8') as file:
        json.dump(final_data, file, indent=4)


if __name__ == '__main__':
    main()
