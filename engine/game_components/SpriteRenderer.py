import pygame as pg
from ..GameComponent import GameComponent


def rotate_with_anchor(
    image: pg.SurfaceType,
    position: tuple[float, float],
    angle: float,
):
    image_width, image_height = image.get_size()
    center = (image_width / 2, image_height / 2)

    # offset from pivot to center
    image_rect = image.get_rect(
        topleft=(position[0] - center[0], position[1] - center[1])
    )
    offset_center_to_pivot = pg.math.Vector2(position) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (
        position[0] - rotated_offset.x,
        position[1] - rotated_offset.y,
    )

    # get a rotated image
    rotated_image = pg.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image, rotated_image_rect


class SpriteRenderer(GameComponent):
    def __init__(self, image: pg.Surface, name="SpriteRenderer", active=True) -> None:
        super().__init__(name, active)
        self.image = image

    def update(self):
        position = self.game_object.transform.world_position
        scale = self.game_object.transform.world_scale
        rotation = self.game_object.transform.world_rotation

        surface = pg.transform.scale_by(self.image, scale)
        surface, o_pos = rotate_with_anchor(surface, position, rotation)

        self.game_object.game.screen.blit(
            surface,
            o_pos,
        )
