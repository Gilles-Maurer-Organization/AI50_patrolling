from models.algorithms.AlgorithmModel import AlgorithmModel

class Naive(AlgorithmModel):
    def __init__(self):
        super().__init__()
        self.parameters = {}
        self.name = "Naive Algorithm"