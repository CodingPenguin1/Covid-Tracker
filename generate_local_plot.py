#!/usr/bin/env python3
from sys import argv

from County import County
from generate_plots import generate_plot


if __name__ == '__main__':
    c = County(argv[1], argv[2])
    generate_plot(c, 'casesnew')
