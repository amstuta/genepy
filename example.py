#!/usr/bin/env python3

import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from genetic.core import EvolutionaryAlgorithm


"""
Functions that can be used in the trees.
"""
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else 1


def compute_fitness(tree, features, data):
    """
    Computes a normalized MAE on the predictions made by one tree.
    """
    predicted = [tree.predict(feat) for feat in features]
    difference = [abs(predicted[i] - data[i]) for i in range(len(data))]
    mae = reduce(lambda a,b: a+b, difference) / len(data)
    fitness = 1 / mae if mae != 0 else 1.0
    fitness /= len(tree.nodes)
    return fitness


def train_test(meta):
    """
    Tests the algorithm on the f(x)=x**3 function and plots the results. Since
    there is no guaranty of finding an optimal solution, you may have to run it
    several times to observe good results.
    """
    features = [[x] for x in range(-100,100)]
    targets = [x**3 for x in range(-100,100)]
    functions = [add, sub, mul, div]
    ea = EvolutionaryAlgorithm(**meta, fitness_function=compute_fitness,
                                functions=functions)
    ea.fit(features, targets, meta['iterations'])
    print(ea.tree)

    x = np.arange(-10,10,0.1)
    predicted = [ea.predict([f]) for f in x]
    real = [f**3 for f in x]
    plt.plot(x, real, label='Real')
    plt.plot(x, predicted, label='Predicted')
    plt.legend()
    plt.show()


if __name__=='__main__':
    meta = {
        'min_depth':        2,
        'max_depth':        5,
        'nb_trees':         50,
        'max_const':        100,
        'func_ratio':       0.5,
        'var_ratio':        0.5,
        'crossover_prob':   0.8,
        'mutation_prob':    0.2,
        "iterations":       80
    }
    train_test(meta)
