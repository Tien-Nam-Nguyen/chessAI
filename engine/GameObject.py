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

    def core_update(self):
        if self.game is None:
            return

        if self.active is False:
            return

        for children in self.children:
            children.core_update()

        for component in self.components:
            component.core_update()

        self.update()

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
