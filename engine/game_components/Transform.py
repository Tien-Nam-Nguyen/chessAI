from pygame.math import Vector2
from ..GameComponent import GameComponent


class Transform(GameComponent):
    def __init__(
        self,
        name="Transform",
        active=True,
        position=Vector2(0.0, 0.0),
        scale=Vector2(1.0, 1.0),
        rotation=0.0,
    ) -> None:
        super().__init__(name, active)

        self.position = position
        self.scale = scale
        self.rotation = rotation
