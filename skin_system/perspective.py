from skinpy import Skin, Perspective
from skin_system import convert_skin


def perspective(skin_image, scale_factor, y, z):
    if skin_image.size != (64, 64):
        skin_image = convert_skin(skin_image)

    skin = Skin.from_image(skin_image)

    perspective = Perspective(
        x="left",
        y=y,
        z=z,
        scaling_factor=scale_factor
    )

    return skin.to_isometric_image(perspective)
