import time


from decimal import Decimal
from typing import List
from graphics import *
import math

from helpers import *


def main() -> None:
    print("Hello")
    start: Decimal = Decimal(time.time())
    # Main code

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

    planet_1_speeds = [7, 0]

    i = 0
    while True:
        trajectory: Line = Line(
            Point(
                planet_1.getCenter().getX(),
                planet_1.getCenter().getY()
            ),
            Point(
                planet_1.getCenter().getX() + planet_1_speeds[0],
                planet_1.getCenter().getY() + planet_1_speeds[1]
            ),
        )
        planet_1.move(planet_1_speeds[0], planet_1_speeds[1])
        trajectory.setOutline('#b7b7c2')
        trajectory.draw(window)
        planet_1_center = planet_1.getCenter()

        planet_1_positions = [
            planet_1_center.getX() - star_positions[0],
            planet_1_center.getY() - star_positions[1],
        ]

        planet_1_accelerarions = get_accelerations(planet_1_positions, 2e5)
        for i in range(0, 2):
            planet_1_speeds[i] += planet_1_accelerarions[i]
        i += 1

        # print(planet_1_speeds)
        time.sleep(0.05)

    window.getMouse()

    # End of main code
    end: Decimal = Decimal(time.time())
    execution_time: Decimal = round((end - start) * 1000, 3)
    print(
        f'This program took {execution_time} miliseconds ({execution_time / 1000} seconds) to run.'
    )


main()
