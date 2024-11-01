from models.algorithms.Algorithm import Algorithm

class ScrollingList:
    def __init__(self, algorithms: list[Algorithm]) -> None:
        self.active = False
        self.algorithms = algorithms
        self.selected_algorithm = None

    def get_algorithms(self) -> list[Algorithm]:
        return self.algorithms
    
    def set_selected_algorithm(self, algorithm: Algorithm) -> None:
        self.selected_algorithm = algorithm

    def get_selected_algorithm(self) -> Algorithm:
        return self.selected_algorithm
    
    def has_an_algorithm_selected(self) -> bool:
        return self.selected_algorithm is not None