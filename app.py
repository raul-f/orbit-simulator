#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbit simulator script

Simulates the orbit of a small body around a much larger body. The mass of
the larger body in not considered. Uses the Heun's method discrete
aproximation for the body position over time.
"""
# We calculate the displacement at each algorithm iteration using the
# Heun's method:
# deltaX[i] = deltaX[i-1] + (deltaT**2)*(k_1 + k_2)/2
# deltaX[i] = X[i+1] - X[i] : body displacement between iterations i+1 and i
# X[i]: body position at time i
# deltaT : time step size
# k_1 = a[i-1] : body acceleration at time i-1
# k_2 : acceleration at position X_inter, obtained by the Euler's method as 
# X_inter = X[i] + deltaX[i-1] + (delta**2)*a[i-1]

# Helping functions
from helpers import *

# generic imports
from decimal import *
from graphics import *
import time


__author__ = "Allan E. Feitosa"
__credits__ = "Raul O. Figueiredo"
__version__ = 1.1.1


def main() -> None:
    # Main code

    start: Decimal = Decimal(time.time())

    # constant parameters
    gravitational_constant: float = 1
    mass: float = 1
    UA: float = 1
    delta: float = 1e-3
    star_radius: float = 0.1

    # Constants to avoid calculating repeatedly
    gravitational_parameter = mass * gravitational_constant
    acceleration_constant = gravitational_parameter * delta**2

    # Set the simulation window
    window_width: int = 800
    window_height: int = 600
    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width,
        height=window_height
    )
    window.setBackground('#101010')

    # Set and draw a star (large body)
    star: Circle = Circle(
        Point(window_width/2, window_height/2), radius=100*star_radius
        )
    star.setFill('#FDB813')
    star_center = star.getCenter()
    star_position = np.array([
        star_center.getX(), star_center.getY()]
        )
    star.draw(window)

    # Set and draw a planet (small body)
    planet_1: Circle = Circle(
        Point(star_position[0] - 100, star_position[1]), radius=2
        )
    planet_1.setFill('white')
    planet_1.setOutline('white')
    planet_1_center = planet_1.getCenter()
    planet_1.draw(window)

    # Set and draw a second planet
    # (does not interact with the previous one yet)
    planet_2: Circle = Circle(
        Point(star_position[0] + 50, star_position[1] + 50), radius=2
    )
    planet_2.setFill('blue')
    planet_2.setOutline('blue')
    planet_2_center = planet_2.getCenter()
    planet_2.draw(window)

    # Setting of initial conditions

    # Lists of the initial speedies (i = -1)
    planet_1_initial_speedy = [0, 1]
    planet_2_initial_speedy = [0, 1]

    # Arrays of (initial) position
    # Using numpy arrays makes calculations simpler
    planet_1_position = UA * np.array([
            (planet_1_center.getX() - star_position[0])/100,
            (planet_1_center.getY() - star_position[1])/100,
        ])
    planet_2_position = UA * np.array([
            (planet_2_center.getX() - star_position[0])/100,
            (planet_2_center.getY() - star_position[1])/100,
        ])

    # An initial displacement (deltaX[-1]) is needed to update the bodies
    # positions at the first iteration (i = 0)
    planet_1_displacement = np.array(planet_1_initial_speedy) * delta
    planet_2_displacement = np.array(planet_2_initial_speedy) * delta

    # The total displacement is the accumulated displacement in
    # a given number of iterations, used to update
    # the window simulation: that can saves us much time!
    # Initially, the total displacement is the initial displacement
    planet_1_total_displacement = np.copy(planet_1_displacement)
    planet_2_total_displacement = np.copy(planet_2_displacement)

    while True:
        # Trajectory Updates
        # At the first iteration (i = 0), we move the planets
        # accordingly to the initial displacements
        # Planet 1:
        trajectory_1: Line = Line(
            Point(
                planet_1.getCenter().getX(),
                planet_1.getCenter().getY()
            ),
            Point(
                planet_1.getCenter().getX()
                + 100*planet_1_total_displacement[0],
                planet_1.getCenter().getY()
                + 100*planet_1_total_displacement[1]
            ),
        )
        planet_1.move(
            100 * planet_1_total_displacement[0],
            100 * planet_1_total_displacement[1]
        )
        trajectory_1.setOutline('#b7b7c2')
        trajectory_1.draw(window)
        # Planet 2:
        trajectory_2: Line = Line(
            Point(
                planet_2.getCenter().getX(),
                planet_2.getCenter().getY()
            ),
            Point(
                planet_2.getCenter().getX()
                + 100*planet_2_total_displacement[0],
                planet_2.getCenter().getY()
                + 100*planet_2_total_displacement[1]
            ),
        )
        planet_2.move(
            100 * planet_2_total_displacement[0],
            100 * planet_2_total_displacement[1]
        )
        trajectory_2.setOutline('blue')
        trajectory_2.draw(window)

        # We calculate the body position a few times between window updates.
        # We take the position before the iterations:
        planet_1_previous_position = np.copy(planet_1_position)
        planet_2_previous_position = np.copy(planet_2_position)
        for i in range(0, 10):

            # previous positions accelerations (k_1 = a[i - 1])
            planet_1_acceleration = get_normalized_acceleration(
                planet_1_position) * acceleration_constant
            planet_2_acceleration = get_normalized_acceleration(
                planet_2_position) * acceleration_constant

            # We update the current positions
            planet_1_position += planet_1_displacement
            planet_2_position += planet_2_displacement

            # intermediary step (to obtain k_2)

            planet_1_inter_acceleration = get_Euler_acceleration(
                planet_1_displacement, planet_1_acceleration,
                planet_1_position, acceleration_constant)
            planet_2_inter_acceleration = get_Euler_acceleration(
                planet_2_displacement, planet_2_acceleration,
                planet_2_position, acceleration_constant)

            # displacements update
            planet_1_displacement += (planet_1_acceleration
                                      + planet_1_inter_acceleration) / 2
            planet_2_displacement += (planet_2_acceleration
                                      + planet_2_inter_acceleration) / 2

        if get_module(planet_1_position)[1] <= star_radius:
            print("Planet 1 colided with the star!")
            break
        if get_module(planet_2_position)[1] <= star_radius:
            print("Planet 2 colided with the star!")
            break

        # To update the window
        planet_1_total_displacement = (planet_1_position
                                       - planet_1_previous_position)

        planet_2_total_displacement = (planet_2_position
                                       - planet_2_previous_position)

    # End of main code


main()
