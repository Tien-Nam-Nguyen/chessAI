from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GameObject import GameObject


class GameComponent:
    def __init__(self, name="GameComponent", active=True) -> None:
        self.name = name
        self.game_object: "GameObject" | None = None
        self.active = active

    @property
    def active_in_hierarchy(self) -> bool:
        if self.game_object is None:
            return False

        return self.active and self.game_object.active_in_hierarchy

    def core_start(self):
        if self.active_in_hierarchy:
            self.start()

    def core_update(self):
        if self.active_in_hierarchy:
            self.update()

    def start(self):
        """Override this method to add custom start logic."""
        pass

    def update(self):
        """Override this method to add custom update logic."""
        pass
