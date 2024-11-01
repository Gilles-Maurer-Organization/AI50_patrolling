import unittest
from unittest.mock import Mock, patch
from models.Graph import Graph
from models.Node import Node
from constants.Config import NODE_RADIUS

from controllers.NodeController import NodeController

class TestNodeController(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.node_controller = NodeController(self.graph)

        self.node1 = Node(1, 1)
        self.node2 = Node(2, 2)
        self.node3 = Node(3, 3)
        self.graph.nodes = [self.node1, self.node2, self.node3]
        self.graph.edges = [(self.node1, self.node2), (self.node2, self.node3), (self.node1, self.node3)]

    def tearDown(self):
        # Reinitialization of the parameters in order to prevent dependencies between the unit tests
        self.graph.nodes.clear()
        self.graph.edges.clear()
        self.node_controller = None
        self.graph = None

    def test_add_node(self):
        pos = (50, 50)
        # We call the method that we want to test
        self.node_controller.add_node(pos)

        # We get the added node corresponding to the position of the mouse
        added_node = self.node_controller.get_node_at_position(pos)
        # We assert that the added node exists
        self.assertIsNotNone(added_node, "The node hasn't been added to the graph")
        # And that de coordinates of the node correspond with the position of the mouse
        self.assertEqual((added_node.x, added_node.y), pos, "The coordinates of the node don't correspond with the position of the mouse")

    def test_delete_node(self):

        # We call the method with want to test
        self.node_controller.delete_node(self.node2)

        # We assert that the node is no longer in the graph's nodes list
        self.assertNotIn(self.node2, self.graph.nodes)

        # We verify that the edges associated with the node2 are deleted
        self.assertNotIn((self.node1, self.node2), self.graph.edges)
        self.assertNotIn((self.node2, self.node3), self.graph.edges)

        # We verify that the other nodes and edges are intact
        self.assertIn(self.node1, self.graph.nodes)
        self.assertIn(self.node3, self.graph.nodes)
        self.assertIn((self.node1, self.node3), self.graph.edges)

    def test_start_drag_with_existing_node(self):
        pos = (50, 50)
        self.node_controller.add_node(pos)

        # We call the method that we want to test
        self.node_controller.start_drag(pos)

        self.assertIsNotNone(self.node_controller.dragging_node, "The node was not found while dragging")

    def test_start_drag_without_node(self):
        # We directly call the method without creating a node
        self.node_controller.start_drag(None)

        self.assertIsNone(self.node_controller.dragging_node, "A node was found while dragging")

    def test_end_drag(self):
        # We start dragging
        self.node_controller.start_drag(self.node1)

        # We call the method that we want to test
        self.node_controller.end_drag()

        # We verify that the node isn't considered as dragged anymore
        self.assertIsNone(self.node_controller.dragging_node, "A node is still considered as dragged in end_drag method")

    def test_drag_node(self):
        # We start initialiazing the dragging_node
        self.node_controller.start_drag(self.node2)

        # We set the new position of the mouse's cursor after dragging
        new_pos = (75, 75)
        # We drag the node according to the new position
        self.node_controller.drag_node(new_pos)

        # We verify that the coordinates are concording
        self.assertEqual((self.node2.x, self.node2.y), new_pos, "The node dragged hasn't the same coordinates as the position dragged by the mouse")


    def test_select_existing_node(self):
        self.node_controller.select_node(self.node2)

        self.assertEqual(self.node_controller.selected_node, self.node2, "The selected node should be node2")

    def test_select_non_existing_node(self):
        self.node_controller.select_node(None)
        self.assertIsNone(self.node_controller.selected_node, "The selected node should be None")
        
    def test_clear_selection(self):
        # We select a node
        self.node_controller.select_node(self.node1)
        self.assertEqual(self.node_controller.selected_node, self.node1, "The selected node should be node1")

        # We clear the selection
        self.node_controller.clear_selection()
        
        # We verify that the selection has been cleared
        self.assertIsNone(self.node_controller.selected_node, "The selected node should be None after clearing")

    def test_get_node_at_position_existing_node(self):
        # We set the position from an existing node
        pos = (self.node1.x, self.node1.y)
        
        # We make sure that the method returns the good node
        result = self.node_controller.get_node_at_position(pos)
        self.assertIs(result, self.node1, "The node returned should be node1")

    def test_get_node_at_position_non_existing_node(self):
        # We set a position with doesn't correspond to any node
        pos = (100, 100)
        
        # We make sure that the method returns None
        result = self.node_controller.get_node_at_position(pos)
        self.assertIsNone(result, "The method should return None for a non-existing node position")

    def test_get_node_at_position_edge_case(self):
        # We set a position at the limit of the NODE RADIUS
        limit_pos = (self.node1.x + NODE_RADIUS - 1, self.node1.y)
        
        # We make sure that the node is still detected
        result = self.node_controller.get_node_at_position(limit_pos)
        self.assertIs(result, self.node1, "The node returned should be node1 at the edge of NODE_RADIUS")