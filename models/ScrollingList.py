class ScrollingList:
    def __init__(self, text: str, algorithms: list[str]) -> None:
        self.active = False
        self.text = text
        self.algorithms = algorithms
        self.selected_algorithm = None

    def get_algorithms(self) -> list[str]:
        return self.algorithms
    
    def set_selected_algorithm(self, algorithm: str) -> None:
        self.selected_algorithm = algorithm

    def get_selected_algorithm(self) -> str:
        return self.selected_algorithm
    
    def has_an_algorithm_selected(self) -> bool:
        return self.selected_algorithm is not None