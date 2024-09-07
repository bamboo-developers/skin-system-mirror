from io import BytesIO

import requests
from PIL import Image


def resolv_skin(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))