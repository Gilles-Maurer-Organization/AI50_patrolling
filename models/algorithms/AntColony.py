from models.TextBox import TextBox
from models.algorithms.AlgorithmModel import AlgorithmModel

class AntColony(AlgorithmModel):
    def __init__(self, nb_iterations=100, alpha=0.1, beta=0.6, p=0.5, t=0.2) -> None:
        super().__init__()

        self.parameters = {
            "Alpha": TextBox(str(alpha)),
            "Beta": TextBox(str(beta)),
            "Rho": TextBox(str(p)),
            "Tau": TextBox(str(t))
        }

        self.name = "Ant Colony Algorithm"