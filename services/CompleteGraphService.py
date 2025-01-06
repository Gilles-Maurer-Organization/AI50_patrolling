from services.IPathFindingService import IPathFindingService
from services.ICompleteGraphService import ICompleteGraphService

class CompleteGraphService(ICompleteGraphService):
    """
        Class for managing a complete graph derived from a simple
        graph.

        Attributes:
            _node_position (dict): A dictionary mapping each node to its
                coordinates.
            _simple_graph (list[list[float]]): The adjacency matrix
                representing distances between nodes in the simple
                graph.
            _complete_graph (list[list[float]]): The adjacency matrix
                representing distances between nodes in the complete
                graph.
            _shortest_way_matrix (list[list[list[int]]]): A matrix that
                specifies, for each pair of nodes, the path to take
                from one to the other.
            _path_finding_service (IPathFindingService): A service that
                implements a function to find the shortest way between
                two nodes.
        """
     
    def __init__(
        self,
        simple_graph: list[list[float]],
        node_position: dict[int, tuple[int, int]],
        path_finding_service : IPathFindingService
    ) -> None: 
        self._simple_graph = simple_graph
        self._node_position = node_position
        self._complete_graph = [[0 for _ in range(len(simple_graph))]
                                for _ in range(len(simple_graph))]
        self._shortest_way_matrix = [[[] for _ in range(len(simple_graph))]
                                     for _ in range(len(simple_graph))]
        self._path_finding_service = path_finding_service
        self.create_complete_graph()

    def create_complete_graph(self) -> None: 
        for i in range(len(self._simple_graph)): 
            for j in range(i, len(self._simple_graph[i])):
                if self._simple_graph[i][j] == 0:
                    path_finding_service = self._path_finding_service(
                        self._simple_graph,
                        self._node_position,
                        i,
                        j
                    )

                    a_star_result = path_finding_service.find_path()

                    if a_star_result is None:
                        self._complete_graph = None
                        return

                    path, distance = a_star_result
                    
                    self._complete_graph[i][j] = distance
                    self._complete_graph[j][i] = distance

                    self._shortest_way_matrix[i][j] = path
                    self._shortest_way_matrix[j][i] = path.reverse()

                elif i != j: 

                    self._complete_graph[i][j] = self._simple_graph[i][j]
                    self._complete_graph[j][i] = self._simple_graph[i][j]

                    self._shortest_way_matrix[i][j] = [i, j]
                    self._shortest_way_matrix[j][i] = [j, i]

    def get_shortest_way(self, node1, node2) -> list[int]: 
        # find the shortest way in the matrix 
        return self._shortest_way_matrix[node1, node2]

    @property
    def complete_graph(self) -> list[list[float]]: 
        """
        Returns the complete graph as an adjacency matrix.

        This property provides access to the complete graph, where each
        element in the matrix represents the distance between two nodes.

        Returns:
            list[list[float]]: The adjacency matrix of the complete graph.
        """
        return self._complete_graph