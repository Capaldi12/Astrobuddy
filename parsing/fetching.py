import requests

from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}


def fetch_page(url: str, filename: str | None = None) -> str | None:
    """Download page and save it to input folder."""

    if filename is None:
        *_, name = url.split('/')
        filename = f'./input/{name}.html'

    result = requests.get(url, headers=headers)

    if result.status_code != 200:
        print(f'Error fetching {url}: {result.status_code}')
        return

    with open(filename, 'wb') as file:
        file.write(result.content)

    return filename


def get_soup(filename: str) -> BeautifulSoup:
    with open(filename, 'rb') as file:
        content = file.read()

    return BeautifulSoup(content, 'lxml')
