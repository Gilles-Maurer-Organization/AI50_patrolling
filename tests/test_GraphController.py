import unittest
from unittest.mock import Mock, MagicMock, patch

import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT
from controllers.GraphController import GraphController
from models.Graph import Graph
from models.GraphData import GraphData
from models.Node import Node
from services.ICSVService import ICSVService
from services.IImageService import IImageService
from views.GraphView import GraphView


class TestGraphController(unittest.TestCase):

    @patch('controllers.GraphController.NodeController')
    @patch('controllers.GraphController.EdgeController')
    @patch('views.GraphView')
    def setUp(self, mockGraphView, mockEdgeController, mockNodeController):
        # We initialize pygame
        pygame.init()
        # We create a simulated screen in order to prevent opening a real window
        self.screen = pygame.Surface((GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        # And we instantiate a mock of our CSV Service
        self.mock_csv_service = Mock(spec=ICSVService)
        # And our Image Service
        self.image_service = Mock(spec=IImageService)
        self.image_service.ensure_image_exists_and_copy = Mock()

        # We instantiate our GraphController that we want to test
        self.graph_controller = GraphController(screen=self.screen, csv_service=self.mock_csv_service, image_service=self.image_service)
        self.graph_controller._graph = Mock(spec=Graph)
        self.graph_controller._graph_view = Mock(spec=GraphView)
        self.graph_controller.graph.nodes = []
        self.graph_controller.graph.edges = []

        # Configure mocked methods
        self.graph_controller._graph_view.get_image_bounds.return_value = {
            "margin_left": 0,
            "margin_top": 0,
            "scaled_width": GRAPH_WINDOW_WIDTH,
            "scaled_height": GRAPH_WINDOW_HEIGHT
        }
        self.graph_controller._load_graph = MagicMock()

    def tearDown(self):
        # We quit pygame at the end of each test method
        pygame.quit()
    
    # We simulate the pygame.mouse.get_pos() method to return a (50, 50) position
    @patch('pygame.mouse.get_pos', return_value=(50, 50))
    def test_handle_event_left_click_add_node(self, mock_get_pos):
        # We set the event to a mouse button down and button=1 in order to indicate
        # that this is a left click
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)

        # We configure the return of the get_node_at_position to None in order
        # to simulate an empty space when the mouse is clicked
        self.graph_controller._node_controller.get_node_at_position.return_value = None
        
        # We call the method
        self.graph_controller.handle_event(event)
        
        # We verify that the add_node method has been called with the good position
        self.graph_controller._node_controller.add_node.assert_called_once_with(mock_get_pos())

    # We simulate the pygame.mouse.get_pos() method to return a (50, 50) position
    @patch('pygame.mouse.get_pos', return_value=(50, 50))
    def test_handle_event_left_click_drag_node(self, mock_get_pos):
        # We set the event to a mouse button down and button=1 in order to indicate
        # that this is a left click that we will need to drag our node
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)

        # We configure the return of the get_node_at_position to a Mock in order
        # to simulate that a node is selected when clicking
        self.graph_controller._node_controller.get_node_at_position.return_value = Mock()
        
        # We call the method
        self.graph_controller.handle_event(event)
        
        # We verify that the start_drag method has been called with the good position
        self.graph_controller._node_controller.start_drag.assert_called_once_with(mock_get_pos())

    
    @patch('pygame.mouse.get_pos', return_value=(50, 50))
    def test_handle_event_left_click_drag_node(self, mock_get_pos):
        # We set the event to a mouse button down and button=3 in order to indicate
        # that this is a right click
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3)

        # We configure the return of the get_node_at_position to a Mock in order
        # to simulate a node is handled by the right click
        self.graph_controller._node_controller.get_node_at_position.return_value = Mock()
        
        # We call the method
        self.graph_controller.handle_event(event)
        
        # We verify that the start_drag method has been called with the good position
        self.graph_controller._edge_controller.create_link.assert_called_once_with(mock_get_pos())
    
    def test_handle_event_end_drag(self):
        # We set the event to a mouse button up and button=1 in order to indicate
        # that the left click has been raised
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1)
        
        # We call the method
        self.graph_controller.handle_event(event)
        
        # We verify that the end_drag method has been called
        self.graph_controller._node_controller.end_drag.assert_called_once_with()

    def test_save_graph_calls_csv_service_save(self):
        # We configurate a fictive feedback for the compute_matrix() method
        edges_matrix = [[0, 1], [1, 0]]
        nodes_list = [(50, 50), (100, 100)]
        self.graph_controller.graph.compute_matrix.return_value = (edges_matrix, nodes_list)
        
        # We call the save_graph() method
        self.graph_controller.save_graph()
        
        # We verify that the CSV Service has been called with the good parameters
        self.mock_csv_service.save.assert_called_once_with(edges_matrix, nodes_list, self.graph_controller._image_name)

    def test_load_graph_calls_csv_service_load(self):
        # We configure the feedback of the load method of the CSV Service
        edges_matrix = [[0, 1], [1, 0]]
        nodes_list = [(50, 50), (100, 100)]
        complete_adjacency_matrix = []
        shortest_paths = []
        graph_data = GraphData(
                shortest_paths=shortest_paths,
                nodes_list=nodes_list,
                complete_adjacency_matrix=complete_adjacency_matrix,
                adjacency_matrix=edges_matrix
            )
        self.mock_csv_service.load_from_num_file.return_value = (
            graph_data
        )

        self.graph_controller.load_graph_from_csv(1)
        
        self.graph_controller._load_graph.assert_called_once_with(graph_data)

    def test_clear_graph_remove_all_nodes_and_edges(self):
        # We create nodes
        node1 = Node(50, 50)
        node2 = Node(100, 100)
        # We add them into the nodes list
        self.graph_controller.graph.nodes.append(node1)
        self.graph_controller.graph.nodes.append(node2)

        # We also add an edge between these two nodes
        self.graph_controller.graph.edges.append((node1, node2))

        # At the beginning, the number of nodes must be 2 and the number of edges 1
        self.assertEqual(len(self.graph_controller.graph.nodes), 2)
        self.assertEqual(len(self.graph_controller.graph.edges), 1)

        # We call the clear_graph() method
        self.graph_controller.clear_graph()

        # We verify that the nodes list and edges have been cleared
        self.assertEqual(len(self.graph_controller.graph.nodes), 0)
        self.assertEqual(len(self.graph_controller.graph.edges), 0)
    
    def test_graph_has_an_image(self):
        # We verify that he graph_has_an_image() method returns true when the
        # graph_view has an image
        self.graph_controller._graph_view.has_an_image.return_value = True
        self.assertTrue(self.graph_controller.graph_has_an_image())

    def test_graph_has_no_image(self):
        # We verify that he graph_has_an_image() method returns false when the
        # graph_view has no image
        self.graph_controller._graph_view.has_an_image.return_value = False
        self.assertFalse(self.graph_controller.graph_has_an_image())
