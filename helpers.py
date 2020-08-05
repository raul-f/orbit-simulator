"""Helping functions for the orbit simulator"""

# general imports
import math
from typing import List
import numpy as np

__author__ = "Allan E. Feitosa"
__credits__ = "Raul O. Figueiredo"
__version__ = 1.0


def get_normalized_acceleration(
   position: List[float]) -> np.ndarray:
    """Returns an array of the particle's normalized acceleration
    vector,from its position vector relative to the larger body
    and the mass of the larger body."""
    position_module: List[float] = get_module(position)
    normalized_acceleration: List[float] = []
    coordinate: float
    for coordinate in position:
        normalized_acceleration.append(
            - coordinate / (position_module[0] * position_module[1])
        )
    return np.array(normalized_acceleration)


def get_module(vector: List[float]) -> List[float]:
    """Returns the square of vector module at position 0
    and the vector module at position 1."""
    square_module = 0
    for coordinate in vector:
        square_module += coordinate ** 2
    return [square_module, square_module ** (1 / 2)]