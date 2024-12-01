from services.AStarService import AStarService
from services.IPathFindingService import IPathFindingService
from services.ICompleteGraphService import ICompleteGraphService

class CompleteGraphService(ICompleteGraphService):
    '''
        Class permettant de gérer un graph complet à partir d'un graphe simple.

        Attributs : 
            node_position : dictionnaire qui pour chaque sommet indique ses coordonnées
            simple_graph : la matrice représentant les distances entre les sommets du graph simple 
            complete_graph : la matrice représentant les distances entre les sommets du graph complet 

            shortest_way_matrix : matrice qui pour chaque couple de sommet, indique le chemin à prendre pour aller de l'un à l'autre
    '''
     
    def __init__(self,  simple_graph, node_position, path_finding_service : IPathFindingService): 
        self._simple_graph = simple_graph
        self._node_position = node_position
        self._complete_graph = [[0 for _ in range(len(simple_graph))] for _ in range(len(simple_graph))]
        self._shortest_way_matrix = [[[] for _ in range(len(simple_graph))] for _ in range(len(simple_graph))]
        self._path_finding_service = path_finding_service
        self.create_complete_graph()

    def create_complete_graph(self): 

        # simple :  [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        # complet : [[0, 1, 2], [1, 0, 1], [2, 1, 0]]

        # shortestWayMatrix : [[(0), (0, 1), (0, 1, 2)], 
        #                      [(1, 0), (1), (1, 2)], 
        #                      [(2, 1, 0), (2, 1), (2)]]

        for i in range(len(self._simple_graph)): 
            for j in range(i, len(self._simple_graph[i])):

                if self._simple_graph[i][j] == 0:

                    path_finding_service = self._path_finding_service(self._simple_graph, self._node_position, i, j)

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

    def get_shortest_way(self, node1, node2): 

        # find the shortest way in the matrix 
        return self._shortest_way_matrix[node1, node2]

    @property
    def complete_graph(self): 
        return self._complete_graph
    

def main():
    # Exemple de graphe simple avec 4 nœuds (graphe non complet)
    # 0 est connecté à 1 avec une distance de 1, et 1 est connecté à 2 avec une distance de 2
    # simple_graph = [
    #     [0, 1, 4, 0, 0, 0],  # Node 0
    #     [1, 0, 2, 5, 0, 0],  # Node 1
    #     [4, 2, 0, 1, 3, 0],  # Node 2
    #     [0, 5, 1, 0, 2, 6],  # Node 3
    #     [0, 0, 3, 2, 0, 2],  # Node 4
    #     [0, 0, 0, 6, 2, 0]   # Node 5
    # ]

    simple_graph = [
        [0, 1, 4, 0, 0, 0],  # Node 0
        [1, 0, 2, 0, 0, 0],  # Node 1
        [4, 2, 0, 0, 0, 0],  # Node 2
        [0, 0, 0, 0, 2, 6],  # Node 3
        [0, 0, 0, 2, 0, 2],  # Node 4
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

    # Initialisation of the complete graph service,
    # with a dependancy injection (in this case a AStarService)
    graph_controller = CompleteGraphService(simple_graph, node_positions, AStarService)
    complete_graph = graph_controller.get_complete_graph()

    if complete_graph is None:
        print("Erreur lors de la génération du graphe complet")
    else :
        print("Graphe complet généré :")
        for row in complete_graph:
            print(row)


    # Tester A* pour obtenir le plus court chemin entre chaque paire de nœuds
    for start in range(len(simple_graph)):
        for end in range(len(simple_graph)):
            if start != end:
                a_star = AStarService(simple_graph, node_positions, start, end)
                shortest_path = a_star.find_path()
                print(f"Chemin le plus court de {start} à {end} : {shortest_path}")

if __name__ == "__main__":
    main()