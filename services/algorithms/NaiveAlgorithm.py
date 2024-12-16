import numpy as np
import random as rd

from models.Graph import Graph
from services.algorithms.IAlgorithm import IAlgorithm

class NaiveAlgorithm(IAlgorithm):
    """
    This class implements the Naive Algorithm.

    Attributes:
        nb_agents : The number of agents
        graph_object : The graph object of the  Graph Class.
        path : a list of the shortest path found by the algorithm
        paths : a list of a list, the path of each agent
    
    """

    def __init__(
        self,
        nb_agents: int,
        graph_object: Graph
    ) -> None:

        self.nb_agents = nb_agents
        self.distance_matrix = np.array(graph_object.get_complete_adjacency_matrix())
        self.path = []
        self.paths = []
    
    def naive_shortest_path(self) -> None:
        """
        Find the shortest path of an agent in
        the graph without repetition of a node.

        """
        nb_nodes = self.distance_matrix.shape[0]
        visited = [False] * nb_nodes

        # Start at a node between 0 and number max of nodes.
        current_node = rd.randint(0,nb_nodes-1)
        self.path.append(current_node)
        visited[current_node] = True
        
        while len(self.path) < nb_nodes:
            # Find the shortest node not visited next to the current node.
            next_node = np.argmin([self.distance_matrix[current_node][i] if not visited[i] else np.inf for i in range(nb_nodes)])
            self.path.append(next_node)
            visited[next_node] = True
            current_node = next_node
    
    
    def launch(self) -> list[list[int]]:
        """
        Launches the whole Algorithm.

        Returns:
            paths : The Array with the path of each agents
        """
                
        self.naive_shortest_path()
        
        # Dispatch each agents to optimize their paths.
        if(self.nb_agents > 1):
            for idx in range(self.nb_agents):
                agent_start_index = int(len(self.path)/self.nb_agents)
                self.paths.append(self.path.copy())
                for i in range(agent_start_index):
                    self.path.append(self.path[0])
                    self.path.pop(0)
        else :
            self.paths.append(self.path.copy())
        
        return self.paths