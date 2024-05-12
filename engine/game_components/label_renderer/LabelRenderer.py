import pygame as pg

from ...GameComponent import GameComponent
from .RenderConfig import LabelRenderConfig
from ..utils.rotate_with_anchor import rotate_with_anchor


class LabelRenderer(GameComponent):
    def __init__(
        self,
        font: pg.font.FontType,
        label="Label",
        render_config: LabelRenderConfig | None = None,
        name="GameComponent:Label",
        active=True,
    ) -> None:
        super().__init__(name, active)

        self.label = label
        self.render_config = (
            LabelRenderConfig() if render_config is None else render_config
        )
        self.font = font

    def update(self):
        position = self.game_object.transform.world_position
        scale = self.game_object.transform.world_scale
        rotation = self.game_object.transform.world_rotation

        # render the label
        label_surface = self.font.render(
            self.label,
            self.render_config.anti_aliasing,
            self.render_config.color,
            self.render_config.background,
        )

        label_surface = pg.transform.scale_by(label_surface, scale)
        label_surface, o_pos = rotate_with_anchor(label_surface, position, rotation)
        label_surface.set_alpha(self.render_config.opacity)

        self.game_object.game.screen.blit(label_surface, o_pos)
