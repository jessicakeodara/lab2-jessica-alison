#!/usr/bin/env python3

import math
import os.path
from collections import Counter


def H_approx(n):
    """
    Returns an approximate value of n-th harmonic number.
    http://en.wikipedia.org/wiki/Harmonic_number
    """
    # Euler-Mascheroni constant
    gamma = 0.57721566490153286060651209008240243104215933593992
    return gamma + math.log(n) + 0.5/n - 1./(12*n**2) + 1./(120*n**4)

def do_zipf_plot(counts, label=""):
    pass

def read_all(directory, extension=None):
    pass

def read_one(fname):
    pass

def plot_all(directory):
    counts = read_all(directory, ".txt")
    do_zipf_plot(counts, os.path.basename(directory))

def plot_one(fname):
    counts = read_one(fname)
    title = os.path.splitext(os.path.basename(fname))[0]

    do_zipf_plot(counts, label=title)

def main():
    plot_one('/cs/cs159/data/gutenberg/carroll-alice.txt')
    plot_all('/cs/cs159/data/gutenberg')


if __name__ == "__main__":
    main()
