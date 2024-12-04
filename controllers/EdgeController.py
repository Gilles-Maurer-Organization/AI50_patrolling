from controllers.NodeController import NodeController
from models.Graph import Graph

class EdgeController:
    """
    This class is representing a controller responsible for managing
    links (edges) between nodes.

    Attributes:
        _graph (Graph): A graph represented by nodes and edges, part of
            the Model.
        _node_controller (NodeController): A reference to the node
            controller.
    """
    def __init__(self, graph: Graph, node_controller: NodeController) -> None:
        self._graph = graph
        self._node_controller = node_controller

    def create_link(self, pos: tuple[int, int]) -> None:
        """
        Creates a link between two nodes by identifying a node at the
        given (x, y) coordinates and the previously selected node.

        Args:
            pos (tuple of int): Position of the mouse click.
        """
        node = self._node_controller.get_node_at_position(pos)
        # If a node is already selected, the second node exists, and
        # the two nodes are not identical:
        if (self._node_controller.selected_node is not None
            and node is not None
            and self._node_controller.selected_node != node):
            # Add an edge
            self._graph.add_edge(self._node_controller.selected_node, node)
            self._node_controller.selected_node = None

    