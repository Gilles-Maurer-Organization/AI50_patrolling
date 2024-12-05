from models.GraphDataComplements import GraphDataComplements


class GraphData:
    def __init__(
        self,
        nodes_list: list[tuple[int, int]] = None,
        adjacency_matrix: list[list[float]] = None,
        complete_adjacency_matrix: list[list[float]] = None,
        shortest_paths: dict[tuple[int, int], list[int]] = None
    ) -> None:
        self._nodes_list = nodes_list
        self._adjacency_matrix = adjacency_matrix
        self._complements = GraphDataComplements(
            complete_adjacency_matrix=complete_adjacency_matrix,
            shortest_paths=shortest_paths
        )
    
    @property
    def nodes_list(self) -> list[tuple[int, int]]:
        return self._nodes_list

    @property
    def adjacency_matrix(self) -> list[list[float]]:
        return self._adjacency_matrix
    
    @property
    def complements(self) -> GraphDataComplements:
        return self._complements
    
    @property
    def complete_adjacency_matrix(self) -> list[list[float]]:
        return self._complements.complete_adjacency_matrix
    
    @property
    def shortest_paths(self) -> dict[tuple[int, int], list[int]]:
        return self._complements._shortest_paths
    
    def all(
        self
    ) -> tuple[
        list[tuple[int, int]],
        list[list[float]],
        list[list[float]],
        dict[tuple[int, int], list[int]]
    ]:
        return (
            self._nodes_list,
            self._adjacency_matrix,
            self._complements._complete_adjacency_matrix,
            self._complements._shortest_paths
        )