import pygame as pg
from ..GameComponent import GameComponent


class SpriteRenderer(GameComponent):
    def __init__(self, image: pg.Surface, name="SpriteRenderer", active=True) -> None:
        super().__init__(name, active)
        self.image = image

    def update(self):
        position = self.game_object.transform.position
        scale = self.game_object.transform.scale
        rotation = self.game_object.transform.rotation

        self.game_object.game.screen.blit(
            pg.transform.rotate(
                pg.transform.scale_by(self.image, scale),
                rotation,
            ),
            position,
        )
