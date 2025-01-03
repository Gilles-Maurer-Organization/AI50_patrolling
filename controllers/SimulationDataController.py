import pygame

from controllers.SimulationController import SimulationController
from controllers.buttons.BackButtonController import BackButtonController
from models.Graph import Graph
from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
from services.ICSVService import ICSVService
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
        csv_service: ICSVService
    ) -> None:
        self._simulation_controller = simulation_controller
        self._csv_service = csv_service

        self._simulation_data_view = SimulationDataView(
            screen.subsurface(
                (GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            ))
        self._idleness_controller = IdlenessController(self._simulation_data_view)

        self._back_button_controller = BackButtonController(
            self._simulation_data_view,
            self._simulation_controller,
            self._idleness_controller
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

    def compute_export(self, algorithm_name: str) -> None:
        if self._simulation_controller.has_simulation_started():
            # Get the current graph number
            graph_number = self._csv_service.current_csv_number

            test_number = self._csv_service.get_next_test_number(algorithm_name, graph_number)

            # Start the idleness export
            self._start_idleness_export(
                algorithm_name = algorithm_name,
                test_number = test_number,
                start_time = self._simulation_controller._start_time
            )
            
    def _start_idleness_export(
        self,
        algorithm_name: str,
        test_number: int,
        start_time: float
    ) -> None:
        """
        Starts exporting idleness data every 10 seconds with metadata.

        Args:
            algorithm (str): The name of the algorithm being used in the simulation.
            test_number (int): The current test number for this simulation.
            start_time (float): The simulation start time in seconds.
        """
        def idleness_data_provider():
            return self._idleness_controller.idleness.get_idleness_data()
        
        def simulation_running_provider():
            return self._simulation_controller.has_simulation_started()
        
        self._csv_service.export_idleness_data(
            idleness_data_provider = idleness_data_provider,
            simulation_running_provider = simulation_running_provider,
            algorithm = algorithm_name,
            test_number = test_number,
            start_time = start_time,
            interval = 10
        )
