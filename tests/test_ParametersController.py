import unittest
from unittest.mock import MagicMock
from controllers.FileExplorerController import FileExplorerController
from controllers.ParametersController import ParametersController
from controllers.GraphController import GraphController
from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH

import pygame

class TestParametersController(unittest.TestCase):
    def setUp(self):
        pygame.init()
        
        self.screen = pygame.Surface((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))

        self.graph_controller = MagicMock(spec=GraphController)
        self.file_explorer_controller = MagicMock(spec=FileExplorerController)
        
        self.graph_controller.graph_has_an_image.return_value = False

        self.parameters_controller = ParametersController(self.screen, self.graph_controller, self.file_explorer_controller)

        self.parameters_controller.start_button_controller.enable_start_button = MagicMock()
        self.parameters_controller.start_button_controller.disable_start_button = MagicMock()
        self.parameters_controller.scrolling_list_controller.get_selected_algorithm = MagicMock()
        self.parameters_controller.text_box_controller.is_everything_filled = MagicMock()

        self.parameters_controller.text_box_controller.handle_event = MagicMock()

        self.parameters_controller.button_controller.handle_event = MagicMock()
        self.parameters_controller.start_button_controller.handle_event = MagicMock()

        self.parameters_controller.scrolling_list_controller.handle_event = MagicMock()
        self.parameters_controller.algorithm_parameters_controller.handle_event = MagicMock()
        
    def tearDown(self):
        pygame.quit()

    def test_draw_parameters(self):
        self.parameters_controller.draw_parameters()

    def test_handle_events(self):
        event = pygame.MOUSEBUTTONDOWN
        self.parameters_controller.handle_events(event)
        self.parameters_controller.button_controller.handle_event.assert_called_once_with(event)
        self.parameters_controller.start_button_controller.handle_event.assert_called_once_with(event)
        self.parameters_controller.text_box_controller.handle_event.assert_called_once_with(event)
        self.parameters_controller.scrolling_list_controller.handle_event.assert_called_once_with(event)
        self.parameters_controller.algorithm_parameters_controller.handle_event.assert_called_once_with(event)
        
    def test_handle_button(self):
        event = pygame.MOUSEBUTTONDOWN
        self.parameters_controller.handle_button(event)
        self.parameters_controller.button_controller.handle_event.assert_called_once_with(event)
        self.parameters_controller.start_button_controller.handle_event.assert_called_once_with(event)

    def test_handle_text_box(self):
        event = pygame.MOUSEBUTTONDOWN
        self.parameters_controller.handle_text_box(event)
        self.parameters_controller.text_box_controller.handle_event.assert_called_once_with(event)

    def test_handle_scrolling_list(self):
        event = pygame.MOUSEBUTTONDOWN
        self.parameters_controller.handle_scrolling_list(event)
        self.parameters_controller.scrolling_list_controller.handle_event.assert_called_once_with(event)

    def test_handle_algorithm_parameters(self):
        # We don't care to verify if the type of event is the one needed
        # The test of the type of event is done in the test_BaseTextBoxController
        event = pygame.MOUSEBUTTONDOWN
        self.parameters_controller.handle_algorithm_parameters(event)
        self.parameters_controller.algorithm_parameters_controller.handle_event.assert_called_once_with(event)
    
    def test_enable_start_button(self):
        self.parameters_controller.enable_start_button()
        self.parameters_controller.start_button_controller.enable_start_button.assert_called_once()

    def test_disable_start_button(self):
        self.parameters_controller.disable_start_button()
        self.parameters_controller.start_button_controller.disable_start_button.assert_called_once()

    def test_check_start_button_state_is_ok(self):
        self.parameters_controller.scrolling_list_controller.get_selected_algorithm.return_value = True
        self.parameters_controller.text_box_controller.is_everything_filled.return_value = True

        self.parameters_controller.check_start_button_state()

        self.parameters_controller.start_button_controller.enable_start_button.assert_called_once()

    def test_check_start_button_state_is_not_ok(self):
        self.parameters_controller.scrolling_list_controller.get_selected_algorithm.return_value = None
        self.parameters_controller.text_box_controller.is_everything_filled.return_value = False

        self.parameters_controller.check_start_button_state()

        self.parameters_controller.start_button_controller.disable_start_button.assert_called_once()
