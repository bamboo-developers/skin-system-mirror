import os

def get_path(file, ext=None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'{ext}'))
    return os.path.join(base_dir, file)