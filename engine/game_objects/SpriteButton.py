from typing import NamedTuple
import pygame as pg
from tweener import Tween, Easing, EasingMode

from ..GameObject import GameObject
from ..game_components import Button as ButtonComponent, SpriteRenderer
from ..game_components.button import ButtonEvents


class SpriteButtonConfig(NamedTuple):
    image: pg.Surface
    rest_scale: float = 1.0
    hover_scale: float = 1.2
    pressed_scale: float = 1.3


class SpriteButton(GameObject):
    def __init__(
        self, config: SpriteButtonConfig, name="RectButton", active=True
    ) -> None:
        super().__init__(name, active)

        self.config = config
        self.sprite_renderer = SpriteRenderer(config.image)
        self.button_component = ButtonComponent(config.image.get_rect())

        self.add_component(self.sprite_renderer)
        self.add_component(self.button_component)

        self.transform.scale_x = config.rest_scale
        self.transform.scale_y = config.rest_scale

        self.setup_animation()

    def setup_animation(self):
        self._scale_tween: Tween | None = None

        self._current_scale = self.config.rest_scale
        self._start_scale = self.config.rest_scale
        self._end_scale = self.config.rest_scale

        def handle_down(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.pressed_scale

        def handle_up(button):
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
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
            self._scale_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._scale_tween.start()
            self._scale_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = self.config.rest_scale

        self.button_component.on(ButtonEvents.DOWN, handle_down)
        self.button_component.on(ButtonEvents.UP, handle_up)
        self.button_component.on(ButtonEvents.ENTER, handle_enter)
        self.button_component.on(ButtonEvents.LEAVE, handle_leave)

    def update(self):
        if self._scale_tween is None:
            return

        self._scale_tween.update()

        self._current_scale = (
            self._scale_tween.value * self._end_scale
            + (1 - self._scale_tween.value) * self._start_scale
        )

        self.transform.scale_x = self._current_scale
        self.transform.scale_y = self._current_scale

        position = self.transform.world_position
        scale = self.transform.world_scale
        image_rect = self.config.image.get_rect()

        self.button_component.rect.left = position.x - image_rect.width * scale.x / 2
        self.button_component.rect.top = position.y - image_rect.height * scale.y / 2
        self.button_component.rect.width = image_rect.width * scale.x
        self.button_component.rect.height = image_rect.height * scale.y
