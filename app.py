#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbit simulator script. Version 2.0

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
__version__ = 2.1


def main() -> None:
    # Main code

    # constant parameters
    gravitational_constant: float = 1
    star_mass: float = 1
    UA: float = 1
    delta: float = 1e-3
    star_radius: float = 0.2
    num_points = 100000
    points_inter = 100

    window_width: int = 1000
    window_height: int = 700

    # Constants to avoid calculating repeatedly
    gravitational_parameter = star_mass * gravitational_constant
    # acceleration_constant = gravitational_parameter * delta**2

    # New Classes

    class Star(Circle):
        def __init__(self, center: list, radius: float, mass: float,
                     color: str, outline: str):
            super().__init__(Point(center[0], center[1]), radius)
            self.center = center
            self.radius = radius
            self.color = color
            self.setFill(self.color)
            self.outline = outline
            self.setOutline(self.outline)

    class Planet(Circle):

        num_planets = 0
        planets = []

        def __init__(self, center: list, radius: float, mass: float,
                     color: str, outline: str):
            super().__init__(Point(center[0], center[1]), radius)
            self.center = center
            self.radius = radius
            self.mass = mass
            self.color = color
            self.setFill(self.color)
            self.outline = outline
            self.setOutline(self.outline)
            self.acceleration = []
            self.velocity = []
            self.position = []

            Planet.num_planets += 1
            Planet.planets.append(self)

    star = Star(
        [window_width/2, window_height/2], radius=100*star_radius,
        mass=star_mass, color='#FDB813', outline='#FDB813'
        )

    planet_1 = Planet(
        [star.center[0] - 50, star.center[1] + 100], radius=4, color='white',
        mass=0.001, outline='white')

    planet_2 = Planet(
       [star.center[0] + 50, star.center[1] - 100], radius=4, color='blue',
       mass=0.001, outline='blue')

    # Setting of initial relative position to the star

    planet_1.position.append(UA * np.array([
            (planet_1.center[0] - star.center[0])/100,
            (planet_1.center[1] - star.center[1])/100,
        ]))

    planet_2.position.append(UA * np.array([
            (planet_2.center[0] - star.center[0])/100,
            (planet_2.center[1] - star.center[1])/100,
        ]))

    # Initial speedies (i = -1)
    planet_1_initial_speedy = [1, 0]
    planet_2_initial_speedy = [-1, 0]

    # An initial displacement (deltaX[-1]) is needed to update the bodies
    # positions at the first iteration (i = 0)

    planet_1.velocity.append(np.array(planet_1_initial_speedy))
    planet_2.velocity.append(np.array(planet_2_initial_speedy))

    planets_force_constant = (planet_1.mass
                              * planet_2.mass
                              * gravitational_constant)

    # call the simulation routine
    start: Decimal = Decimal(time.time())
    simulation(num_points, Planet.planets, delta, gravitational_parameter,
               planets_force_constant)    
    end: Decimal = Decimal(time.time())
    simulation_time: Decimal = round((end - start) * 1000, 3)
    print(
        f'This program took {simulation_time} miliseconds ({simulation_time / 1000} seconds) to run.'
    )
    # call the animation routine
    animation(num_points, points_inter, Planet.planets, star, window_width,
              window_height)


def simulation(num_points: int, planets: list, delta: float,
               gravitational_parameter: float,
               planets_force_constant: float) -> None:
    """Executes the simulations from a list of planets"""
    delta_sqr = delta**2
    distance = np.zeros(2)
    for planet in planets:
        distance = -distance - planet.position[-1]
    for i in range(0, num_points):
        force = (planets_force_constant
                 * get_normalized_force(distance))

        distance = np.zeros(2)
        for planet in planets:
            # previous acceleration (a[i-1])
            planet.acceleration.append(
                force/planet.mass
                + get_normalized_acceleration(
                    planet.position[-1]) * gravitational_parameter)

            # intermediary step
            planet.position.append(
                planet.position[-1] + planet.velocity[-1]*delta
                + planet.acceleration[-1] * delta_sqr / 2)

            distance = -distance - planet.position[-1]
            force = -force

        inter_force = (planets_force_constant
                       * get_normalized_force(distance))
        distance = np.zeros(2)

        for planet in planets:
            inter_acceleration = (
                inter_force/planet.mass
                + get_normalized_acceleration(planet.position[-1])
                * gravitational_parameter)
            planet.velocity.append(
                planet.velocity[-1]
                + delta * (planet.acceleration[-1]
                           + inter_acceleration) / 2
            )
            planet.position[-1] = (planet.position[-2]
                                   + delta * (planet.velocity[-1]
                                              + planet.velocity[-2]) / 2)

            distance = -distance - planet.position[-1]
            inter_force = -inter_force


def animation(num_points: int, points_inter: int, planets: list, star,
              window_width: int, window_height: int) -> None:

    # Set the simulation window
    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width,
        height=window_height
    )
    window.setBackground('#101010')

    star.draw(window)
    for planet in planets:
        planet.draw(window)

    for i in range(0, num_points, points_inter):
        for planet in planets:
            delta_X = 100 * (planet.position[i + points_inter][0]
                             - planet.position[i][0])
            delta_Y = 100 * (planet.position[i + points_inter][1]
                             - planet.position[i][1])
            trajectory: Line = Line(
                Point(
                    planet.getCenter().getX(),
                    planet.getCenter().getY()
                ),
                Point(
                    planet.getCenter().getX() + delta_X,
                    planet.getCenter().getY() + delta_Y
                )
            )
            planet.move(delta_X, delta_Y)

            trajectory.setOutline(planet.outline)
            trajectory.draw(window)

        time.sleep(0.05)

    window.getMouse()

main()
