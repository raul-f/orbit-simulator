"""Helping functions for the orbit simulator"""

# general imports
import math
from typing import List
import numpy as np

__author__ = "Allan E. Feitosa"
__credits__ = "Raul O. Figueiredo"
__version__ = 3.0


def get_normd_acceleration(
   distance: np.ndarray) -> np.ndarray:
    """Returns an array of the particle's normalized acceleration
    vector, from its position vector relative to another body"""
    distance_module = get_module(distance)
    normalized_acceleration = (-distance
                               / (distance_module[0] * distance_module[1]))

    return normalized_acceleration


def get_module(vector: np.ndarray) -> List[float]:
    """Returns the square of vector module at position 0
    and the vector module at position 1."""
    square_module = np.inner(vector, vector)
    return [square_module, square_module ** (1 / 2)]
