from parser import Parser
from pages.items import ItemsParser

parsers: list[Parser] = [
    ItemsParser(),  # Printed (mostly) items and their recipes

    # TODO
    Parser('Resources'),        # Resources and where to find them
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


for parser in parsers:
    try:
        parser.parse()
        print(f'{parser.name} parser is done')
    except NotImplementedError:
        print(f'{parser.name} parser is not implemented')
