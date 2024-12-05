from typing import Optional

import pygame

from constants.Colors import Colors
from constants.Config import NODE_RADIUS
from models.Agent import Agent
from models.Graph import Graph
from models.Node import Node
from views.popup.PopupView import PopupView
from views.popup.InfoPopupView import InfoPopupView
from views.popup.ErrorPopupView import ErrorPopupView

class GraphView:
    """
    This class represents the view of the graph.

    It is responsible for displaying the graph, nodes, edges, and
    agents, as well as managing the background image for the graph view.

    Attributes:
        _screen (pygame.Surface): The surface on which the graph and
            other UI elements are drawn.
        _background_image (Optional[pygame.Surface]): The background
            image for the graph view, or None if no background is set.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._background_image = None
        self._popup = None

    def set_background_image(
        self,
        background_image: Optional[pygame.Surface]
    ) -> None:
        """
        Sets the background image for the view.

        If None is passed, the background image will be cleared.

        Args:
            background_image (Optional[pygame.Surface]): The background
                image for the graph view, or None to clear it.
        """
        self._background_image = background_image

    def draw_graph(
        self,
        graph: Graph,
        selected_node: Node = None,
        dragging_node: Node = None
    ) -> None:
        """
        Draws the graph on the screen, including nodes and edges.

        If a background image is set, it will be drawn first. Then,
        nodes are drawn, with optional highlighting for selected or
        dragging nodes.

        Args:
            graph (Graph): The graph object containing nodes and edges
                to be drawn.
            selected_node (Node, optional): The node currently selected
                by the user.
            dragging_node (Node, optional): The node currently being
                dragged by the user.
        """
        if self._background_image is None:
            self._screen.fill(Colors.WHITE.value)
        else:
            self._screen.blit(self._background_image, (0, 0))

        for node in graph.nodes:
            color = self._get_node_color(node, selected_node, dragging_node)
            pygame.draw.circle(
                self._screen,
                color,
                (node.x, node.y),
                NODE_RADIUS
            )

        self._draw_edges(graph)

    def draw_popup(self):
        """
        Draws the currently active popup on the screen, if any.

        If a popup is set, it will be displayed and its expiration will
        be checked to determine if it should be dismissed.

        This method ensures that popups are rendered and managed
        properly during the application's update cycle.
        """
        if self._popup:
            self._popup.show()
            self._popup.check_popup_expiration()

    def _get_node_color(
        self,
        node: Node,
        selected_node: Node,
        dragging_node: Node
    ) -> None:
        """
        Determines the color of a node based on its state.

        Args:
            node (Node): The node whose color is to be determined.
            selected_node (Node): The node that is currently selected.
            dragging_node (Node): The node that is currently being
                dragged.

        Returns:
            pygame.Color: The color of the node.
        """
        if node == selected_node:
            return Colors.SELECTED_NODE_COLOR.value
        elif node == dragging_node:
            return Colors.DRAGGING_NODE_COLOR.value
        else:
            return Colors.NODE_COLOR.value

    def _draw_edges(self, graph: Graph) -> None:
        """
        Draws edges between nodes in the graph.

        Args:
            graph (Graph): The graph containing the edges to be drawn.
        """
        for edge in graph.edges:
            start_node = edge[0]
            end_node = edge[1]
            pygame.draw.line(
                self._screen,
                Colors.EDGE_COLOR.value,
                (start_node.x, start_node.y),
                (end_node.x, end_node.y),
                3
            )

    def draw_simulation(self, agents: list[Agent]) -> None:
        """
        Draws each agent at its updated position.

        Args:
            agents (List[Agent]): A list of agents to be drawn on the
                screen.
        """
        for agent in agents:
            pygame.draw.circle(
                self._screen,
                Colors.AGENT_COLOR.value,
                (int(agent.x), int(agent.y)),
                5
            )

    def has_an_image(self) -> bool:
        """
        Checks if a background image is set.

        Returns:
            bool: True if a background image is set, False otherwise.
        """
        return self._background_image is not None
    
    def show_error_popup(self, message: str) -> None:
        """
        Shows an Error Popup
        """
        popup_view = ErrorPopupView(self._screen, message)
        self._show_pop_up_type(popup_view)

    def show_info_popup(self, message: str) -> None:
        """
        Shows an Info Popup
        """
        popup_view = InfoPopupView(self._screen, message)
        self._show_pop_up_type(popup_view)
    
    def show_popup(self, message: str) -> None:
        """
        Shows a Popup
        """
        popup_view = PopupView(self._screen, message)
        self._show_pop_up_type(popup_view)

    def _show_pop_up_type(self, popup: PopupView) -> None:
        """
        Sets and starts a popup of a specific type.

        This method initializes the popup, allowing it to be displayed
        and managed within the view. It replaces any currently active
        popup with the new one.

        Args:
            popup (PopupView): The popup instance to be displayed.
        """
        self._popup = popup
        self._popup.start_popup()