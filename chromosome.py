import random


class Chromosome:
    """Class to work with 6 gene chromosomes.

    A Chromosome object consists of a list of weights
    and a fitness parameter. A gene is an entry from the
    weights list.

    """

    def __init__(self):
        """Method to initialize class parameters.

        Weights list is set to size 6 and initialized with zeros.
        Fitness parameter is initially set to zero.

        """

        self.weights = [0] * 6
        self.fitness = 0

    def set_random_weights(self):
        """Method to set random values for this chromosome's genes.

        """

        for i in range(len(self.weights)):
            self.weights[i] = random.randint(0, 2000)

    def set_fitness(self, fitness):
        """Method to set the fitness of a chromosome.

        """

        self.fitness = fitness

    def to_string(self):
        """Method to get info from chromosome formatted as string.

        """

        return "w: " + str(self.weights) + ", f: " + str(self.fitness)

    def set_weights(self, weights):
        """Method to set weights from list parameter.

        """

        self.weights = weights

if __name__ == '__main__':
    c = Chromosome()
    c.set_random_weights()
    print c.weights
