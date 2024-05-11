from pygame.rect import Rect
from pygame.color import Color
from pygame.draw import rect

from ..GameObject import GameObject


class Rectangle(GameObject):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Color,
        name="Rectangle",
        active=True,
    ):
        super().__init__(name, active)
        self.color = color
        self.rect = Rect(x - width / 2, y - height / 2, width, height)

    def update(self):
        rect(
            self.game.screen,
            self.color,
            self.rect,
        )
