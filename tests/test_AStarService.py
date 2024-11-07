import unittest
import math
from services.AStarService import AStarService

class TestAStarService(unittest.TestCase):
    
    def setUp(self):
        self.graph = [
            [0, 1, 1, 0],  # Node 0
            [1, 0, 0, 1],  # Node 1
            [1, 0, 0, 1],  # Node 2
            [0, 1, 1, 0]   # Node 3
        ]
        self.node_position = {
            0: (0, 0), 1: (2, 0),
            2: (0, 1), 3: (1, 1)
        }
    
    def test_compute_h(self):
        # Test de la méthode compute_h
        service = AStarService(self.graph, self.node_position, start=0, end=3)
        heuristic = service.compute_h(0)
        expected = math.sqrt((0 - 1) ** 2 + (0 - 1) ** 2)
        self.assertEqual(heuristic, expected)

    def test_reconstruct_path(self):
        service = AStarService(self.graph, self.node_position, start=0, end=3)
        service.camem_from = {1: 0, 3: 1}
        path = service.reconstruct_path(3)
        self.assertEqual(path, [0, 1, 3])
    
    def test_find_path_success(self):
        service = AStarService(self.graph, self.node_position, start=0, end=3)
        path, cost = service.find_path()
        expected_path = [0, 2, 3]
        self.assertEqual(path, expected_path)
        self.assertEqual(cost, 2)
    
    '''
    def test_find_path_no_path(self):
        self.graph[2][3] = 0
        self.graph[3][2] = 0
        self.graph[1][3] = 0
        self.graph[3][1] = 0
        service = AStarService(self.graph, self.node_position, start=0, end=3)
        result = service.find_path()
        self.assertIsNone(result)
    '''