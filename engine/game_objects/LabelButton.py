from typing import NamedTuple
import pygame as pg
from tweener import Tween, Easing, EasingMode

from ..GameObject import GameObject
from ..game_components import Button as ButtonComponent, SpriteRenderer, LabelRenderer
from ..game_components.button import ButtonEvents
from ..game_components.label_renderer import LabelRenderConfig


class LabelButtonConfig(NamedTuple):
    label_config: LabelRenderConfig
    rest_scale: float = 1.0
    hover_scale: float = 1.2
    pressed_scale: float = 1.3


class LabelButton(GameObject):
    def __init__(
        self,
        font: pg.font.FontType,
        label: str,
        config: LabelButtonConfig,
        name="LabelButton",
        active=True,
    ) -> None:
        super().__init__(name, active)

        self.config = config
        self.label_component = LabelRenderer(font, label, config.label_config)
        self.button_component = ButtonComponent(self.label_component.get_rect())

        self.add_component(self.label_component)
        self.add_component(self.button_component)

        self.transform.scale_x = self.config.rest_scale
        self.transform.scale_y = self.config.rest_scale

        self.setup_animation()

    def setup_animation(self):
        self._scale_tween: Tween | None = None

        self._current_scale = self.config.rest_scale
        self._start_scale = self.config.rest_scale
        self._end_scale = self.config.rest_scale

        self.transform.scale_x = self._current_scale
        self.transform.scale_y = self._current_scale

        def handle_down(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.pressed_scale

        def handle_up(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.EXPO, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.rest_scale

        def handle_enter(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.hover_scale

        def handle_leave(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.EXPO, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.rest_scale

        self.button_component.on(ButtonEvents.DOWN, handle_down)
        self.button_component.on(ButtonEvents.UP, handle_up)
        self.button_component.on(ButtonEvents.ENTER, handle_enter)
        self.button_component.on(ButtonEvents.LEAVE, handle_leave)

    def update(self):
        if self._scale_tween is not None:
            self._scale_tween.update()

            self._current_scale = (
                self._scale_tween.value * self._end_scale
                + (1 - self._scale_tween.value) * self._start_scale
            )

            self.transform.scale_x = self._current_scale
            self.transform.scale_y = self._current_scale

        position = self.transform.world_position
        scale = self.transform.world_scale
        rect = self.label_component.get_rect()

        self.button_component.rect.left = position.x - rect.width * scale.x / 2
        self.button_component.rect.top = position.y - rect.height * scale.y / 2
        self.button_component.rect.width = rect.width * scale.x
        self.button_component.rect.height = rect.height * scale.y
