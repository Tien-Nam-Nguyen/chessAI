from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GameObject import GameObject


class GameComponent:
    def __init__(self, name="GameComponent", active=True) -> None:
        self.name = name
        self.game_object: "GameObject" | None = None
        self.active = active

    def core_update(self):
        if self.game_object is None:
            return

        if self.active is False:
            return

        self.update()

    def update(self):
        """Override this method to add custom update logic."""
        pass
