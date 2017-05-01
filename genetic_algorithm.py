"""Genetic Algorithm module.

This module defines several elements from the genetic algorithm such as
population creation, next generation production and selection.

"""

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

if __name__ == '__main__':
    lst = create_population(10)
    for l in lst:
        print l.weights
