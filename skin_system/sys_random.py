import random
import os
from .get_path import *


def random_def_skin():
    directory = get_path('default_skins/', '.')  # noqa: F405

    files = os.listdir(directory)
    png_files = [f for f in files if f.lower().endswith('.png')]

    if not png_files:
        return None

    random_png = random.choice(png_files)
    
    return os.path.join(directory, random_png)