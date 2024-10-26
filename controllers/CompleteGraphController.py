<<<<<<< HEAD

# from models import Graph
# from views import GraphView
# from controllers.NodeController import NodeController
# from controllers.EdgeController import EdgeController
# from controllers.CSVController import CSVController
import math
=======
import pygame
<<<<<<< HEAD
from models import Graph
from views import GraphView
from controllers.NodeController import NodeController
from controllers.EdgeController import EdgeController
from controllers.CSVController import CSVController
>>>>>>> 4516dea (ajout complete graph controller)
=======
# from models import Graph
# from views import GraphView
# from controllers.NodeController import NodeController
# from controllers.EdgeController import EdgeController
# from controllers.CSVController import CSVController
import math
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)


class CompleteGraphController:
    '''
        Class permettant de gérer un graph complet à partir d'un graphe simple.

        Attributs : 
<<<<<<< HEAD
<<<<<<< HEAD

            nodePosition : dictionnaire qui pour chaque sommet indique ses coordonnées

=======
>>>>>>> 4516dea (ajout complete graph controller)
=======
            nodePosition : dictionnaire qui pour chaque sommet indique ses coordonnées
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)
            simpleGraph : la matrice représentant les distances entre les sommets du graph simple 
            completeGraph : la matrice représentant les distances entre les sommets du graph complet 

            shortestWayMatrix : matrice qui pour chaque couple de sommet, indique le chemin à prendre pour aller de l'un à l'autre

<<<<<<< HEAD

    '''

    def __init__(self, simpleGraph, nodePosition): 

        self.simpleGraph = simpleGraph
        self.nodePosition = nodePosition
        self.completeGraph = [[0 for i in range(len(simpleGraph))] for j in range(len(simpleGraph))]
        self.shortestWayMatrix = [[[] for i in range(len(simpleGraph))] for j in range(len(simpleGraph))]
        self.create_complete_graph()
