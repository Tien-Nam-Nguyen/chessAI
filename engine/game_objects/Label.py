import pygame as pg

from ..game_components import LabelRenderer
from ..game_components.label_renderer import LabelRenderConfig
from ..GameObject import GameObject


class Label(GameObject):
    def __init__(
        self,
        font: pg.font.FontType,
        label="Label",
        render_config: LabelRenderConfig | None = None,
        name="GameComponent:Label",
        active=True,
    ):
        super().__init__(name, active)
        self.label_componenet = LabelRenderer(font, label, render_config)
        self.add_component(self.label_componenet)
