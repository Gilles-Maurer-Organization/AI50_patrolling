from models.Algorithm import Algorithm
from models.TextBox import TextBox

class EvolutionalAlgorithm(Algorithm):
    def __init__(self, nb_iterations: int = 100, population_size: int = 10, nb_individuals = 10):
        super().__init__()
        self.nb_iterations = TextBox(str(nb_iterations))
        self.population_size = TextBox(str(population_size))
        self.nb_individuals = TextBox(str(nb_individuals))

        self.name = "Evolutional Algorithm"
        self.parameters = [self.nb_iterations, self.population_size, self.nb_individuals]