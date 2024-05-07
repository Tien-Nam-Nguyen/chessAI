import pygame as pg
from ..GameObject import GameObject
from ..game_components import SpriteRenderer


class Sprite(GameObject):
    def __init__(self, image: pg.Surface, name="Sprite", active=True) -> None:
        super().__init__(name, active)
        self.sprite = SpriteRenderer(image)
        self.add_component(self.sprite)
