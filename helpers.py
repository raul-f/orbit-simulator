import math
from typing import List


def get_acceleration(positions: List[float], mass: float) -> List[float]:
    """Calculates a particle's acceleration vector, 
    from its position vector relative to the other body and the 
    mass of the other body."""
    gravitational_const: float = 0.00593
    position_module: float = get_module(positions)
    accelerations: List[float] = []
    coordinate: float
    for coordinate in positions:
        accelerations.append(
            - (coordinate / position_module) * (
                gravitational_const * mass /
                position_module ** 2
            )
        )
    return accelerations


def get_module(vector: List[float]) -> float:
    """Calculates the norm of a vector."""
    square_module = 0
    for coordinate in vector:
        square_module += coordinate ** 2
    return square_module ** (1 / 2)
