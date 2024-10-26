from models.TextBox import TextBox
from models.Algorithm import Algorithm

class AntColonyAlgorithm(Algorithm):
    def __init__(self, alpha=0.1, beta=0.6, p=0.5, t=0.2) -> None:
        super().__init__()

        self.parameters = {
            "Number of iterations:": TextBox(str(alpha)),
            "Population size": TextBox(str(beta)),
            "P": TextBox(str(p)),
            "T": TextBox(str(t))
        }

        self.name = "Ant Colony Algorithm"