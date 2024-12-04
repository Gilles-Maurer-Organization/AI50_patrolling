import pygame
from models.Graph import Graph
from constants.Colors import Colors
from constants.Config import NODE_RADIUS
from views.popup.PopupView import PopupView
from views.popup.InfoPopupView import InfoPopupView
from views.popup.ErrorPopupView import ErrorPopupView

class GraphView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_image = None
        self._popup = None

    def set_background_image(self, background_image):
        """Set the background image for the view."""
        self.background_image = background_image

    def draw_graph(self, graph: Graph, selected_node=None, dragging_node=None) -> None:
        """
        Draw the user interface for graph design.
        """
        if self.background_image is None:
            self.screen.fill(Colors.WHITE.value)
        else:
            self.screen.blit(self.background_image, (0, 0))

        for node in graph.nodes:
            color = self.get_node_color(node, selected_node, dragging_node)
            pygame.draw.circle(self.screen, color, (node.x, node.y), NODE_RADIUS)

        self.draw_edges(graph)

    def draw_popup(self):
        if self._popup:
            self._popup.show()
            self._popup.check_popup_expiration()


    def get_node_color(self, node, selected_node, dragging_node):
        """Determine the color of a node based on its state."""
        if node == selected_node:
            return Colors.SELECTED_NODE_COLOR.value
        elif node == dragging_node:
            return Colors.DRAGGING_NODE_COLOR.value
        else:
            return Colors.NODE_COLOR.value

    def draw_edges(self, graph):
        """Draw edges between nodes."""
        for edge in graph.edges:
            start_node = edge[0]
            end_node = edge[1]
            pygame.draw.line(self.screen, Colors.EDGE_COLOR.value, (start_node.x, start_node.y), (end_node.x, end_node.y), 3)

    def draw_simulation(self, agents):
        """Draw each agent at its updated position."""
        for agent in agents:
            pygame.draw.circle(self.screen, Colors.AGENT_COLOR.value, (int(agent.x), int(agent.y)), 5)

    def has_an_image(self) -> bool:
        """Check if a background image is set."""
        return self.background_image is not None
    
    def show_error_popup(self, message: str) -> None:
        """
        This method shows an Error Popup
        """
        popup_view = ErrorPopupView(self.screen, message)
        self._show_pop_up_type(popup_view)

    def show_info_popup(self, message: str) -> None:
        """
        This method shows an Info Popup
        """
        popup_view = InfoPopupView(self.screen, message)
        self._show_pop_up_type(popup_view)
    
    def show_popup(self, message: str) -> None:
        """
        This method shows a Popup
        """
        popup_view = PopupView(self.screen, message)
        self._show_pop_up_type(popup_view)

    def _show_pop_up_type(self, popup: PopupView) -> None:
        self._popup = popup
        self._popup.start_popup()