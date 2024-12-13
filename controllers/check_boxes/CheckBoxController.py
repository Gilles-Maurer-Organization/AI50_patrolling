import pygame

from constants.Config import PARAMETERS_WINDOW_WIDTH
from controllers.GraphController import GraphController
from models.CheckBox import CheckBox
from views.CheckBoxView import CheckBoxView
from views.ParametersView import ParametersView

class CheckBoxController:
    """
    This class is managing the logic and interactions of a checkbox.
    
    Attributes:
        _graph_controller (GraphController): The controller managing the graph logic.
        _parameters_view (ParametersView): The view containing UI elements.
        _check_box (CheckBox): The model representing the checkbox state.
        _check_box_view (CheckBoxView): The view for rendering the checkbox.
    """
    def __init__(
        self,
        parameters_view: ParametersView,
        graph_controller: GraphController
    ) -> None:
        self._graph_controller = graph_controller
        self._parameters_view = parameters_view

        self._check_box = CheckBox()
        self._check_box_view = self.create_view()

    def create_view(self) -> CheckBoxView:
        """
        Creates the checkbox view. This method should be overridden to define 
        the specific position and properties of the checkbox.

        Args:
            parameters_view (ParametersView): The view containing UI elements.

        Returns:
            CheckBoxView: An instance of the checkbox view.
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events for the checkbox, such as mouse clicks.

        Args:
            event (pygame.event.Event): The event to be processed (mouse click).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._check_box_view.is_clicked(event):
                self._check_box.toggle()
                self.draw_check_box()
                self.on_state_change()

    def on_state_change(self) -> None:
        """
        Called when the state of the checkbox changes.
        This method should be overridden to implement specific behavior.
        """
        pass
    
    def draw_check_box(self) -> None:
        """
        Draws the checkbox on the parameters' view.

        This method updates the checkbox's appearance based on its state.
        """
        self._check_box_view.draw(
            self._check_box.enabled
        )
