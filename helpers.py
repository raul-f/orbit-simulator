import math
from typing import List
from classes import vetor


def calc_acel(corpo, lst_corpos) -> List[float]:
    """ (corpo_celeste, list) -> vetor
    Calcula o vetor aceleração de um objeto do tipo `corpo_celeste`,
    a partir da força sobre si resultante das interações com outros corpos
    celestes na lista `lst_corpos`.
    """
    
    # Força resultante
    f_res = vetor([0] * corpo['acel'].dimensao)
    const_gravitacional: float = 1e-12

    for cc in lst_corpos:
        vetor_r =  cc['pos'] - corpo['pos']
        f_res += (const_gravitacional * corpo['massa'] * cc['massa'] / vetor_r.modulo() ** 3) * vetor_r

    return f_res * (1 / corpo['massa'])


# def get_module(vector: List[float]) -> float:
#     """Calculates the norm of a vector."""
#     square_module = 0
#     for coordinate in vector:
#         square_module += coordinate ** 2
    # return square_module ** (1 / 2)
