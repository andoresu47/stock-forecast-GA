"""Genetic Algorithm module.

This module defines several elements from the genetic algorithm such as
population creation, next generation production and selection.

"""
import math
import pandas as pd

from chromosome import Chromosome


def create_population(size):
    """Method to deal with the creation of an initial population.

    Args:
        size (int): Size of the generated population.

    Returns:
        list: the generated population.

    """

    population_list = []
    for i in range(size):
        c = Chromosome()
        c.set_random_weights()
        population_list.append(c)

    return population_list


def evaluate_fitness(chromosome, path):
    """Method to evaluate a chromosome's fitness.

    Args:
        chromosome (Chromosome): chromosome object to evaluate.
        path (str): path to data file.

    """

    success = 0
    fail = 0
    data = pd.read_csv(path, index_col='Date').values.tolist()
    weights = chromosome.weights

    for i in range(len(data) - 2):
        res = evaluate_sigmoid(weights, data[i])
        prc_diff = data[i+1][3] - data[i][3]
        if (res == 1 and prc_diff >= 0) or (res == -1 and prc_diff < 0):
            success += 1
        else:
            fail += 1

    chromosome.set_fitness(success)


def evaluate_sigmoid(weights, values):
    """Method to deal with the creation of an initial population.

    Args:
        weights (list): weights to evaluate.
        values (list): values of distinct attributes.

    Returns:
        int: 1 if sigmoid evaluates to > 0.5,
            -1 otherwise.

    """

    weighted_sum = 0
    for (w, v) in zip(weights, values):
        weighted_sum += w * v

    gamma = weighted_sum - 200000
    res = 1 - 1/(1 + math.exp(gamma)) if gamma < 0 else 1/(1 + math.exp(-1 * gamma))

    if res >= 0.5:
        return 1
    else:
        return -1

if __name__ == '__main__':
    lst = create_population(10)
    # for l in lst:
    #     print l.weights

    path = "C:\\Users\\Andres\\Documents\\UNAM\\Ciencias de la Computacion\\6to semestre\\Inteligencia " \
           "Artificial\\ProyectoFinal\\Data\\MSFT.csv"

    evaluate_fitness(lst[0], path)
    print lst[0].weights
    print lst[0].fitness
