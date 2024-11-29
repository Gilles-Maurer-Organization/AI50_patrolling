from models.algorithms.AlgorithmModel import AlgorithmModel
from models.TextBox import TextBox

class Evolutional(AlgorithmModel):
    def __init__(self, nb_iterations: int = 100, population_size: int = 10, nb_individuals: int = 10):
        super().__init__()

        # Dictionnaire pour stocker les paramètres et leurs étiquettes
        self.parameters = {
            "Number of iterations": TextBox(str(nb_iterations)),
            "Population size": TextBox(str(population_size)),
            "Number of individuals": TextBox(str(nb_individuals))
        }

        self.name = "Evolutional Algorithm"