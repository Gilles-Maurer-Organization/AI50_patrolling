import pygame

from controllers.GraphController import GraphController
from models.Button import Button
from views.ButtonView import ButtonView
from views.ParametersView import ParametersView


class BaseButtonController:
    """
    This class is responsible for managing the buttons in the ParametersView and handling their events.

    It initializes the button views and associates them with the corresponding button actions. 
    The controller listens for mouse events such as clicks and hover motions, and it triggers the appropriate 
    button actions based on user interaction.

    Methods:
        draw_buttons() -> None:
            Draws all the buttons onto the view.
        
        handle_event(event: pygame.event.Event) -> None:
            Handles the mouse events, such as clicks and hover motions, triggering the corresponding button actions.

    Attributes:
        _parameters_view (ParametersView): The view that contains the buttons.
        _graph_controller (GraphController): The controller that manages the graph.
        _button_map (dict[Button, ButtonView]): A dictionary mapping Button objects to their corresponding ButtonView objects.
    """
    def __init__(self,
                 parameters_view: ParametersView,
                 graph_controller: GraphController) -> None:
        self._parameters_view = parameters_view
        self._graph_controller = graph_controller

        self._button_map: dict[Button, ButtonView] = {}

    def draw_buttons(self) -> None:
        """
        Draws all the buttons on the view.
        """
        for button, button_view in self._button_map.items():
            button_view.draw(button.enabled)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles the button click event.

        This method checks if the received event corresponds to a left mouse click. 
        If so, it triggers the action associated with the button clicked by the user.

        Args:
            event: The Pygame event containing information about the mouse click.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, button_view in self._button_map.items():
                if button_view.is_hovered(event) and button.enabled:
                    button.action()
        
        if event.type == pygame.MOUSEMOTION:
            for button_view in self._button_map.values():
                if button_view.is_hovered(event):
                    button_view.set_hovered()
                else:
                    button_view.set_normal()
