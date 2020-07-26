import time


from decimal import Decimal
from typing import List
from graphics import *
import math
import numpy as np

from helpers import *


def main() -> None:
    start: Decimal = Decimal(time.time())
    # Main code

    window_width: int = 800
    window_height: int = 600

    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width, height=window_height
    )
    window.setBackground('#101010')
 
    star: Circle = Circle(Point(window_width / 2, window_height / 2), radius=10)
    star.setFill('#FDB813')
    star_center = star.getCenter()
    star_position = np.array([
        star_center.getX(),
        star_center.getY()
    ])

    star.draw(window)

    planet_1: Circle = Circle(Point(star_position[0] + 50, star_position[1] - 50), radius=1)
    planet_1.setFill('white')
    planet_1.setOutline('white')
    planet_1_center = planet_1.getCenter()
    planet_1.draw(window)

    planet_1_initial_speedy = [0.1, 0]

    planet_1_initial_position = [
            (planet_1_center.getX() - star_position[0])/100,
            (planet_1_center.getY() - star_position[1])/100,
        ]

    # planet_1_anterior_positions = [
    #         planet_1_initial_positions[0] - planet_1_initial_speedy[0],
    #         planet_1_initial_positions[1] - planet_1_initial_speedy[1],
    #     ]   
    delta = 0.01

    anterior_position = list(np.array(planet_1_initial_speedy) * delta)
    planet_1_positions = np.array([anterior_position, planet_1_initial_position, [0, 0]])

    
    i = 0
    while True:

        planet_1_positions[2] += planet_1_positions[1]
        planet_1_positions[1] = planet_1_positions[0]
        planet_1_acceleration = get_acceleration(planet_1_positions[2], 1)
        print(planet_1_acceleration)
        planet_1_positions[0] += delta**2 * np.array(planet_1_acceleration)    

        trajectory: Line = Line(
            Point(
                planet_1.getCenter().getX(),
                planet_1.getCenter().getY()
            ),
            Point(
                planet_1.getCenter().getX() + 100 * planet_1_positions[0][0],
                planet_1.getCenter().getY() + 100 * planet_1_positions[0][1]
            ),
        )
        planet_1.move(100 * planet_1_positions[0][0], 100 * planet_1_positions[0][1])
        trajectory.setOutline('#b7b7c2')
        trajectory.draw(window)
        # planet_1_center = planet_1.getCenter()

        # planet_1_positions = [
        #     (planet_1_center.getX() - star_position[0])/100,
        #     (planet_1_center.getY() - star_position[1])/100,
        # ]

        # planet_1_accelerarions = get_accelerations(planet_1_positions, 1)
        # for i in range(0, 2):
        #     planet_1_speeds[i] += 100 * planet_1_accelerarions[i]
        # i += 1

        # print(planet_1_speeds)
        time.sleep(0.001)

    window.getMouse()

    # End of main code
    end: Decimal = Decimal(time.time())
    execution_time: Decimal = round((end - start) * 1000, 3)
    print(
        f'This program took {execution_time} miliseconds ({execution_time / 1000} seconds) to run.'
    )


main()
