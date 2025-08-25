import re


def get_image_name(image_url: str) -> str:
    """Extract image name from url."""

    return re.search(r'/([^/]*\.png)/', image_url)[1]
