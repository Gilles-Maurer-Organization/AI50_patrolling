from models.TextBox import TextBox
from models.Algorithm import Algorithm

class AntColonyAlgorithm(Algorithm):
    def __init__(self, alpha = 0.1, beta = 0.6, p = 0.5, t = 0.2) -> None:
        super().__init__()
        self.alpha = TextBox(str(alpha))
        self.beta = TextBox(str(beta))
        self.p = TextBox(str(p))
        self.t = TextBox(str(t))

        self.name = "Ant Colony Algorithm"
        self.parameters = [self.alpha, self.beta, self.p, self.t]

