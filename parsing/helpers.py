import re


def get_image_name(image_url: str) -> str:
    """Extract image name from url."""

    return re.search(r'/([^/]*\.png)/', image_url)[1]


def merge(left: list[dict], right: list[dict]):
    """Placeholder for actual content-aware merging of lists of dicts"""

    # TODO
    return left + right
