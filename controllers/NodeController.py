import math
from typing import Optional

from constants.Config import NODE_RADIUS
from models.Node import Node
from models.Graph import Graph

class NodeController:
    """
    This class represents a controller responsible for handling
    operations on nodes.

    Attributes:
        _graph (Graph): A graph represented by nodes and edges, part of
            the Model.
        _dragging_node (Node or None): A node that is currently being
            dragged.
        _selected_node (Node or None): A node that is currently
            selected for operation.
    """
    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._dragging_node = None
        self._selected_node = None

    @property
    def dragging_node(self) -> Node:
        """
        Returns the node currently being dragged.

        This property provides access to the node that the user is
        currently dragging on the graph.

        Returns:
            Node: The node currently being dragged.
        """
        return self._dragging_node
    
    @property
    def selected_node(self) -> Optional[Node]:
        """
        Returns the node currently selected.

        This property provides access to the node that the user has
        selected for interaction or linking.

        Returns:
            Optional[Node]: The node currently selected, or None if no
                node is selected.
        """
        return self._selected_node
    
    @selected_node.setter
    def selected_node(self, selected_node: Optional[Node]) -> None:
        """
        Sets the selected node for interaction.

        This setter allows assigning a node as the currently selected
        node. Passing None will deselect any previously selected
        node.

        Args:
            selected_node (Optional[Node]): The node to be marked as
                selected, or None to clear the selection.
        """
        self._selected_node = selected_node

    def add_node(self, pos: tuple[int, int]) -> None:
        """
        Adds a new node to the graph at the given mouse click
        coordinates.

        Args:
            pos (tuple of float): The coordinates of the mouse click
                (x, y).
        """
        self._graph.add_node(pos[0], pos[1])
    
    def delete_node(self, node: Node) -> None:
        """
        Deletes the specified node and its associated edges from the
        graph.

        Args:
            node (Node): The node to be deleted.
        """
    
        if node is not None:  
            # Find and remove edges connected to the node
            edges_to_remove = [edge for edge in self._graph.edges
                               if edge[0] == node or edge[1] == node]
            
            for edge in edges_to_remove:
                del self._graph.edges[edge]

            # Remove the node itself
            self._graph.nodes.remove(node)


    def start_drag(self, pos: tuple[int, int]) -> None:
        """
        Starts the dragging operation by storing the node to be moved
        based on the mouse click coordinates.

        Args:
            pos (tuple of float): The coordinates of the mouse click
                (x, y).
        """
        self._dragging_node = self.get_node_at_position(pos)

    def end_drag(self) -> None:
        """
        Ends the dragging operation by resetting the dragged node and
        updating the graph's distances.
        """
        self._graph.update_distances(self._dragging_node)
        self._dragging_node = None

    def drag_node(self, pos: tuple[int, int]) -> None:
        """
        Moves the dragged node according to the current mouse position.

        Args:
            pos (tuple of float): The current coordinates of the mouse
                cursor (x, y).
        """
        if self._dragging_node is not None:
            # Update the node's position with the current mouse coordinates
            self._dragging_node.x, self._dragging_node.y = pos

    def select_node(self, node: Node) -> None:
        """
        Selects a node for linking based on its coordinates (x, y).

        Args:
            node (Node): The node to be selected for linking.
        """
        if node is not None:
            self._selected_node = node
        else:
            self._selected_node = None

    def clear_selection(self) -> None:
        """
        Deselects the currently selected node. This method is called
        when the user no longer wants to create a link between nodes.
        """
        self._selected_node = None

    def get_node_at_position(self, pos: tuple[int, int]):
        """
        Finds and returns the node located at the specified (x, y)
        coordinates based on the user's mouse click.

        Args:
            pos (tuple of int): The mouse click coordinates (x, y).

        Returns:
            Node: The node located at the specified coordinates, or
                None if no node is found.
        """
        for node in self._graph.nodes:
            if (
                math.sqrt((node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2)
                < NODE_RADIUS
            ):
                return node
        return None
