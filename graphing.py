import matplotlib.pyplot as plt
from f_bidr import *
from f_bidr_data import get_orbit_file_path as orbit
import itertools

def get(records, *names):
    outputs = []
    for name in names:
        if callable(name):
            outputs.append([name(r) for r in records])
        else:
            outputs.append([r[name] for r in records])
            #return [r[name] for r in records]
    if len(names) == 1:
        return outputs[0]
    else:
        return outputs

def graph(records, *names, **axargs):
    stuff = get(records, *names)
    if len(names) == 1:
        plt.scatter(range(len(stuff)), stuff)
        ax = plt.gca()
        ax.set(xlabel='record #', ylabel=names[0])
    else:
        plt.scatter(stuff[0], stuff[1])
        ax = plt.gca()
        ax.set(xlabel=names[0], ylabel=names[1])
    if axargs:
        ax.set(**axargs)
    plt.show()