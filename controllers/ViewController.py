import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH

from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController
from controllers.ParametersController import ParametersController
from controllers.SimulationDataController import SimulationDataController
from controllers.SimulationController import SimulationController

from services import IImageService
from services.ICSVService import ICSVService

class ViewController:
    """
    This class coordinates the different controllers and handles the
    overall drawing and event handling for the application. It manages
    the graph, parameters, file explorer, and simulation.

    Attributes:
        _screen (pygame.Surface): The main screen for rendering the
            application.
        _graph_controller (GraphController): The controller responsible
            for handling graph-related tasks.
        _file_explorer_controller (FileExplorerController):
            The controller responsible for managing the file explorer.
        _simulation_controller (SimulationController): The controller
            responsible for managing the simulation.
        _parameters_controller (ParametersController): The controller
            responsible for managing the parameters interface.
    """
    def __init__(
        self,
        csv_service: ICSVService,
        image_service: IImageService
    ) -> None:
        self._screen = pygame.display.set_mode(
            (GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            )
        self._graph_controller = GraphController(
            self._screen,
            csv_service,
            image_service
        )
        self._file_explorer_controller = FileExplorerController(
            self._screen,
            self._graph_controller
        )
        self._simulation_controller = SimulationController(
            self._graph_controller
        )
        self._parameters_controller = ParametersController(
            self._screen,
            self._graph_controller,
            self._file_explorer_controller,
            self._simulation_controller,
            csv_service
        )

        self._simulation_data_controller = SimulationDataController(
            self._screen
        )

    def handle_actions(self, event) -> None:
        """
        Handles all user actions, delegating to the appropriate
        controllers based on the event type.

        Args:
            event: The Pygame event that triggers the actions.
        """
        if not self._file_explorer_controller.is_file_explorer_opened():
            self._parameters_controller.handle_events(event)
            self._graph_controller.handle_event(event)
        self._file_explorer_controller.handle_event(event)

    def draw(self) -> None:
        """
        Draws all the necessary views, including the graph, parameters,
        and simulation on the screen.
        
        Also handles drawing the file explorer if it is open.
        """
        if self._simulation_controller.has_simulation_started():
            self._simulation_controller.draw_simulation()
            self._simulation_data_controller.draw_simulation_data()
        else:
            self._parameters_controller.draw_parameters()
        self._graph_controller.update()
        if self._file_explorer_controller.is_file_explorer_opened():
            self._file_explorer_controller.draw_file_explorer()
