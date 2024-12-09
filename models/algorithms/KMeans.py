from models.TextBox import TextBox
from models.algorithms.AlgorithmModel import AlgorithmModel

class KMeans(AlgorithmModel):
    def __init__(self) -> None:
        super().__init__()

        self.parameters = {
            # "Alpha": TextBox(str(alpha)),
            # "Beta": TextBox(str(beta)),
            # "Rho": TextBox(str(p)),
            # "Tau": TextBox(str(t))
        }

        self.name = "K-Means Algorithm"