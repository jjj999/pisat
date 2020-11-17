
import math

import numpy as np


def get_rot_mat2(theta: float) -> np.ndarray:
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos, -sin], [sin, cos]])


def get_rot_mat3x(theta: float) -> np.ndarray:
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[1, 0, 0], [0, cos, - sin], [0, sin, cos]])


def get_rot_mat3y(theta: float) -> np.ndarray:
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos, 0, sin], [0, 1, 0], [- sin, 0, cos]])


def get_rot_mat3z(theta: float) -> np.ndarray:
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos, - sin, 0], [sin, cos, 0], [0, 0, 1]])


def get_rot_mat3(theta: float, x: float, y: float, z: float) -> np.ndarray:
    axis = np.ndarray([x, y, z])
    axis = axis / abs(axis)
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([
        [cos + axis[0]**2 * (1 - cos), axis[0] * axis[1] * (1 - cos) - axis[2] * sin, axis[2] * axis[0] * (1 - cos) + axis[1] * sin],
        [axis[0] * axis[1] * (1 - cos) + axis[2] * sin, cos + axis[1]**2 * (1 - cos), axis[1] * axis[2] * (1 - cos) - axis[0] * sin],
        [axis[2] * axis[0] * (1 - cos) - axis[1] * sin, axis[1] * axis[2] * (1 - cos) + axis[0] * sin, cos + axis[2]**2 * (1 - cos)]
    ])
