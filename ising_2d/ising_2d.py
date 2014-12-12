# /usr/bin/env python
# coding: utf-8
"""Simulate a 2-dimensional Ising paramagnet."""


import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
import picture
import random
import sys


__author__ = [
    'simoninoc@gmail.com (Simon Lin)',
    'dbarella@oberlin.edu (Dan Barella)',
    ]


# Constants
PROMPT = False


def randomCandidate(size):
    """Generate random candidate configuration of size*size."""
    playground=[]
    for i in range(size):
        playground.append([float(random.randint(0, 1)) for _ in range(size)])
    return playground


def all_spins_up(size):
    """Generate most energetic candidate configuration of size*size."""
    playground=[]
    for i in range(size):
        playground.append([1.0] * size)
    return playground


def checkerBoard(size):
    playground=[]
    for i in range(size):
        playground.append([])
        for j in range(size):
            if i%2 == 0:
                playground[i].append(1.0 if j%2==0 else -1.0)
            else:
                playground[i].append(-1.0 if j%2==0 else 1.0)
    return playground


def printlist(list):
    """Print candidate 2D list in letters."""
    for row in range(list):
        print(' '.join(row))


def dE(configuration, magnetic_field, i, j, interaction_energy=1):
    """Calculate the energy difference of flipping s(i, j)."""
    size = len(configuration)

    ua, ub = i - 1, j
    da, db = i + 1, j
    la, lb = i, j - 1
    ra, rb = i, j + 1

    if i == 0:
        ua = size - 1
    if i == size - 1:
        da = 0
    if j == 0:
        lb = size - 1
    if j == size - 1:
        rb = 0

    upNeighbour = configuration[ua][ub]
    downNeighbour = configuration[da][db]
    leftNeighbour = configuration[la][lb]
    rightNeighbour = configuration[ra][rb]

    neighbor_spins = (upNeighbour + downNeighbour
                      + leftNeighbour + rightNeighbour)

    # The 2 factor comes from flipping one spin
    deltaE = (
        2.0 * (configuration[i][j] * neighbor_spins * interaction_energy) + (
        (configuration[i][j] * interaction_energy * magnetic_field))
        )

    return deltaE


def total_E_M(configuration, magnetic_field, i, j, interaction_energy=1):
    """Calculate total energy and magnetization of a configuration."""
    tmp_energy = 0.0
    tmp_spin = 0.0

    for i, row in enumerate(configuration):
        for j, site in enumerate(row):
            tmp_energy += dE(configuration, magnetic_field, i, j,
                             interaction_energy)
            tmp_spin += site

    energy = -tmp_energy / (len(configuration)**2)
    magnetization = tmp_spin / (len(configuration)**2)

    return energy/2.0, magnetization


def setup_canvas(spin_array):
    """Set up the canvas and tile array.

    Args:
        spin_array (list of (list of int)): A two - dimensional array representing
        the spins of the paramagnet sites.

    Returns (tuple of picture.Picture, (list of (list of picture.Rectangle))):
    The setup canvas and tile array.
    """
    dimension = len(spin_array)

    canvas = picture.Picture(dimension*10, dimension*10)
    canvas.setFillColor(0, 0, 0)

    tiles=[]
    for i in range(len(spin_array)):
        tiles.append([])
        for j in range(len(spin_array[i])):
            tiles[i].append(None)
    for i in range(len(spin_array)):
        for j in range(len(spin_array[i])):
            tiles[i][j]=canvas.drawRectFill(i*10, j*10, 50, 50)
    for i in range(len(spin_array)):
        for j in range(len(spin_array[i])):
            if spin_array[i][j]==1:
                tiles[i][j].changeFillColor((255, 255, 255))

    return canvas, tiles


def flip_spin(spin_array, tiles, row, col):
    """Flips the spin at (row, col) in spin_array."""
    if spin_array[row][col] > 0:
        spin_array[row][col] = -1.0
        tiles[row][col].changeFillColor((0, 0, 0))
    else:
        spin_array[row][col] = 1.0
        tiles[row][col].changeFillColor((255, 255, 255))

    return spin_array


def update_line(line, y_point):
    """Updates a line with a new y-datapoint, incrementing x_data by one."""
    x_data, y_data = line.get_xdata(), line.get_ydata()

    line.set_xdata(np.append(x_data, len(x_data)))
    line.set_ydata(np.append(y_data, y_point))


def add_data(figure, data):
    """Adds a line of y-data to a figure."""
    ax, = figure.get_axes()
    line = lines.Line2D(
        [i for i in range(len(data))],
        data)

    ax.add_line(line)
    ax.relim()
    ax.autoscale()
    ax.autoscale_view()


def main():
    dimension = int(raw_input("Input size: "))
    temperature = float(raw_input("Temperature [ϵ/kB]: "))
    magnetic_field = float(raw_input("Magnetic Field [spin]: "))
    user_steps = int(raw_input("Steps: "))
    candidate = int(raw_input("Which candidate do you want to start with? "
        "[1: Random candidate, 2: All Spins Up, 3: Checkerboard]: "))
    if raw_input('Type "a" for Anti-Ferromagnetic, '
                 'otherwise ferromagnetic is assumed: ') == 'a':
        interaction_energy = -1.0
    else:
        interaction_energy = 1.0

    # Set up candidate
    if candidate == 1:
        spin_array = randomCandidate(dimension)
    elif candidate == 2:
        spin_array = all_spins_up(dimension)
    elif candidate == 3:
        spin_array = checkerBoard(dimension)
    else:
        print('Invalid candidate.')
        sys.exit(1)

    # Set up picture canvas
    canvas, tiles = setup_canvas(spin_array)
    canvas.display()

    # Set up plots
    energy_figure = plt.figure()
    energy_ax = energy_figure.add_subplot(1, 1, 1)
    energy_ax.set_title('Energy')
    energy_data = []

    magnetization_figure = plt.figure()
    magnetization_ax = magnetization_figure.add_subplot(1, 1, 1)
    magnetization_ax.set_title('Magnetization')
    magnetization_data = []

    # BEGIN THE MARKOV CHAIN
    for i in range(user_steps):
        #if PROMPT:
        print("Step {}".format(i))

        for j in range(dimension**2):
            row = random.randint(0, dimension - 1)
            col = random.randint(0, dimension - 1)
            deltaE = dE(spin_array, magnetic_field,
                        row, col, interaction_energy)

            if PROMPT:
                print("delta E = {}".format(deltaE))

            if deltaE <= 0:  # If flipping this spin decreases energy, flip it
                flip_spin(spin_array, tiles, row, col)
            else:
                # Otherwise the Boltzmann factor gives the probability of
                # flipping
                if temperature > 0:
                    boltzmann_factor = math.exp(-deltaE/temperature)
                else:
                    boltzmann_factor = 0.0

                rand = random.uniform(0, 1)
                if rand < boltzmann_factor:
                    if PROMPT:
                        print('Boltzmann factor: {}'.format(
                            math.exp(-deltaE/temperature)))

                    flip_spin(spin_array, tiles, row, col)

            canvas.display()

            energy, magnetization = total_E_M(spin_array, magnetic_field,
                                              row, col, interaction_energy)
            energy_data.append(energy)
            magnetization_data.append(magnetization)

            if PROMPT:
                print(energy, magnetization, entropy)

    add_data(energy_figure, energy_data)
    add_data(magnetization_figure, magnetization_data)

    plt.show(block=True)


if __name__ == '__main__':
    main()
