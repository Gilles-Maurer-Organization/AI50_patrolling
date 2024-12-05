class GraphDataComplements:
    def __init__(
        self,         
        complete_adjacency_matrix: list[list[float]] = None,
        shortest_paths: dict[tuple[int, int], list[int]] = None
    ) -> None:
        self._complete_adjacency_matrix = complete_adjacency_matrix
        self._shortest_paths = shortest_paths

    @property
    def complete_adjacency_matrix(self) -> list[list[float]]:
        return self._complete_adjacency_matrix
    
    @property
    def shortest_paths(self) -> dict[tuple[int, int], list[int]]:
        return self._shortest_paths