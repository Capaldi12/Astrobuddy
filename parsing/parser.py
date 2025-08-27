import json
import os

from bs4 import BeautifulSoup

from fetching import fetch_page, get_soup


class Parser:
    """Base class for page parsers"""

    name: str   # Page and parser name
    custom_url: str | None  # Page url in case it differs from name

    def __init__(self, name: str, custom_url: str | None = None):
        self.name = name
        self.custom_url = custom_url

    @property
    def url(self) -> str:
        """Wiki page url."""

        return self.custom_url or f'https://astroneer.wiki.gg/wiki/{self.name}'

    @property
    def page_filename(self) -> str:
        """Filename for saving wiki page."""

        return f'./input/{self.name}.html'

    @property
    def output_filename(self) -> str:
        """Filename for output."""

        return f'./output/{self.name}.json'

    def fetch(self) -> str | None:
        """Fethces the page and saves it."""

        return fetch_page(self.url, self.page_filename)

    def get_soup(self) -> BeautifulSoup:
        """Get the soup of a page (fetch it, if it's not)."""

        if not os.path.exists(self.page_filename):
            self.fetch()

        return get_soup(self.page_filename)

    def parse(self, write=False) -> dict:
        """Parse the page."""

        data = self.do_parse(self.get_soup())

        if write:
            with open(self.output_filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

        return data

    def do_parse(self, soup: BeautifulSoup) -> dict:
        """Do the actual parsing"""

        raise NotImplementedError('Override this method!')
