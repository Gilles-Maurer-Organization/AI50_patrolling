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


    def get_complete_graph(self): 
        return self._complete_graph