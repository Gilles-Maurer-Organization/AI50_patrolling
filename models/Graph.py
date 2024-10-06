from models.Node import Node
import math

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x: float, y: float):
        '''
        Cette méthode ajoute un nouveau noeud dans la liste de noeuds du graphe (côté Model).

        Args:
            x (float): Coordonnée x du noeud
            y (float): Coordonnée y du noeud
        '''
        self.nodes.append(Node(x, y))

    def add_edge(self, node1: Node, node2: Node):
        '''
        Cette méthode ajoute un lien entre deux noeuds et stocke ce lien dans la liste de liens du graphe (côté Model).

        Args:
            node1 (Node): Premier noeud
            node2 (Node): Deuxième noeud faisant la liaison avec le précédent
        '''
        self.edges.append((node1, node2))

    def distance(self, node1: Node, node2: Node):
        '''
        Cette méthode calcule la distance entre deux noeuds.

        Args:
            node1 (Node): Premier noeud
            node2 (Node): Deuxième noeud
        '''

        # Calcul de la distance entre les noeuds à l'aide de leurs coordonnées
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def compute_matrix(self):
        '''
        Cette méthode génère la matrice de noeuds du graphe ainsi que les éventuels liens entre les noeuds.
        Dans le cas où deux noeuds sont lié, leur distance les séparant est stocké dans la matrice des edges.

        Elle ne prend pas d'arguments.

        Returns:
            tuple: Un tuple contenant deux éléments :
            - edges_matrix (liste de liste de float): Une matrice d'adjacence, où edges_matrix[i][j] représente 
              la distance entre le noeud i et le noeud j. Si i et j ne sont pas liés, la valeur est 0.
            - nodes_list (liste de tuple): Une liste de tuples représentant les coordonnées des noeuds. 
              Chaque tuple contient deux coordonnées (x, y) correspondant à la position d'un noeud.
        '''

        # Création d'une matrice d'adjacence dont l'intégralité des valeurs est initialisée à zéro
        size = len(self.nodes)
        edges_matrix = [[0 for _ in range(size)] for _ in range(size)]
        
        # Remplissage de la matrice en fonction des arêtes
        for edge in self.edges:
            # On récupère les noeuds dont leur référence se situent dans les liens stockés dans la liste edge
            node1_index = self.nodes.index(edge[0])
            node2_index = self.nodes.index(edge[1])

            # On calcule leur distance
            distance = self.distance(edge[0], edge[1])

            # On stocke cette distance dans la matrice des edges
            edges_matrix[node1_index][node2_index] = distance
            # La matrice d'adjacence est symétrique, on réalise donc la même chose pour son symétrique
            edges_matrix[node2_index][node1_index] = distance


        return edges_matrix, [(node.x, node.y) for node in self.nodes]