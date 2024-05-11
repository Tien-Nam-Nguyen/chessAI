from typing import Callable, Self
from pygame.rect import Rect
from pygame.mouse import get_pos, get_pressed

from ...GameComponent import GameComponent
from ...EventListener import EventListener
from .Events import ButtonEvents


class Button(GameComponent):
    def __init__(self, rect: Rect, name="Button", active=True):
        super().__init__(name, active)

        self.rect = rect
        self._event_listener = EventListener[ButtonEvents, [Self], None]()

        self._clicked = False
        self._entered = False

    @property
    def clicked(self):
        return self._clicked

    @property
    def entered(self):
        return self._entered

    def on(self, event: ButtonEvents, callback: Callable[[Self], None]):
        self._event_listener.on(event, callback)

    def once(self, event: ButtonEvents, callback: Callable[[Self], None]):
        self._event_listener.once(event, callback)

    def off(self, event: ButtonEvents, callback: Callable[[Self], None]):
        self._event_listener.off(event, callback)

    def update(self):
        mouse_pos = get_pos()
        colliding = self.rect.collidepoint(mouse_pos)
        pressing = get_pressed()[0]

        if colliding and pressing and not self._clicked and not self._entered:
            return

        if colliding and pressing and not self._clicked:
            self._clicked = True
            self._event_listener.emit(ButtonEvents.DOWN, self)
            return

        if colliding and not pressing and self._clicked:
            self._clicked = False
            self._event_listener.emit(ButtonEvents.UP, self)
            self._event_listener.emit(ButtonEvents.CLICK, self)
            return

        if not colliding and not pressing and self._clicked:
            self._clicked = False
            self._event_listener.emit(ButtonEvents.UP, self)
            return

        if colliding and not self._entered:
            self._entered = True
            self._event_listener.emit(ButtonEvents.ENTER, self)
            return

        if not colliding and self._entered:
            self._entered = False
            self._event_listener.emit(ButtonEvents.LEAVE, self)
