from models.Node import Node
import math

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        self.edges = {}
        self.complete_adjacency_matrix = []
        self.shortest_paths = {}

    def add_node(self, x: float, y: float) -> None:
        '''
        Ajoute un nouveau noeud dans le graphe.

        Args:
            x (float): Coordonnée x du noeud
            y (float): Coordonnée y du noeud
        '''
        self.nodes.append(Node(x, y))

    def add_edge(self, node1: Node, node2: Node) -> None:
        '''
        Ajoute un lien entre deux noeuds avec leur distance, stockée dans le dictionnaire des arêtes.

        Args:
            node1 (Node): Premier noeud
            node2 (Node): Deuxième noeud
        '''
        distance = self.distance(node1, node2)
        # Stockage de la distance dans un dictionnaire avec des tuples (node1, node2) comme clés
        self.edges[(node1, node2)] = distance
        self.edges[(node2, node1)] = distance

    def distance(self, node1: Node, node2: Node) -> float:
        '''
        Calcule la distance entre deux noeuds.

        Args:
            node1 (Node): Premier noeud
            node2 (Node): Deuxième noeud

        Returns:
            float: La distance entre les deux noeuds.
        '''
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def compute_matrix(self):
        '''
        Génère la matrice d'adjacence du graphe ainsi que la liste des noeuds.
        
        Returns:
            tuple: (edges_matrix, nodes_list)
        '''
        size = len(self.nodes)

        edges_matrix = [[0 for _ in range(size)] for _ in range(size)]

        for (node1, node2), distance in self.edges.items():
            node1_index = self.nodes.index(node1)
            node2_index = self.nodes.index(node2)
            edges_matrix[node1_index][node2_index] = distance  # Graph symétrique

        nodes_list = {index: (node.x, node.y) for index, node in enumerate(self.nodes)}
        
        return edges_matrix, nodes_list


