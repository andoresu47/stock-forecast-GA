"""Genetic Algorithm module.

This module defines several elements from the genetic algorithm such as
population creation, next generation production and selection.

"""
import math
import random

import pandas as pd

from chromosome import Chromosome


def create_population(size):
    """Function to deal with the creation of an initial population.

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
    """Function to evaluate a chromosome's fitness.

    Args:
        chromosome (Chromosome): chromosome object to evaluate.
        path (str): path to data file.

    """

    success = 0
    fail = 0
    data = pd.read_csv(path, index_col='Date').values.tolist()
    weights = chromosome.weights

    for i in range(len(data) - 1):
        res = evaluate_sigmoid(weights, data[i])
        prc_diff = data[i + 1][3] - data[i][3]
        if (res == 1 and prc_diff >= 0) or (res == -1 and prc_diff < 0):
            success += 1
        else:
            fail += 1

    chromosome.set_fitness(success)


def evaluate_sigmoid(weights, values):
    """Function to evaluate a weighted sum as input for a sigmoid function.

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

    gamma = weighted_sum - 125000
    res = 1 - 1 / (1 + math.exp(gamma)) if gamma < 0 else 1 / (1 + math.exp(-1 * gamma))

    if res >= 0.5:
        return 1
    else:
        return -1


def crossover(chromosome1, chromosome2):
    """Function to generate children from two chromosomes via two point crossover.

    Args:
        chromosome1 (Chromosome): parent chromosome.
        chromosome2 (Chromosome): parent chromosome.

    Returns:
        list: child chromosomes list.

    """

    # Mutation probability
    p = 0.5
    cut1 = random.randint(0, 3)
    cut2 = random.randint(4, 6)
    child1 = Chromosome()
    child2 = Chromosome()

    for i in range(len(chromosome1.weights)):
        mut1 = random.uniform(0, 1)
        mut2 = random.uniform(0, 1)
        if mut1 <= p:
            # Mutation takes place
            child1.weights[i] = child1.weights[i] + random.randint(0, 10)
        else:
            if i < cut1:
                child1.weights[i] = chromosome1.weights[i]
            elif cut1 <= i < cut2:
                child1.weights[i] = chromosome2.weights[i]
            else:
                child1.weights[i] = chromosome1.weights[i]

        if mut2 <= p:
            # Mutation takes place
            child2.weights[i] = child2.weights[i] + random.randint(0, 10)
        else:
            if i < cut1:
                child2.weights[i] = chromosome2.weights[i]
            elif cut1 <= i < cut2:
                child2.weights[i] = chromosome1.weights[i]
            else:
                child2.weights[i] = chromosome2.weights[i]

    return [child1, child2]


def add_children(population):
    """Function to generate and append children to current population.

    Args:
        population (list): current chromosome population.

    """

    random.shuffle(population)
    mid = int(len(population) / 2)
    half1 = population[:mid]
    half2 = population[mid:]
    for i in range(mid):
        children = crossover(half1[i], half2[i])
        population.extend(children)


def evaluate_population(population, data_file):
    """Function to evaluate fitness for each chromosome in a population.

    Args:
        population (list): current chromosome population.
        data_file (str): path to data file.

    """

    for chromosome in population:
        evaluate_fitness(chromosome, data_file)


def select_fittest(population):
    """Function to select the fittest chromosomes from a given population

    Args:
        population (list): current chromosome population.

    """

    mid = int(len(population) / 2)
    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[:mid]


def optimize(initial_population, iterations, data_file):
    """Function to optimize weight vectors with a Genetic Algorithm.

    Args:
        initial_population (int): Initial individuals amount.
        iterations (int): number of iterations.
        data_file (str): path to data file.

    Returns:
        list: population from last iteration.

    """

    population = create_population(initial_population)

    for i in range(iterations):
        add_children(population)
        evaluate_population(population, data_file)
        population = select_fittest(population)
        print "Finished iteration " + str(i + 1)

    return population


def get_optimal(population):
    """Function to get the optimal individual from a list of individuals.

    Args:
        population (list): List of individuals.

    Returns:
        Chromosome: optimal individual.

    """

    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[0]


if __name__ == '__main__':
    training_data = "Data_Sets\\MSFT_training.csv"
    testing_data = "Data_Sets\\MSFT_testing.csv"

    optimal = get_optimal(optimize(100, 20, training_data))
    print "Training set: " + optimal.to_string()
    evaluate_fitness(optimal, testing_data)
    print "Testing set: " + optimal.to_string()
