#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbit simulator script

Simulates the orbit of a small body around a much larger body.
The mass of the larger body in not considered. Uses a second-
order discrete aproximation for the body position over time.
"""

# Second-order model:
# deltaX[i+1] = deltaX[i] + (a[i]+a[i-1]) / 2
# deltaX[i]: body displacement at time i
# a[i]: body acceleration at time i

# Helping functions
from helpers import *

# generic imports
from decimal import *
from graphics import *
import time


__author__ = "Allan E. Feitosa"
__credits__ = "Raul O. Figueiredo"
__version__ = 1.0


def main() -> None:
    # Main code

    start: Decimal = Decimal(time.time())

    # constant parameters
    gravitational_constant: float = 1
    mass: float = 1
    UA: float = 1
    delta: float = 1.506e-3
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
        Point(star_position[0] + 400, star_position[1] + 100), radius=2
        )
    planet_1.setFill('white')
    planet_1.setOutline('white')
    planet_1_center = planet_1.getCenter()
    planet_1.draw(window)

    # Set and draw a second planet
    # (does not interact with the previous one)
    planet_2: Circle = Circle(
        Point(star_position[0] + 100, star_position[1]), radius=2
    )
    planet_2.setFill('blue')
    planet_2.setOutline('blue')
    planet_2_center = planet_2.getCenter()
    planet_2.draw(window)

    # Setting of initial conditions

    # Lists of the initial speedies (i = -1)
    planet_1_initial_speedy = [-1, -0]
    planet_2_initial_speedy = [0, 1.2]

    # Arrays of the initial positions (i = -1)
    # Using arrays makes calculations simpler
    planet_1_initial_position = UA * np.array([
            (planet_1_center.getX() - star_position[0])/100,
            (planet_1_center.getY() - star_position[1])/100,
        ])
    planet_2_initial_position = UA * np.array([
            (planet_2_center.getX() - star_position[0])/100,
            (planet_2_center.getY() - star_position[1])/100,
        ])

    # Arrays of positions
    # arg: [current position, previous position]
    planet_1_positions = np.array([planet_1_initial_position, [0, 0]])
    planet_2_positions = np.array([planet_2_initial_position, [0, 0]])

    # An initial displacement (deltaX[-1]) is needed to calculate the
    # acceleration in the first iteration (i = 0)
    planet_1_initial_displacement = np.array(planet_1_initial_speedy) * delta
    planet_2_initial_displacement = np.array(planet_2_initial_speedy) * delta
    # Array of displacements
    # arg: [next displacement, previous displacement]
    planet_2_displacements = np.array([planet_2_initial_displacement, [0, 0]])
    planet_1_displacements = np.array([planet_1_initial_displacement, [0, 0]])

    # an initial aceleration is needed because we are using a
    # second-order approximation for the body position
    planet_1_initial_aceleration = get_normalized_acceleration(
        planet_1_positions[0], star_radius) * acceleration_constant
    planet_2_initial_aceleration = get_normalized_acceleration(
        planet_2_positions[0], star_radius) * acceleration_constant
    # Array of accelerations
    # arg: [current acceleration, previous acceleration]
    planet_1_accelerations = [planet_1_initial_aceleration, [0, 0]]
    planet_2_accelerations = [planet_2_initial_aceleration, [0, 0]]

    # The total displacement is the accumulated displacement in
    # a given number of iterations, used to update
    # the window simulation: that can saves us much time!
    # Initially, the total displacement is the initial displacement
    planet_1_total_displacement = np.copy(planet_1_initial_displacement)
    planet_2_total_displacement = np.copy(planet_2_initial_displacement)

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

        # We calculate the body position 1000 times between window updates.
        # We take the position before the iterations:
        planet_1_previous_position = np.copy(planet_1_positions[0])
        planet_2_previous_position = np.copy(planet_2_positions[0])
        for i in range(0, 1000):
            # We update the previous values
            planet_1_positions[1] = planet_1_positions[0]
            planet_2_positions[1] = planet_2_positions[0]
            planet_1_accelerations[1] = planet_1_accelerations[0]
            planet_2_accelerations[1] = planet_2_accelerations[0]
            planet_1_displacements[1] = planet_1_displacements[0]
            planet_2_displacements[1] = planet_2_displacements[0]

            # We update the current values
            planet_1_positions[0] += planet_1_displacements[0]
            planet_2_positions[0] += planet_2_displacements[0]
            planet_1_accelerations[0] = get_normalized_acceleration(
                planet_1_positions[0], star_radius) * acceleration_constant
            planet_2_accelerations[0] = get_normalized_acceleration(
                planet_2_positions[0], star_radius) * acceleration_constant
            # We apply the second-order model:
            planet_1_displacements[0] += (planet_1_accelerations[0]
                                          + planet_1_accelerations[1]) / 2
            planet_2_displacements[0] += (planet_2_accelerations[0]
                                          + planet_2_accelerations[1]) / 2

        if get_module(planet_2_positions[0])[1] < star_radius:
            print("Planet 1 colided with the star!")
            break

        if get_module(planet_2_positions[0])[1] < star_radius:
            print("Planet 2 colided with the star!")
            break

        # The total displacement is final_position (the position
        # at i + 1000) minus initial_position (the position at i)
        planet_1_total_displacement = (planet_1_positions[0]
                                       - planet_1_previous_position)

        planet_2_total_displacement = (planet_2_positions[0]
                                       - planet_2_previous_position)

    # End of main code


main()
