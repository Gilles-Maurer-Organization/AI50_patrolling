import unittest
from unittest.mock import Mock
from controllers.EdgeController import EdgeController
from models.Graph import Graph
from controllers.NodeController import NodeController

class TestEdgeController(unittest.TestCase):
    def setUp(self):
        # We create mocks for Graph and NodeController classes
        self.mock_graph = Mock(spec=Graph)
        self.mock_node_controller = Mock(spec=NodeController)
        
        # We initialize EdgeController with the mocks
        self.edge_controller = EdgeController(self.mock_graph, self.mock_node_controller)
        
        # We prepare fictive nodes
        self.node1 = Mock()
        self.node2 = Mock()

    def test_create_link_successful_link_creation(self):
        # We configure the mock so that the NodeController returns the node1 for the selected node
        # and the node2 for the node at a specific position
        self.mock_node_controller.selected_node = self.node1
        self.mock_node_controller.get_node_at_position.return_value = self.node2
        
        # We create a fictive position of the mouse's cursor and we create the link
        pos = (100, 100)
        self.edge_controller.create_link(pos)
        
        # We verify that the add_method was called in the Controller's method
        self.mock_graph.add_edge.assert_called_once_with(self.node1, self.node2)
        
        # We finally verify that the selected_node has been set to None after creating the edge
        self.assertIsNone(self.mock_node_controller.selected_node)

    def test_create_link_no_link_if_selected_node_none(self):
        # We set the selected_node to None in order to verify that the edge hasn't been created
        self.mock_node_controller.selected_node = None
        # We still set a probable node return by the get_node_at_position method
        self.mock_node_controller.get_node_at_position.return_value = self.node2

        pos = (100, 100)
        self.edge_controller.create_link(pos)
        
        # We verify that the add_edge method hasn't been called
        self.mock_graph.add_edge.assert_not_called()

    def test_create_link_no_link_if_same_node(self):
        # We configure the selected node and the node found as the same nodes
        self.mock_node_controller.selected_node = self.node1
        self.mock_node_controller.get_node_at_position.return_value = self.node1
        
        # We call the method with a fictive position of mouse
        pos = (100, 100)
        self.edge_controller.create_link(pos)
        
        # We finally verify that the edge hasn't been created
        self.mock_graph.add_edge.assert_not_called()