from pygame.math import Vector2
import numpy as np
import math


def translation_matrix(vec: Vector2):
    matrix = np.array(
        [[1.0, 0.0, vec.x], [0.0, 1.0, vec.y], [0.0, 0.0, 1.0]], dtype=np.float32
    )

    def update(vec: Vector2):
        matrix[0, 2] = vec.x
        matrix[1, 2] = vec.y
        return matrix

    return matrix, update


def scale_matrix(vec: Vector2):
    matrix = np.array(
        [[vec.x, 0.0, 0.0], [0.0, vec.y, 0.0], [0.0, 0.0, 1.0]], dtype=np.float32
    )

    def update(vec: Vector2):
        matrix[0, 0] = vec.x
        matrix[1, 1] = vec.y
        return matrix

    return matrix, update


def rotation_matrix(rotation: float):
    rotation = math.radians(rotation)
    rotation = -rotation

    matrix = np.array(
        [
            [math.cos(rotation), -math.sin(rotation), 0.0],
            [math.sin(rotation), math.cos(rotation), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float32,
    )

    def update(rotation: float):
        rotation = math.radians(rotation)
        rotation = -rotation

        matrix[0, 0] = math.cos(rotation)
        matrix[0, 1] = -math.sin(rotation)
        matrix[1, 0] = math.sin(rotation)
        matrix[1, 1] = math.cos(rotation)
        return matrix

    return matrix, update


def affine_transform_matrix(translation: Vector2, scale: Vector2, rotation: float):
    tm, update_tm = translation_matrix(translation)
    sm, update_sm = scale_matrix(scale)
    rm, update_rm = rotation_matrix(rotation)

    intermediate_m = np.matmul(rm, sm, dtype=np.float32)
    affine_m: np.ndarray[np.float32] = np.matmul(tm, intermediate_m, dtype=np.float32)

    def update(
        translation: Vector2 | None = None,
        scale: Vector2 | None = None,
        rotation: float | None = None,
    ):
        should_update_tm = translation is not None
        should_update_sm = scale is not None
        should_update_rm = rotation is not None

        should_update_affine_m = (
            should_update_tm or should_update_sm or should_update_rm
        )

        if should_update_tm:
            update_tm(translation)

        if should_update_sm:
            update_sm(scale)

        if should_update_rm:
            update_rm(rotation)

        if should_update_affine_m:
            np.matmul(rm, sm, intermediate_m)
            np.matmul(tm, intermediate_m, affine_m)

        return affine_m

    temp_transform_in = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    temp_transform_out = np.array([0.0, 0.0, 1.0], dtype=np.float32)

    def transform(vec: Vector2, out: Vector2 | None = None):
        temp_transform_in[0] = vec.x
        temp_transform_in[1] = vec.y

        np.matmul(affine_m, temp_transform_in, temp_transform_out)

        if out is None:
            return Vector2(temp_transform_out[0], temp_transform_out[1])

        out.update(temp_transform_out[0], temp_transform_out[1])
        return out

    return affine_m, transform, update
