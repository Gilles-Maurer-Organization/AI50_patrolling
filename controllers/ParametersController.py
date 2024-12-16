import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH
from controllers.AlignmentCheckBoxController import AlignmentCheckBoxController
from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController
from controllers.ScrollingListController import ScrollingListController
from controllers.SimulationController import SimulationController
from controllers.buttons.ButtonController import ButtonController
from controllers.buttons.StartButtonController import StartButtonController
from controllers.text_boxes.AlgorithmParametersController import AlgorithmParametersController
from controllers.text_boxes.TextBoxController import TextBoxController
from views.ParametersView import ParametersView

from services.CompleteGraphService import CompleteGraphService
from services.ICSVService import ICSVService


class ParametersController:
    """
    This class is responsible for managing the parameters section of
    the application interface. 

    Attributes:
        _simulation_controller (SimulationController): Controls the
            simulation process.
        _parameters_view (ParametersView): The view that contains
            buttons, text boxes, and other UI elements.
        _graph_controller (GraphController): Manages the graph-related
            operations and data.
        _button_controller (ButtonController): Handles interactions
            with standard buttons.
        _text_box_controller (TextBoxController): Handles interactions
            with text boxes in the UI.
        _scrolling_list_controller (ScrollingListController): Manages
            the dropdown list interactions.
        _start_button_controller (StartButtonController): Controls the
            start button functionality.
        _algorithm_parameters_controller (AlgorithmParametersController):
            Handles interactions for algorithm parameters.
    """
    
    def __init__(
        self,
        screen: pygame.Surface,
        graph_controller: GraphController,
        file_explorer_controller: FileExplorerController,
        simulation_controller: SimulationController,
        csv_service: ICSVService
    ) -> None:
        self._simulation_controller = simulation_controller

        # Creating the ParametersView with a specific subsurface
        self._parameters_view = ParametersView(
            screen.subsurface(
                (GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)
            )
        )
        
        # Initializing individual controllers
        self._graph_controller = graph_controller
        self._button_controller = ButtonController(
            self._parameters_view,
            graph_controller,
            file_explorer_controller
        )
        self._text_box_controller = TextBoxController(
            self._parameters_view
        )
        self._scrolling_list_controller = ScrollingListController(
            self._parameters_view
        )
        self._start_button_controller = StartButtonController(
            self._parameters_view,
            graph_controller,
            simulation_controller,
            self._scrolling_list_controller,
            self._text_box_controller,
            CompleteGraphService,
            csv_service
        )
        self._algorithm_parameters_controller = AlgorithmParametersController(
            self._parameters_view
        )
        self._alignment_check_box_controller = AlignmentCheckBoxController(
            self._parameters_view,
            self._graph_controller
        )

        # Disabling certain buttons if the graph does not have an image
        self._enable_or_disable_buttons()

    def draw_parameters(self) -> None:
        """
        Draws all the parameters UI components: buttons, scrolling
        list, text boxes, etc.
        """
        self._parameters_view.draw()
        self._button_controller.draw_buttons()
        self._start_button_controller.draw_buttons()
        self._text_box_controller.draw_text_boxes()
        self._algorithm_parameters_controller.draw_text_boxes()
        self._scrolling_list_controller.draw_scrolling_list()
        self._alignment_check_box_controller.draw_check_box()

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handles user interactions for each interactive component in the
        parameters section.

        Args:
            event: The Pygame event containing interaction details
                (e.g., mouse clicks, key presses).
        """
        self._handle_button(event)
        self._handle_text_box(event)
        self._handle_scrolling_list(event)
        self._handle_algorithm_parameters(event)
        self._check_start_button_state()
        self._handle_check_box(event)

    def _handle_button(self, event: pygame.event.Event) -> None:
        """
        Handles mouse click interactions on buttons.

        Args:
            event: The Pygame event containing information about mouse
                clicks.
        """
        self._button_controller.handle_event(event)
        self._start_button_controller.handle_event(event)

    def _handle_text_box(self, event: pygame.event.Event) -> None:
        """
        Handles events for the text boxes.

        Args:
            event: The Pygame event containing user interaction details.
        """
        self._text_box_controller.handle_event(event)

    def _handle_scrolling_list(self, event: pygame.event.Event) -> None:
        """
        Handles events for the dropdown list.

        Args:
            event: The Pygame event containing user interaction details.
        """
        is_algorithm_selected = self._scrolling_list_controller.handle_event(event)
        if is_algorithm_selected:
            selected_algorithm = self._scrolling_list_controller.get_selected_algorithm()
            self._algorithm_parameters_controller.handle_selected_algorithm(selected_algorithm)

    def _handle_algorithm_parameters(self, event: pygame.event.Event) -> None:
        """
        Handles events related to algorithm parameters.

        Args:
            event: The Pygame event containing interaction details.
        """
        self._algorithm_parameters_controller.handle_event(event)

    def _handle_check_box(self, event: pygame.event.Event) -> None:
        """
        Handles events related to nodes alignment.

        Args:
            event: The Pygame event containing user interaction.
        """
        self._alignment_check_box_controller.handle_event(event)

    def _enable_start_button(self) -> bool:
        """
        Enables the start button to initiate the simulation.
        """
        self._start_button_controller.enable_start_button()

    def _disable_start_button(self) -> bool:
        """
        Disables the start button to prevent the simulation from
        starting.
        """
        self._start_button_controller.disable_start_button()

    def _check_start_button_state(self) -> None:
        """
        Checks whether the start button should be enabled or disabled
        based on the current state of the UI.
        """
        if (
            self._scrolling_list_controller.get_selected_algorithm() is not None
            and self._text_box_controller.is_everything_filled()
            and not self._graph_controller.is_graph_empty()
        ):
            self._enable_start_button()
        else:
            self._disable_start_button()

    def _enable_or_disable_buttons (self) -> None:
        """
        Checks if the graph has an image and enables or disables the
        clear and save buttons accordingly.
        """
        if self._graph_controller.graph_has_an_image():
            self._button_controller.enable_clear_button()
            self._button_controller.enable_save_button()
        else:
            self._button_controller.disable_clear_button()
            self._button_controller.disable_save_button()

