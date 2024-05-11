from pygame.math import Vector2

from ...GameComponent import GameComponent
from .affine import affine_transform_matrix


class Transform(GameComponent):
    def __init__(
        self,
        name="Transform",
        active=True,
        position: Vector2 | None = None,
        scale: Vector2 | None = None,
        rotation=0.0,
    ) -> None:
        super().__init__(name, active)

        self._position = position if position is not None else Vector2(0.0, 0.0)
        self._scale = scale if scale is not None else Vector2(1.0, 1.0)
        self._rotation = rotation

        self._transform_matrix, self._apply_transform, self._update_transform_matrix = (
            affine_transform_matrix(
                self._position,
                self._scale,
                self._rotation,
            )
        )

        self._world_position = Vector2(0.0, 0.0)
        self._world_scale = Vector2(1.0, 1.0)
        self._world_rotation = 0.0

    def start(self):
        self._update_transform_matrix(self._position, self._scale, self._rotation)

    @property
    def x(self) -> float:
        return self._position.x

    @x.setter
    def x(self, value: float):
        self._position.update(value, self._position.y)

        if self.active_in_hierarchy:
            self._update_transform_matrix(self._position)

    @property
    def y(self) -> float:
        return self._position.y

    @y.setter
    def y(self, value: float):
        self._position.update(self._position.x, value)

        if self.active_in_hierarchy:
            self._update_transform_matrix(self._position)

    @property
    def scale_x(self) -> float:
        return self._scale.x

    @scale_x.setter
    def scale_x(self, value: float):
        self._scale.update(value, self._scale.y)

        if self.active_in_hierarchy:
            self._update_transform_matrix(scale=self._scale)

    @property
    def scale_y(self) -> float:
        return self._scale.y

    @scale_y.setter
    def scale_y(self, value: float):
        self._scale.y = value

        if self.active_in_hierarchy:
            self._update_transform_matrix(scale=self._scale)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value

        if self.active_in_hierarchy:
            self._update_transform_matrix(rotation=self._rotation)

    @property
    def world_position(self):
        if self.game_object is None:
            self._world_position.update(self._position)
            return self._world_position

        if self.game_object.parent is None:
            self._world_position.update(self._position)
            return self._world_position

        parent_transform = self.game_object.parent.transform
        parent_transform._apply_transform(self._position, self._world_position)
        return self._world_position

    @property
    def world_scale(self):
        if self.game_object is None:
            self._world_scale.update(self._scale)
            return self._world_scale

        if self.game_object.parent is None:
            self._world_scale.update(self._scale)
            return self._world_scale

        parent_transform = self.game_object.parent.transform

        self._world_scale.update(
            self._scale.x * parent_transform.world_scale.x,
            self._scale.y * parent_transform.world_scale.y,
        )

        return self._world_scale

    @property
    def world_rotation(self) -> float:
        if self.game_object is None:
            self._world_rotation = self._rotation
            return self._world_rotation

        if self.game_object.parent is None:
            self._world_rotation = self._rotation
            return self._world_rotation

        parent_transform = self.game_object.parent.transform
        self._world_rotation = self._rotation + parent_transform.world_rotation
        return self._world_rotation
