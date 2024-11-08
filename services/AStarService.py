
import math
from services.IPathFindingService import IPathFindingService

class AStarService(IPathFindingService): 

    def __init__(self, graph, node_position, start, end): 
        self.graph = graph
        self.node_position = node_position
        self.start = start
        self.end = end

        self.open_set = []
        self.camem_from = {}
        self.g_score = {}
        self.f_score = {}

        # si node position est une liste : for node in range(len(nodePosition))
        for node in self.node_position.keys():
            self.g_score[node] = math.inf
            self.f_score[node] = math.inf

    def compute_h (self, node): 

        # distance entre le noeud et la fin
        (x1, y1) = self.node_position[node]
        (x2, y2) = self.node_position[self.end]

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def reconstruct_path(self, current): 
        total_path = [current]
        while current in self.camem_from.keys(): 
            current = self.camem_from[current]
            total_path.insert(0, current)

        return total_path
    

    def find_path(self):
        open_set = [self.start]  

        self.g_score[self.start] = 0 
        self.f_score[self.start] = self.compute_h(self.start)

        while len(open_set) > 0:

            current = open_set[0]
            for node in open_set: 
                if self.f_score[node] < self.f_score[current]: 
                    current = node

            if current == self.end: 
                return (self.reconstruct_path(current), self.g_score[current])

            open_set.remove(current)

            for i in range(len(self.graph[current])): 
                if self.graph[current][i] > 0: 
                    tentative_g_score = self.g_score[current] + self.graph[current][i]

                    if tentative_g_score < self.g_score[i]: 
                        self.camem_from[i] = current
                        self.g_score[i] = tentative_g_score
                        self.f_score[i] = tentative_g_score + self.compute_h(i)
                        if i not in open_set: 
                            open_set.append(i)

        return None
                
    