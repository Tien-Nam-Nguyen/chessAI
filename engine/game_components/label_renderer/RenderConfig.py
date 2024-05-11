from typing import NamedTuple
from pygame.color import Color


class LabelRenderConfig(NamedTuple):
    color: Color = Color(0, 0, 0)
    background: Color | None = None
    opacity: int = 255
    anti_aliasing: bool = True
