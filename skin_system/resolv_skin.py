from io import BytesIO
import requests
from PIL import Image
from .sys_random import *
import os


def resolv_skin(url):
    response = None

    try:
        response = requests.get(url)
        response.raise_for_status()

        skin_image = Image.open(BytesIO(response.content))

        if skin_image.mode != 'RGBA':
            skin_image = skin_image.convert('RGBA')

        return skin_image

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            default_skin_path = random_def_skin()  # noqa: F405
            if not os.path.exists(default_skin_path):
                raise Exception("Default skin image not found")

            skin_image = Image.open(default_skin_path)

            if skin_image.mode != 'RGBA':
                skin_image = skin_image.convert('RGBA')

            return skin_image

        else:
            raise
