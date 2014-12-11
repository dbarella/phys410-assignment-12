# /usr/bin/env python
# coding: utf-8
"""Simulate a 2-dimensional Ising paramagnet."""


import math
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
        playground.append([])
        for j in range(size):
            dimension = random.randint(0, 1)
            if dimension == 0:
                playground[i].append(1)
            else:
                playground[i].append(-1)
    return playground


def mostEnergetic(size):
    """Generate most energetic candidate configuration of size*size."""
    playground=[]
    for i in range(size):
        playground.append([])
        for j in range(size):
            playground[i].append(1)
    return playground


def printlist(list):
    """Print candidate 2D list in letters."""
    for row in range(list):
        print(' '.join(row))


def dE(configuration, magnetic_field, i, j):
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
    deltaE = 2 * configuration[i][j] * neighbor_spins

    return deltaE


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
    if spin_array[row][col] == 1:
        spin_array[row][col] == -1
        tiles[row][col].changeFillColor((0, 0, 0))
    else:
        spin_array[row][col] == 1
        tiles[row][col].changeFillColor((255, 255, 255))


def main():
    dimension = int(raw_input("Input size: "))
    temperature = float(raw_input("Temperature [ϵ/kB]: "))
    magnetic_field = float(raw_input("Magnetic Field [spin]: "))
    user_steps = int(raw_input("Steps: "))
    candidate = int(raw_input("Which candidate do you want to start with? "
        "[1: Random candidate, 2: Most Energetic Candidate]: "))

    if candidate == 1:
        spin_array = randomCandidate(dimension)
    elif candidate == 2:
        spin_array = mostEnergetic(dimension)
    else:
        print('Invalid candidate.')
        sys.exit(1)

    canvas, tiles = setup_canvas(spin_array)
    canvas.display()

    # Candidate has already been constructed
    # BEGIN THE MARKOV CHAIN
    for i in range(user_steps):
        #if PROMPT:
        print("Step {}".format(i))

        for j in range(dimension**2):
            row = random.randint(0, dimension - 1)
            col = random.randint(0, dimension - 1)
            deltaE = dE(spin_array, magnetic_field, row, col)

            if PROMPT:
                print("delta E = {}".format(deltaE))

            if deltaE <= 0:  # If flipping this spin decreases energy, flip it
                flip_spin(spin_array, tiles, row, col)
            else:
                # Otherwise the Boltzmann factor gives the probability of
                # flipping
                rand = random.uniform(0, 1)
                if rand < math.exp(-deltaE/temperature):
                    if PROMPT:
                        print('Boltzmann factor: {}'.format(
                            math.exp(-deltaE/temperature)))

                    flip_spin(spin_array, tiles, row, col)

            canvas.display()

    raw_input('Hit enter to finish.')  # Lock the final canvas until the user hits enter


if __name__ == '__main__':
    main()