=======
    
    '''
     
    def __init__(self, simpleGraph, nodePosition): 

        self.simpleGraph = simpleGraph
<<<<<<< HEAD
        self.completeGraph, self.shortestWayMatrix = self.create_complete_graph()
>>>>>>> 4516dea (ajout complete graph controller)
=======
        self.nodePosition = nodePosition
        self.completeGraph = [[0 for i in range(len(simpleGraph))] for j in range(len(simpleGraph))]
        self.shortestWayMatrix = [[[] for i in range(len(simpleGraph))] for j in range(len(simpleGraph))]
        self.create_complete_graph()
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)

        return
    
    def create_complete_graph(self): 

<<<<<<< HEAD
<<<<<<< HEAD
=======
        # TODO : algo qui crée le graph complet 

>>>>>>> 4516dea (ajout complete graph controller)
=======
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)
        # exemple 
        # simple :  [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        # complet : [[0, 1, 2], [1, 0, 1], [2, 1, 0]]

        # shortestWayMatrix : [[(0), (0, 1), (0, 1, 2)], 
        #                      [(1, 0), (1), (1, 2)], 
        #                      [(2, 1, 0), (2, 1), (2)]]

        for i in range(len(self.simpleGraph)): 
            for j in range(i, len(self.simpleGraph[i])):

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)
                if self.simpleGraph[i][j] == 0:

                    aStar = AStarAlgorithm(self.simpleGraph, self.nodePosition, i, j)
                    path, distance = aStar.a_star()

                    self.completeGraph[i][j] = distance
                    self.completeGraph[j][i] = distance

                    self.shortestWayMatrix[i][j] = path
                    self.shortestWayMatrix[j][i] = path.reverse()

                elif i != j: 

                    self.completeGraph[i][j] = self.simpleGraph[i][j]
                    self.completeGraph[j][i] = self.simpleGraph[i][j]

                    self.shortestWayMatrix[i][j] = [i, j]
                    self.shortestWayMatrix[j][i] = [j, i]
                    
<<<<<<< HEAD

=======
                print(self.simpleGraph[i][j])

        return [], []
    
>>>>>>> 4516dea (ajout complete graph controller)
=======

>>>>>>> 1e5a6d3 (finish A* and complete graph generation)

    def get_shortest_way(self, node1, node2): 

        # find the shortest way in the matrix 
        return self.shortestWayMatrix[node1, node2]


    def get_complete_graph(self): 
        return self.completeGraph
    

<<<<<<< HEAD
class AStarAlgorithm: 

    def __init__(self, graph, nodePosition, start, end): 
        self.graph = graph
        self.nodePosition = nodePosition
        self.start = start
        self.end = end

        self.openSet = []
        self.camemFrom = {}
        self.gScore = {}
        self.fScore = {}

        # si node position est une liste : for node in range(len(nodePosition))
        for node in self.nodePosition.keys():
            self.gScore[node] = math.inf
            self.fScore[node] = math.inf

    def compute_h (self, node): 

        # distance entre le noeud et la fin
        (x1, y1) = self.nodePosition[node]
        (x2, y2) = self.nodePosition[self.end]

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def reconstruct_path(self, current): 
        total_path = [current]
        while current in self.camemFrom.keys(): 
            current = self.camemFrom[current]
            total_path.insert(0, current)

        return total_path
    

<<<<<<< HEAD
=======
class AStarAlgorithm: 

    def __init__(self, graph, nodePosition, start, end): 
        self.graph = graph
        self.nodePosition = nodePosition
        self.start = start
        self.end = end

        self.openSet = []
        self.camemFrom = {}
        self.gScore = {}
        self.fScore = {}

        # si node position est une liste : for node in range(len(nodePosition))
        for node in self.nodePosition.keys():
            self.gScore[node] = math.inf
            self.fScore[node] = math.inf

    def compute_h (self, node): 

        # distance entre le noeud et la fin
        (x1, y1) = self.nodePosition[node]
        (x2, y2) = self.nodePosition[self.end]

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def reconstruct_path(self, current): 
        total_path = [current]
        while current in self.camemFrom.keys(): 
            current = self.camemFrom[current]
            total_path.insert(0, current)

        return total_path
    

>>>>>>> 1e5a6d3 (finish A* and complete graph generation)
    def a_star(self):

        openSet = [self.start]  

        self.gScore[self.start] = 0 
        self.fScore[self.start] = self.compute_h(self.start)

        while len(openSet) > 0:

            current = openSet[0]
            for node in openSet: 
                if self.fScore[node] < self.fScore[current]: 
                    current = node

            if current == self.end: 
                return (self.reconstruct_path(current), self.gScore[current])

            openSet.remove(current)

            for i in range(len(self.graph[current])): 
                if self.graph[current][i] > 0: 
                    tentative_gScore = self.gScore[current] + self.graph[current][i]

                    if tentative_gScore < self.gScore[i]: 
                        self.camemFrom[i] = current
                        self.gScore[i] = tentative_gScore
                        self.fScore[i] = tentative_gScore + self.compute_h(i)
                        if i not in openSet: 
                            openSet.append(i)

        return None
                
                

def main():
    # Exemple de graphe simple avec 4 nœuds (graphe non complet)
    # 0 est connecté à 1 avec une distance de 1, et 1 est connecté à 2 avec une distance de 2
    simple_graph = [
        [0, 1, 4, 0, 0, 0],  # Node 0
        [1, 0, 2, 5, 0, 0],  # Node 1
        [4, 2, 0, 1, 3, 0],  # Node 2
        [0, 5, 1, 0, 2, 6],  # Node 3
        [0, 0, 3, 2, 0, 2],  # Node 4
        [0, 0, 0, 6, 2, 0]   # Node 5
    ]

    # Position des nœuds (x, y)
    node_positions = {
        0: (0, 0),
        1: (1, 0),
        2: (2, 1),
        3: (3, 0),
        4: (2, -1),
        5: (3, -1)
    }

    # Initialisation du contrôleur de graphe complet
    graph_controller = CompleteGraphController(simple_graph, node_positions)
    complete_graph = graph_controller.get_complete_graph()
    print("Graphe complet généré :")
    for row in complete_graph:
        print(row)


    # Tester A* pour obtenir le plus court chemin entre chaque paire de nœuds
    for start in range(len(simple_graph)):
        for end in range(len(simple_graph)):
            if start != end:
                astar = AStarAlgorithm(graph=simple_graph, nodePosition=node_positions, start=start, end=end)
                shortest_path = astar.a_star()
                print(f"Chemin le plus court de {start} à {end} : {shortest_path}")

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======

>>>>>>> 4516dea (ajout complete graph controller)
=======
    main()
>>>>>>> 1e5a6d3 (finish A* and complete graph generation)
