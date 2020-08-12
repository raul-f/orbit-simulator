#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbit simulator script. Version 3.0

Simulates the orbit of astronomical bodies, using a process to approximate the bodies positions based on the Heun's method over time.
"""
# We calculate the displacement at each algorithm iteration using the
# following process, based on the Heun's method:
# Given
#     x[i-1] : previous body position, and
#     v[i-1] : previous body velocity at position x[i-1],
# we calculate the previous acceleration
#     a[i-1] = f(x[i-1]),
# where f is the corresponding function.
# Then, we estimate the current velocity as
#     v_est[i] = v[i-1] + deltaT*a[i-1],
# where deltaT is the time step.
# Then we apply the Heun's method to estimate the current position:
#     x_est[i] = x[i-1] + 0.5*deltaT*(v[-1] + v_est[i]),
# which can be reduced to
#     x_est[i] = x[i-1] + v[-1]*deltaT + 0.5*(deltaT**2)*a[-1].
# We now apply the method again to refine the current velocity and position.
# We estimate the new acceleration:
#     a_est[i] = f(x_est[i]),
# and apply the Heun's method in the velocity:
#     v[i] = v[-1] + 0.5*deltaT*(a[-1] + a_est[i]),
# which is our definite velocity estimate.
# Next, we use it to refine the current position:
#     x[i] = x[-1] + 0.5*deltaT*(v[-1] + v[i]),
# which completes the process for iteration i.

# Helping functions
from helpers import *

# generic imports
from decimal import *
from graphics import *
import time


__author__ = "Allan E. Feitosa"
__credits__ = "Raul O. Figueiredo"
__version__ = 3.0


def main() -> None:
    # Main code

    # constant parameters
    gravitational_constant: float = 1
    UA: float = 1
    delta: float = 1e-3
    num_points = 50000      # number of points of the simulation
    points_inter = 100      # interval between points used in animation

    window_width: int = 1000
    window_height: int = 700

    class Body(Circle):

        num_bodies = 0
        bodies = []

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

            Body.num_bodies += 1
            Body.bodies.append(self)

    body_0 = Body(
        center=[window_width/2, window_height/2+300],
        radius=20,
        mass=1,
        color='#FDB813',
        outline='#FDB813'
        )

    body_1 = Body(
        center=[window_width/2 + 200, window_height/2 + 300],
        radius=2,
        color='white',
        mass=0.001,
        outline='white')

    body_2 = Body(
        center=[window_width/2 + 100, window_height/2+300],
        radius=8,
        color='blue',
        mass=0.1,
        outline='blue')

    # Setting of initial relative position to the body_0

    body_0.position.append(UA * np.array([0, 0]))

    body_1.position.append(UA * np.array([
            (body_1.center[0] - body_0.center[0])/100,
            (body_1.center[1] - body_0.center[1])/100,
        ]))

    body_2.position.append(UA * np.array([
            (body_2.center[0] - body_0.center[0])/100,
            (body_2.center[1] - body_0.center[1])/100,
        ]))

    # Initial speedies (i = -1)
    body_0_initial_speedy = [0, 0]
    body_1_initial_speedy = [0, -0.8]
    body_2_initial_speedy = [0, -1]

    body_0.velocity.append(np.array(body_0_initial_speedy))
    body_1.velocity.append(np.array(body_1_initial_speedy))
    body_2.velocity.append(np.array(body_2_initial_speedy))

    bodies_masses = [body.mass for body in Body.bodies]

    # call the simulation routine
    body_0t: Decimal = Decimal(time.time())
    simulation(num_points, Body.bodies, delta, gravitational_constant,
               bodies_masses)
    end: Decimal = Decimal(time.time())
    simulation_time: Decimal = round((end - body_0t) * 1000, 3)
    print(
        f'This program took {simulation_time} miliseconds ({simulation_time / 1000} seconds) to run.'
    )
    # call the animation routine
    animation(num_points, points_inter, Body.bodies, window_width,
              window_height)


def simulation(num_points: int, bodies: list, delta: float,
               gravitational_constant: float,
               masses: float) -> None:
    """Executes the simulations from a list of bodys"""
    half_delta = delta / 2
    half_delta_sqr = delta**2 / 2
    num_bodies = bodies[0].num_bodies

    positions = []
    for body in bodies:
        positions.append(body.position[-1])

    for i in range(0, num_points):
        # previous acceleration (a[i-1])
        normd_acc_X = np.zeros((num_bodies, num_bodies))
        normd_acc_Y = np.zeros((num_bodies, num_bodies))
        for m in range(0, num_bodies):
            for n in range(m+1, num_bodies):
                normd_acc_X[m][n], normd_acc_Y[m][n] = get_normd_acceleration(
                    positions[m] - positions[n]
                )
                normd_acc_X[n][m] = -normd_acc_X[m][n]
                normd_acc_Y[n][m] = -normd_acc_Y[m][n]
        acc_X = (gravitational_constant
                 * np.dot(normd_acc_X, masses))
        acc_Y = (gravitational_constant
                 * np.dot(normd_acc_Y, masses))

        # intermediary step
        positions = []
        k = 0
        for body in bodies:
            acc = np.array([acc_X[k], acc_Y[k]])
            body.acceleration.append(acc)
            positions.append(
                body.position[-1] + body.velocity[-1]*delta
                + body.acceleration[-1] * half_delta_sqr
            )
            k += 1
        # new acceleration (a[i])
        normd_acc_X = np.zeros((num_bodies, num_bodies))
        normd_acc_Y = np.zeros((num_bodies, num_bodies))
        for m in range(0, num_bodies):
            for n in range(m+1, num_bodies):
                normd_acc_X[m][n], normd_acc_Y[m][n] = get_normd_acceleration(
                    positions[m] - positions[n]
                )
                normd_acc_X[n][m] = -normd_acc_X[m][n]
                normd_acc_Y[n][m] = -normd_acc_Y[m][n]
        acc_X = (gravitational_constant
                 * np.dot(normd_acc_X, masses))
        acc_Y = (gravitational_constant
                 * np.dot(normd_acc_Y, masses))

        k = 0
        for body in bodies:
            acc = np.array([acc_X[k], acc_Y[k]])
            body.velocity.append(
                body.velocity[-1]
                + half_delta*(body.acceleration[-1] + acc)
            )
            body.position.append(
                body.position[-1]
                + half_delta * (body.velocity[-1] + body.velocity[-2]))
            k += 1


def animation(num_points: int, points_inter: int, bodies: list,
              window_width: int, window_height: int) -> None:

    # Set the simulation window
    window: GraphWin = GraphWin(
        title="Orbit Simulator - phase 1", width=window_width,
        height=window_height
    )
    window.setBackground('#101010')

    for body in bodies:
        body.draw(window)

    for i in range(0, num_points, points_inter):
        for body in bodies:
            delta_X = 100 * (body.position[i + points_inter][0]
                             - body.position[i][0])
            delta_Y = 100 * (body.position[i + points_inter][1]
                             - body.position[i][1])
            trajectory: Line = Line(
                Point(
                    body.getCenter().getX(),
                    body.getCenter().getY()
                ),
                Point(
                    body.getCenter().getX() + delta_X,
                    body.getCenter().getY() + delta_Y
                )
            )
            body.move(delta_X, delta_Y)

            trajectory.setOutline(body.outline)
            trajectory.draw(window)

        time.sleep(0.05)

    window.getMouse()


main()
