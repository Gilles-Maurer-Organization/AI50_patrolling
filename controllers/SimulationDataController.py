import pygame

from controllers.SimulationController import SimulationController
from controllers.buttons.BackButtonController import BackButtonController
from models.Graph import Graph
from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
from views.SimulationDataView import SimulationDataView
from controllers.IdlenessesController import IdlenessController

class SimulationDataController:

    """
    This class manages everything related to the visualization 
    of Idleness of the simulation.

    Attributes:
        _simulation_controller: a reference to the simulation controller
        _simulation_data_view: the Simulation section of the View
        _idleness_controller : the Idleness-data controller
        _back_button_controller: the controller handling interactions
            with the 'Back to configuration' button.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        simulation_controller: SimulationController,
    ) -> None:
        self._simulation_controller = simulation_controller

        self._simulation_data_view = SimulationDataView(
            screen.subsurface(
                (GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            ))
        self._idleness_controller = IdlenessController(self._simulation_data_view)

        self._back_button_controller = BackButtonController(
            self._simulation_data_view,
            self._simulation_controller
        )

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handles user interactions for each interactive component in the
        simulation data section.

        Args:
            event: The Pygame event containing interaction details
                (e.g., mouse clicks, key presses).
        """
        self._handle_back_button(event)

    def _handle_back_button(self, event: pygame.event.Event) -> None:
        """
        Handles mouse click interactions on the back to configuration button.

        Args:
            event: The Pygame event containing information about mouse
                clicks.
        """
        self._back_button_controller.handle_event(event)

    def draw_simulation_data(self,graph : Graph) -> None:
        """
        Draws the simulation data by updating the idleness's values.
        Draws also the back to configuration button.
        """
        self._simulation_data_view.draw()
        self._idleness_controller.draw_idlenesses(graph.nodes)
        self._back_button_controller.draw_buttons()
