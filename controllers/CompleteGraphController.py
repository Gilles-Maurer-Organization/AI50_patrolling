import pygame
from models import Graph
from views import GraphView
from controllers.NodeController import NodeController
from controllers.EdgeController import EdgeController
from controllers.CSVController import CSVController


class CompleteGraphController:
    '''
        Class permettant de gérer un graph complet à partir d'un graphe simple.

        Attributs : 
            simpleGraph : la matrice représentant les distances entre les sommets du graph simple 
            completeGraph : la matrice représentant les distances entre les sommets du graph complet 

            shortestWayMatrix : matrice qui pour chaque couple de sommet, indique le chemin à prendre pour aller de l'un à l'autre

    
    '''
     
    def __init__(self, simpleGraph) :

        self.simpleGraph = simpleGraph
        self.completeGraph, self.shortestWayMatrix = self.create_complete_graph()

        return
    
    def create_complete_graph(self): 

        # TODO : algo qui crée le graph complet 

        # exemple 
        # simple :  [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        # complet : [[0, 1, 2], [1, 0, 1], [2, 1, 0]]

        # shortestWayMatrix : [[(0), (0, 1), (0, 1, 2)], 
        #                      [(1, 0), (1), (1, 2)], 
        #                      [(2, 1, 0), (2, 1), (2)]]

        for i in range(len(self.simpleGraph)): 
            for j in range(i, len(self.simpleGraph[i])):

                print(self.simpleGraph[i][j])

        return [], []
    

    def get_shortest_way(self, node1, node2): 

        # find the shortest way in the matrix 
        return self.shortestWayMatrix[node1, node2]


    def get_complete_graph(self): 
        return self.completeGraph
    


