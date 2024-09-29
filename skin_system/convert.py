from PIL import Image


def convert_skin(old_skin): #TODO fix convert as soon as possible

    if old_skin.size != (64, 32):
        raise ValueError("Old skin must be 64x32 pixels")

    new_skin = Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    new_skin.paste(old_skin.crop((0, 0, 64, 32)), (0, 0))
    new_skin.paste(old_skin.crop((0, 16, 16, 32)), (16, 48))
    new_skin.paste(old_skin.crop((40, 16, 56, 32)), (32, 48))

    old_skin.close()

    return new_skin