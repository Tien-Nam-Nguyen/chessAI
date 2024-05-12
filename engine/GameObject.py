from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from .Game import Game
    from .GameComponent import GameComponent

from .game_components import Transform


class GameObject:
    def __init__(self, name="GameObject", active=True) -> None:
        self.name = name
        self.game: "Game" | None = None
        self.active = active

        self.components: list["GameComponent"] = []
        self.parent: Self | None = None
        self.children: list[Self] = []

        transform = Transform()
        self.add_component(transform)
        self.transform = transform

    @property
    def active_in_hierarchy(self) -> bool:
        if self.game is None:
            return False

        if self.game.running is False:
            return False

        if self.active is False:
            return False

        if self.parent is not None:
            return self.parent.active_in_hierarchy

        return True

    def core_start(self):
        if self.active_in_hierarchy is False:
            return

        for children in self.children:
            children.core_start()

        for component in self.components:
            component.core_start()

        self.start()

    def core_update(self):
        if self.active_in_hierarchy is False:
            return

        for children in self.children:
            children.core_update()

        for component in self.components:
            component.core_update()

        self.update()

    def start(self):
        """Override this method to add custom logic when the GameObject is added to the game."""
        pass

    def update(self):
        """Override this method to add custom update logic."""
        pass

    def add_component(self, component: "GameComponent"):
        component.game_object = self
        self.components.append(component)

    def remove_component(self, component: "GameComponent"):
        self.components.remove(component)
        component.game_object = None

    def add_child(self, child: Self):
        if child.parent is not None:
            child.parent.remove_child(child)

        child.game = self.game
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Self):
        self.children.remove(child)
        child.game = None
        child.parent = None
