import math

from services.IPathFindingService import IPathFindingService

class AStarService(IPathFindingService):
    """
    This class implements the A* pathfinding algorithm.

    Attributes:
        _graph (list[list[float]]): The adjacency matrix representing the
            graph.
        _node_position (dict[int, tuple[int, int]]): The positions of the
            nodes as (x, y) coordinates.
        _start (int): The starting node for the pathfinding.
        _end (int): The target node for the pathfinding.
        _open_set (list[int]): A list of nodes to be evaluated by the
            algorithm.
        _came_from (dict[int, int]): A dictionary mapping nodes to
            their predecessors in the path.
        _g_score (dict[int, float]): The cost of the shortest path from
            the start to each node.
        _f_score (dict[int, float]): The estimated cost from the start
            to the target through each node.
    """
    def __init__(
        self,
        graph: list[list[float]],
        node_position: dict[int, tuple[int, int]],
        start: int,
        end: int
    ) -> None: 
        
        self._graph = graph
        self._node_position = node_position
        self._start = start
        self._end = end

        self._open_set = []
        self._came_from = {}
        self._g_score = {}
        self._f_score = {}

        for node in self._node_position.keys():
            self._g_score[node] = math.inf
            self._f_score[node] = math.inf

    def _compute_h (self, node): 
        # distance entre le noeud et la fin
        (x1, y1) = self._node_position[node]
        (x2, y2) = self._node_position[self._end]

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def _reconstruct_path(self, current): 
        total_path = [current]
        while current in self._came_from.keys(): 
            current = self._came_from[current]
            total_path.insert(0, current)

        return total_path
    

    def find_path(self):
        open_set = [self._start]  

        self._g_score[self._start] = 0 
        self._f_score[self._start] = self._compute_h(self._start)

        while len(open_set) > 0:

            current = open_set[0]
            for node in open_set: 
                if self._f_score[node] < self._f_score[current]: 
                    current = node

            if current == self._end: 
                return (self._reconstruct_path(current),
                        self._g_score[current])

            open_set.remove(current)

            for i in range(len(self._graph[current])): 
                if self._graph[current][i] > 0: 
                    tentative_g_score = self._g_score[current] + self._graph[current][i]

                    if tentative_g_score < self._g_score[i]: 
                        self._came_from[i] = current
                        self._g_score[i] = tentative_g_score
                        self._f_score[i] = tentative_g_score + self._compute_h(i)
                        if i not in open_set: 
                            open_set.append(i)

        return None
                
    