import time


from decimal import Decimal
from typing import List
from graphics import *
import math

from helpers import *
from classes import *


def main() -> None:
    start: Decimal = Decimal(time.time())
    # Main code

    u = vetor([1, 0])
    v = u[:]
    w = vetor([3, 4])

    v[1] = 1

    print(v)

    v += 3 * w

    print(v)
    print(w)


    sist_solar = [
        {
            'pos': vetor([600, 250]),
            'vel': vetor([12, 0]),
            'acel': vetor([0, 0]),
            'massa': 2e5
        },
        {
            'pos': vetor([600, 375]),
            'vel': vetor([0, 0]),
            'acel': vetor([0, 0]),
            'massa': 2e5
        }
    ]

    # End of main code
    end: Decimal = Decimal(time.time())
    execution_time: Decimal = round((end - start) * 1000, 3)
    print(
        f'This program took {execution_time} miliseconds ({execution_time / 1000} seconds) to run.'
    )

def simular(ccs, c, delta_t):
    '''(list, int, float) -> list
    RECEBE uma lista `ccs` de objetos do tipo `corpo_celeste`, um inteiro `c` e um tamanho de passo `delta_t`.
    
    CALCULA as mudanças de posição, velocidade e aceleração desses objetos por `c` ciclos e armazena a mudança de posição dada uma variação de tempo `delta_t` de cada corpo celeste por ciclo em um objeto correspondente do tipo `trajetoria`.

    RETORNA uma lista de objetos do tipo `trajetoria`.
    '''
    trajetorias = []
    copias = []

    for cc in ccs:
        trajetorias.append({ 'pos_ini': cc['pos'][:], 'deltas_s': []})
        copias.append(
            { 
                'pos': cc['pos'][:], 
                'vel': cc['vel'][:], 
                'acel': cc['acel'][:], 
                'massa': cc['massa']
            }
        )
    
    num_corpos = len(copias)

    for i in range(c):

        for j in range(num_corpos):
            trajetorias[j]['deltas_s'].append(copias[j]['vel'] * delta_t)

            copias[j]['pos'] += copias[j]['vel'] * delta_t

            if j < num_corpos - 1:
                copias[j]['acel'] = calc_acel(copias[j], copias[0:j] + copias[j + 1:len(copias)])
            else:
                copias[j]['acel'] = calc_acel(copias[0:j])

            copias[j]['vel'] += copias[j]['acel'] * delta_t

    return trajetorias

def animar():
    window_width: int = 1200
    window_height: int = 750

    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width, height=window_height
    )
    window.setBackground('#101010')

    planet_1: Circle = Circle(Point(600, 250), radius=1)
    planet_1.setFill('white')
    planet_1.setOutline('white')

    planet_1.draw(window)

    star: Circle = Circle(Point(600, 375), radius=10)
    star.setFill('#FDB813')
    star_center = star.getCenter()
    star_positions = [
        star_center.getX(),
        star_center.getY()
    ]

    star.draw(window)

    planet_1_speeds = [0.001, 0.01]

    i = 0
    while True:
        trajectory: Line = Line(
            Point(
                planet_1.getCenter().getX(),
                planet_1.getCenter().getY()
            ),
            Point(
                planet_1.getCenter().getX() + planet_1_speeds[0] * 0.05,
                planet_1.getCenter().getY() + planet_1_speeds[1] * 0.05
            ),
        )
        planet_1.move(planet_1_speeds[0] * 0.05, planet_1_speeds[1] * 0.05)
        trajectory.setOutline('#b7b7c2')
        trajectory.draw(window)
        planet_1_center = planet_1.getCenter()

        planet_1_positions = [
            planet_1_center.getX() - star_positions[0],
            planet_1_center.getY() - star_positions[1],
        ]

        planet_1_accelerarions = get_accelerations(planet_1_positions, 2e5)
        for i in range(0, 2):
            planet_1_speeds[i] += planet_1_accelerarions[i] * 0.05
        i += 1

        # print(planet_1_speeds)
        # time.sleep(0.01)

    window.getMouse()

main()
