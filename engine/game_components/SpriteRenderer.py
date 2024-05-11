import pygame as pg
from ..GameComponent import GameComponent
from .utils.rotate_with_anchor import rotate_with_anchor


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
