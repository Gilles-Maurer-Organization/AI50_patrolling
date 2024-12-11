from typing import Optional

import pygame

from constants.Colors import Colors
from constants.Config import NODE_RADIUS, GRAPH_WINDOW_WIDTH, \
    GRAPH_WINDOW_HEIGHT, MAX_IDLENESS
from models.Agent import Agent
from models.Graph import Graph
from models.Node import Node
from views.AgentView import AgentView
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
        self._scaled_width = None
        self._scaled_height = None
        self._margin_left = 0
        self._margin_top = 0
        self._margin_color = None
        self._popup = None

    def set_background_image(
        self,
        background_image: pygame.Surface
    ) -> None:
        """
        Set the background image for the view, adjusting its size to
        fit the window and centering it with margins.

        Args:
            background_image (pygame.Surface): The image to be set as
                the background.
        """
        # Store the image in an instance variable
        self._background_image = background_image

        # Get the original dimensions of the image
        original_width, original_height = self._background_image.get_width(), \
                                          self._background_image.get_height()
        window_ratio = GRAPH_WINDOW_WIDTH / GRAPH_WINDOW_HEIGHT
        image_ratio = original_width / original_height

        # Adjust the image to fit the window size
        if image_ratio > window_ratio:
            self._scaled_width = GRAPH_WINDOW_WIDTH
            self._scaled_height = int(GRAPH_WINDOW_WIDTH / image_ratio)
            self._margin_top = (GRAPH_WINDOW_HEIGHT - self._scaled_height) // 2
            self._margin_left = 0
        elif image_ratio < window_ratio:
            self._scaled_height = GRAPH_WINDOW_HEIGHT
            self._scaled_width = int(GRAPH_WINDOW_HEIGHT * image_ratio)
            self._margin_left = (GRAPH_WINDOW_WIDTH - self._scaled_width) // 2
            self._margin_top = 0

        # Draw margins and render the image
        self._margin_color = Colors.BLACK.value
        self._screen.fill(self._margin_color)

        # Scale the image and store it as the final background
        self._background_image = pygame.transform.scale(self._background_image,
                                                        (self._scaled_width,
                                                         self._scaled_height))

    def get_image_bounds(self) -> dict[str, int]:
        """
        Retrieve the dimensions and margins of the scaled image.

        Returns:
            dict: A dictionary containing the keys 'scaled_width',
            'scaled_height', 'margin_left', and 'margin_top', each
            with their respective values as integers.
        """
        return {
            "scaled_width": self._scaled_width,
            "scaled_height": self._scaled_height,
            "margin_left": self._margin_left,
            "margin_top": self._margin_top
        }

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
        if self._background_image is None and not graph.nodes:
            # Display a default message when no graph or background is loaded
            self._screen.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(
                "Please import a graph or image to start.", True, Colors.BLACK.value
            )
            self._screen.blit(
                text_surface,
                (
                    GRAPH_WINDOW_WIDTH // 2 - text_surface.get_width() // 2,
                    GRAPH_WINDOW_HEIGHT // 2 - text_surface.get_height() // 2,
                ),
            )
            return

            # If a background or nodes exist, proceed with normal drawing
        if self._background_image is None:
            self._screen.fill(Colors.WHITE.value)
        else:    
            self._screen.fill(self._margin_color)
            self._screen.blit(
                self._background_image,
                (self._margin_left, self._margin_top)
            )

        self._draw_edges(graph)

        # Draw nodes
        self._draw_nodes(graph, selected_node, dragging_node)

    def _draw_nodes(self, graph: Graph, selected_node: Node, dragging_node: Node):
        for node in graph.nodes:
            color = self._get_node_color(node, selected_node, dragging_node)
            pygame.draw.circle(
                self._screen,
                color,
                (node.x, node.y),
                min(
                    NODE_RADIUS * (1 + 0.05 * MAX_IDLENESS), 
                    NODE_RADIUS * (1 + 0.05 * node.idleness)
                ) # Modify size based on the idleness
            )

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
            min_color = Colors.NODE_COLOR_MIN.value
            max_color = Colors.NODE_COLOR_MAX.value

            if node.idleness >= MAX_IDLENESS:
                return max_color

            # Calculate the color based on idleness
            ratio = node.idleness / MAX_IDLENESS
            color = (
                min_color[0] + (max_color[0] - min_color[0]) * ratio,
                min_color[1] + (max_color[1] - min_color[1]) * ratio,
                min_color[2] + (max_color[2] - min_color[2]) * ratio
            )
            return color

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
        agent_views = [AgentView(self._screen) for _ in agents]
        
        for agent, agent_view in zip(agents, agent_views):
            agent_view.draw((int(agent.x), int(agent.y)))

    def draw_line_full_extent(self, candidate: Node, axis: str) -> None:
        """
        Draws an horizontal or vertical line that covers the graph screen.

        Args:
            candidate (Node): the candidate found.
            axis (str): the axis x or y of the alingment.
        """
        x1, y1 = candidate.x, candidate.y

        if axis == "y":
            pygame.draw.line(self._screen, "orange", (0, y1), (GRAPH_WINDOW_WIDTH, y1), 1)
        elif axis == "x":
            pygame.draw.line(self._screen, "orange", (x1, 0), (x1, GRAPH_WINDOW_HEIGHT), 1)
        else:
            raise ValueError("Can't find axis alingment on alingment assistant.")


    def draw_line_full_extent(self, candidate: Node, axis: str) -> None:
        """
        Draws an horizontal or vertical line that covers the graph screen.

        Args:
            candidate (Node): the candidate found.
            axis (str): the axis x or y of the alingment.
        """
        x1, y1 = candidate.x, candidate.y

        if axis == "y":
            pygame.draw.line(self._screen, "orange", (0, y1), (GRAPH_WINDOW_WIDTH, y1), 1)
        elif axis == "x":
            pygame.draw.line(self._screen, "orange", (x1, 0), (x1, GRAPH_WINDOW_HEIGHT), 1)
        else:
            raise ValueError("Can't find axis alingment on alingment assistant.")


    def has_an_image(self) -> bool:
        """
        Checks if a background image is set.

        Returns:
            bool: True if a background image is set, False otherwise.
        """
        return self._background_image is not None
    
    def show_error_popup(self, message: str) -> None:
        """
        Displays an error popup with the specified message.

        Args:
            message (str): The error message to be displayed.
        """
        popup_view = ErrorPopupView(self._screen, message)
        self._show_pop_up_type(popup_view)

    def show_info_popup(self, message: str) -> None:
        """
        Displays an informational popup with the specified message.

        Args:
            message (str): The info message to be displayed.
        """
        popup_view = InfoPopupView(self._screen, message)
        self._show_pop_up_type(popup_view)
    
    def show_popup(self, message: str) -> None:
        """
        Displays a generic popup with the specified message.

        Args:
            message (str): The message to be displayed in the popup.
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