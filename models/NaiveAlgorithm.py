from models.Algorithm import Algorithm

class NaiveAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        self.parameters = []
        self.name = "Naive Algorithm"