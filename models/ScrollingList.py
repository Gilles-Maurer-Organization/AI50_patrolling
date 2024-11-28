from models.algorithms.AlgorithmModel import AlgorithmModel

class ScrollingList:
    def __init__(self, algorithms: list[AlgorithmModel]) -> None:
        self.active = False
        self.algorithms = algorithms
        self.selected_algorithm = None

    def get_algorithms(self) -> list[AlgorithmModel]:
        return self.algorithms
    
    def set_selected_algorithm(self, algorithm: AlgorithmModel) -> None:
        self.selected_algorithm = algorithm

    def get_selected_algorithm(self) -> AlgorithmModel:
        return self.selected_algorithm
    
    def has_an_algorithm_selected(self) -> bool:
        return self.selected_algorithm is not None