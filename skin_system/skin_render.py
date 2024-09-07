from PIL import Image
from .convert import *


def process(skin_image, scale_factor, body_type, need_layer):
    if body_type != 'body':
       return process_minecraft_head(skin_image, scale_factor, need_layer)
    else:
       return process_minecraft_skin(skin_image, scale_factor, need_layer)

def process_minecraft_skin(skin_image, scale_factor, need_layer):
    if skin_image.size != (64, 64):
        skin_image = convert_skin(skin_image)

    head_size = 8 * scale_factor
    body_width, body_height = 8 * scale_factor, 12 * scale_factor
    arm_leg_width, arm_leg_height = 4 * scale_factor, 12 * scale_factor
    canvas = Image.new('RGBA', (2 * arm_leg_width + body_width, head_size + body_height + arm_leg_height), (0, 0, 0, 0))
    head = skin_image.crop((8, 8, 16, 16)).resize((head_size, head_size), Image.NEAREST)  # Голова
    body = skin_image.crop((20, 20, 28, 32)).resize((body_width, body_height), Image.NEAREST)  # Туловище
    arm_left = skin_image.crop((36, 52, 40, 64)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)  # Левая рука
    arm_right = skin_image.crop((44, 20, 48, 32)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)  # Правая рука
    leg_left = skin_image.crop((20, 52, 24, 64)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)  # Левая нога
    leg_right = skin_image.crop((4, 20, 8, 32)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)  # Правая нога


    canvas.paste(head, (arm_leg_width, 0))
    canvas.paste(body, (arm_leg_width, head_size))
    canvas.paste(arm_left, (0, head_size))
    canvas.paste(arm_right, (arm_leg_width + body_width, head_size))
    canvas.paste(leg_left, (arm_leg_width, head_size + body_height))
    canvas.paste(leg_right, (arm_leg_width + body_width - arm_leg_width, head_size + body_height))  # Перемещаем правую ногу левее ещё больше

    if need_layer == 1:
        head_layer = skin_image.crop((40, 8, 48, 16)).resize((head_size, head_size), Image.NEAREST)
        body_layer = skin_image.crop((20, 36, 28, 48)).resize((body_width, body_height), Image.NEAREST)
        arm_left_layer = skin_image.crop((52, 52, 56, 64)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)
        arm_right_layer = skin_image.crop((44, 36, 48, 48)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)
        leg_left_layer = skin_image.crop((4, 52, 8, 64)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)
        leg_right_layer = skin_image.crop((4, 36, 8, 48)).resize((arm_leg_width, arm_leg_height), Image.NEAREST)

        canvas.paste(head_layer, (arm_leg_width, 0), mask=head_layer)
        canvas.paste(body_layer, (arm_leg_width, head_size), mask=body_layer)
        canvas.paste(arm_left_layer, (0, head_size), mask=arm_left_layer)
        canvas.paste(arm_right_layer, (arm_leg_width + body_width, head_size), mask=arm_right_layer)
        canvas.paste(leg_left_layer, (arm_leg_width, head_size + body_height), mask=leg_left_layer)
        canvas.paste(leg_right_layer, (arm_leg_width + body_width - arm_leg_width, head_size + body_height), mask=leg_right_layer)

    return canvas

def process_minecraft_head(skin_image, scale_factor, need_layer):
    head_size = 8 * scale_factor

    head = skin_image.crop((8, 8, 16, 16)).resize((head_size, head_size), Image.NEAREST)  # Голова

    canvas = Image.new('RGBA', (head_size, head_size), (0, 0, 0, 0))
    canvas.paste(head, (0, 0))

    if need_layer == 1:
        head_layer = skin_image.crop((40, 8, 48, 16)).resize((head_size, head_size), Image.NEAREST)

        canvas.paste(head_layer, (0, 0), mask=head_layer)

    return canvas