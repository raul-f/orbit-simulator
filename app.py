import time
import math

from decimal import Decimal
from typing import List
from graphics import *
import math

from helpers import *
from classes import *


def main() -> None:
    start: Decimal = Decimal(time.time())
    # Main code

    sist_solar = [
        {
            'pos': vetor([1000, 250]),
            'vel': vetor([6, 0]),
            'acel': vetor([0, 0]),
            'massa': 2e10
        },
        {
            'pos': vetor([1200, 375]),
            'vel': vetor([-2, 0]),
            'acel': vetor([0, 0]),
            'massa': 2e16
        },
        {
            'pos': vetor([1100, 400]),
            'vel': vetor([0, -5]),
            'acel': vetor([0, 0]),
            'massa': 2e14
        }
    ]

    dados_sim = simular(sist_solar, int(1e5), 0.1)

    # End of main code
    end: Decimal = Decimal(time.time())
    execution_time: Decimal = round((end - start) * 1000, 3)
    print(
        f'This program took {execution_time} miliseconds ({execution_time / 1000} seconds) to run.'
    )

    animar(dados_sim)

def simular(ccs, c, delta_t):
    '''(list, int, float) -> dict
    RECEBE uma lista `ccs` de objetos do tipo `corpo_celeste`, um inteiro `c` e um tamanho de passo `delta_t`.
    
    CALCULA as mudanças de posição, velocidade e aceleração desses objetos por `c` ciclos e armazena a mudança de posição dada uma variação de tempo `delta_t` de cada corpo celeste por ciclo em um objeto correspondente do tipo `trajetoria`.

    RETORNA um dicionário com uma lista de objetos do tipo `trajetoria` e o número `c` de ciclos.
    '''
    trajetorias = { 'ciclos': c, 'trajs': []}
    copias = []

    for cc in ccs:
        trajetorias['trajs'].append(
            { 'pos_ini': cc['pos'][:], 'deltas_s': [], 'massa': cc['massa'] }
        )
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
            trajetorias['trajs'][j]['deltas_s'].append(copias[j]['vel'] * delta_t)

            copias[j]['pos'] += copias[j]['vel'] * delta_t

            if j < num_corpos - 1:
                outros = copias[0:j] + copias[j + 1:len(copias)]
            else:
                outros = copias[0:j]
            
            copias[j]['acel'] = calc_acel(copias[j], outros)
            copias[j]['vel'] += copias[j]['acel'] * delta_t

    return trajetorias

def animar(dados):
    window_width: int = 1920
    window_height: int = 1080

    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width, height=window_height
    )
    window.setBackground('#101010')

    corpos_c = []
    massa_min = dados['trajs'][0]['massa']

    for t in dados['trajs']:
        if t['massa'] < massa_min:
            massa_min = t['massa']

    for c, t in enumerate(dados['trajs']):
        print(math.log2(t['massa']) // math.log2(massa_min))
        corpos_c.append(Circle(Point(t['pos_ini'][0], t['pos_ini'][1]), radius=math.log2(t['massa']) // math.log2(massa_min)))
        corpos_c[-1].setFill(f'#aa{c * 3 % 10}')
        corpos_c[-1].setOutline(f'#aa{c * 3 % 10}')
        corpos_c[-1].draw(window)

    for i in range(dados['ciclos']):
        for j in range(len(corpos_c)):
            delta_s = dados['trajs'][j]['deltas_s'][i]

            trajectory = Line(
                Point(
                    corpos_c[j].getCenter().getX(),
                    corpos_c[j].getCenter().getY()
                ),
                Point(
                    corpos_c[j].getCenter().getX() + delta_s[0],
                    corpos_c[j].getCenter().getY() + delta_s[1]
                ),
            )

            trajectory.setOutline(f'#aa{j * 3 % 10}')

            corpos_c[j].move(delta_s[0], delta_s[1])

            trajectory.draw(window)

            time.sleep(0.001)

    window.getMouse()

main()
