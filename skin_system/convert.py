from PIL import Image

def convert_skin(old_skin: Image.Image) -> Image.Image:
    if old_skin.size != (64, 32):
        raise ValueError("Old skin must be 64x32 pixels")

    new_skin = Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    new_skin.paste(old_skin.crop((0, 0, 64, 32)), (0, 0))

    right_leg = old_skin.crop((4, 16, 8, 20))
    new_skin.paste(right_leg.transpose(Image.FLIP_LEFT_RIGHT), (20, 48))

    right_leg_front = old_skin.crop((4, 20, 8, 32))
    new_skin.paste(right_leg_front, (16, 52))

    right_arm = old_skin.crop((44, 16, 48, 20))
    new_skin.paste(right_arm.transpose(Image.FLIP_LEFT_RIGHT), (36, 48))

    right_arm_front = old_skin.crop((44, 20, 48, 32))
    new_skin.paste(right_arm_front, (32, 52))

    old_skin.close()
    return new_skin