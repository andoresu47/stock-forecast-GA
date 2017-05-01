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
            self.weights[i] = random.randint(-10, 10)

if __name__ == '__main__':
    c = Chromosome()
    c.set_random_weights()
    print c.weights
