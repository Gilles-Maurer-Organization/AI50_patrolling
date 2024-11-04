
import math


class AStarService: 

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
                
    