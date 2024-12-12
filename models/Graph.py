import math

from models.Node import Node

class Graph:
    """
    This class represents a graph with nodes and edges and provides
    various methods for graph manipulation such as adding nodes,
    calculating distances, and generating adjacency matrices.

    The Graph class allows you to manage nodes, edges, and compute
    matrices for the graph. 

    It also provides functionality to store and update the shortest
    paths and modify distances between nodes.

    Attributes:
        _nodes: A list of nodes in the graph.
        _edges: A dictionary mapping pairs of nodes (edges) to their
            corresponding distances.
        _complete_adjacency_matrix: A complete adjacency matrix
            representing the graph's connectivity.
        _shortest_paths: A dictionary storing the shortest paths
            between nodes.
        _modified: A flag indicating whether the graph has been
            modified.
    """
    def __init__(self) -> None:
        self._nodes: list[Node] = []
        self._edges: dict[tuple[Node, Node], float] = {}
        self._complete_adjacency_matrix: list[list[float]] = []
        self._shortest_paths: dict[tuple[int, int], list[int]] = {}
        self._modified = False

    @property
    def nodes(self) -> list[Node]:
        """
        Getter for the nodes attribute.
        """
        return self._nodes

    @property
    def edges(self) -> dict[tuple[Node, Node], float]:
        """
        Getter for the edges attribute.
        """
        return self._edges
    
    @property
    def modified(self) -> bool:
        """
        Returns True if the graph has been modified, otherwise False.
        """
        return self._modified
    
    @property

    def empty(self) -> bool:
        """
        Returns True if the graph contains no nodes, otherwise False.
        """
        return not self._nodes
    

    def mark_as_modified(self) -> None:
        """
        Marks the graph as modified if it has not been marked already.
        """
        if not self._modified:
            print("Graph Modified")
            self._modified = True

    def update_distances(self, dragged_node: Node) -> None:
        """
        Updates the distances of the neighbors of a dragged node after
        a move.

        Args:
            dragged_node (Node): The node that has been dragged and
            whose neighbors' distances need to be updated.
        """
        neighbors = set()

        for (n1, n2) in self._edges.keys():
            if n1 == dragged_node:
                neighbors.add(n2)
            elif n2 == dragged_node:
                neighbors.add(n1)
        
        for neighbor in neighbors:
            print("modifying distance")
            distance = self.distance(neighbor, dragged_node)
            self._edges[neighbor, dragged_node] = self._edges[dragged_node, neighbor] = distance

    def add_node(self, x: float, y: float) -> None:
        """
        Adds a new node to the graph at the specified coordinates.

        Args:
            x (float): The x coordinate of the new node.
            y (float): The y coordinate of the new node.
        """
        self._nodes.append(Node(x, y))

    def add_edge(self, node1: Node, node2: Node) -> None:
        """
        Adds an edge between two nodes with the calculated distance.

        Args:
            node1 (Node): The first node in the edge.
            node2 (Node): The second node in the edge.
        """
        distance = self.distance(node1, node2)
        self._edges[(node1, node2)] = self._edges[(node2, node1)] = distance

    def distance(self, node1: Node, node2: Node) -> float:
        """
        Calculates the Euclidean distance between two nodes.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The Euclidean distance between the two nodes.
        """
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def compute_matrix(
            self
    ) -> tuple[
        list[list[float]],
        dict[int, tuple[int, int]]
    ]:
        """
        Generates the adjacency matrix and a dictionary mapping node
        indices to their coordinates.

        Returns:
            tuple: A tuple containing the adjacency matrix and the
                nodes' list.
        """
        size = len(self._nodes)

        edges_matrix = [[0 for _ in range(size)] for _ in range(size)]

        for (node1, node2), distance in self._edges.items():
            node1_index = self._nodes.index(node1)
            node2_index = self._nodes.index(node2)
            edges_matrix[node1_index][node2_index] = distance

        nodes_list = {index: (node.x, node.y)
                      for index, node in enumerate(self._nodes)}
        
        return edges_matrix, nodes_list


    def get_shortest_paths(self):
        return self._shortest_paths


    def get_complete_adjacency_matrix(self):
        return self._complete_adjacency_matrix

    def set_shortest_paths(
        self,
        shortest_paths: dict[tuple[int, int],list[int]]
    ) -> None:
        """
        Sets the shortest paths dictionary for the graph.

        Args:
            shortest_paths (dict[tuple[int, int], list[int]]):
                A dictionary where the keys are node pairs and the
                values are the shortest paths between those nodes.
        """
        self._shortest_paths = shortest_paths

    def set_complete_adjacency_matrix(
        self,
        complete_adjacency_matrix: list[list[float]]
    ) -> None:
        """
        Sets the complete adjacency matrix for the graph.

        Args:
            complete_adjacency_matrix (list[list[float]]): The complete
                adjacency matrix representing the connectivity of the
                graph.
        """
        self._complete_adjacency_matrix = complete_adjacency_matrix


