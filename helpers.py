import math
from typing import List
from classes import vetor


def calc_acel(corpo, o_corpos) -> List[float]:
    """ (corpo_celeste, list) -> vetor
    Calcula o vetor aceleração de um objeto do tipo `corpo_celeste`,
    a partir da força sobre si resultante das interações com outros corpos
    celestes em sua proximidade.
    """
    gravitational_const: float = 1e-4
    position_module: float = get_module(positions)
    accelerations: List[float] = []
    coordinate: float
    for coordinate in positions:
        accelerations.append(
            - coordinate * (
                gravitational_const * mass /
                position_module ** 3
            ) ** (1 / 2)
        )
    return accelerations


# def get_module(vector: List[float]) -> float:
#     """Calculates the norm of a vector."""
#     square_module = 0
#     for coordinate in vector:
#         square_module += coordinate ** 2
    # return square_module ** (1 / 2)
