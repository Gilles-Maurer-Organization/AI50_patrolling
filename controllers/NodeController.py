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

    def drag_node(
        self,
        pos: tuple[int, int]
    ) -> Optional[dict[str, Node | None]]:
        """
        Moves the dragged node according to the current mouse position.
        Either with a snapping process, or without.

        Args:
            pos (tuple of float): The current coordinates of th
                mouse's cursor (x, y).

        Returns:
            dict[str, Node | None] (optional): a dictionary of the
                candidates that pass the snap sensitivity check,
                composed of the related node with its axis.
                Returns None if no candidates are found.
        """
        if self._dragging_node is not None:
            candidates = self.move_node_with_snapping(
                self._dragging_node, pos[0], pos[1], self._graph.nodes, mouse_position=pos
            )
            return candidates
        
        return None

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

    def get_node_at_position(self, pos: tuple[int, int]) -> Optional[Node]:
        """
        Finds and returns the node located at the specified (x, y)
        coordinates based on the user's mouse click.

        Args:
            pos (tuple of int): The mouse click coordinates (x, y).

        Returns:
            Node (optional): The node located at the specified
                coordinates, or None if no node is found.
        """
        for node in self._graph.nodes:
            if (
                math.sqrt((node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2)
                < NODE_RADIUS
            ):
                return node
        return None
    
    def move_node_with_snapping(
        self,
        node: Node,
        new_x: int,
        new_y: int,
        nodes: list[Node],
        mouse_position: tuple[int, int],
        threshold: int = 10,
    ) -> Optional[dict[str, Node | None]]:
        """
        Moves a node with a snapping process that helps the user to
        align nodes on the user interface.

        Args:
            node (Node): the dragged node.
            new_x (int): the new x position of the node when a snap is
                detected on the y axis.
            new_y (int): the new y position of the node when a snap is
                detected on the y axis.
            nodes (list[Node]): the list of nodes in the graph used to
                find any candidate.
            mouse_position (tuple[int, int]): the user's cursor
                position when dragging the node.
            threshold (int, optional): the sensivity of the snapping.

        Returns:
            dict[str, Node | None] (optional): a dictionary of the
                candidates that pass the snap sensitivity check,
                composed of the related node with its axis.
                Returns None if no candidates are found.
        """
        if mouse_position:
            distance_x = abs(mouse_position[0] - node.x)
            distance_y = abs(mouse_position[1] - node.y)

            # If the mouse is too far from the thresold,
            # move the node to the position of the mouse
            if distance_x > threshold or distance_y > threshold:
                node.x, node.y = mouse_position
                # Don't need to search for candidates
                return None

        # If the mouse is close enough, search for snap candidates
        candidates = self._graph.find_alignment_candidates(
            node,
            nodes,
            threshold
        )
        
        # If a candidate is found on the x axis, we apply the
        # x position of the candidate
        if candidates.get("x"):
            new_x = candidates["x"].x

        # If a candidate is found on the y axis, we apply the
        # y position of the candidate
        if candidates.get("y"):
            new_y = candidates["y"].y

        # Move the coordinates of the node (after or without snap)
        node.x, node.y = new_x, new_y

        return candidates


