import unittest
import pygame

from unittest.mock import MagicMock, Mock

from controllers.ScrollingListController import ScrollingListController
from views.ParametersView import ParametersView
from constants.Config import PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT

class TestScrollingListController(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.parameters_view = MagicMock(spec=ParametersView)
        self.screen = pygame.Surface((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.parameters_view.screen = self.screen.subsurface((GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.scrolling_list_controller = ScrollingListController(self.parameters_view)
        self.scrolling_list_controller.scrolling_list_view.draw = Mock()

    def tearDown(self):
        pygame.quit()
    
    def test_draw_scrolling_list(self):
        self.scrolling_list_controller.draw_scrolling_list()
        self.scrolling_list_controller.scrolling_list_view.draw.assert_called_once()
    
    def test_is_scrolling_list_header_hovered_scrolling_list_doesnt_exist(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (30 + GRAPH_WINDOW_WIDTH, 30)})
        self.scrolling_list_controller.scrolling_list_view.scrolling_list_rect = pygame.Rect(0, 0, 0, 0)
        is_hovered = self.scrolling_list_controller.is_scrolling_list_header_hovered(event)

        self.assertFalse(is_hovered)
    
    def test_is_scrolling_list_header_hovered_is_not_hovered(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (30 + GRAPH_WINDOW_WIDTH, 30)})
        is_hovered = self.scrolling_list_controller.is_scrolling_list_header_hovered(event)

        self.assertFalse(is_hovered)

    def test_is_scrolling_list_header_hovered_is_hovered(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (30 + GRAPH_WINDOW_WIDTH, 30)})
        self.scrolling_list_controller.scrolling_list_view.scrolling_list_rect = pygame.Rect(20, 20, 20, 20)
        is_hovered = self.scrolling_list_controller.is_scrolling_list_header_hovered(event)

        self.assertTrue(is_hovered)
    
    def test_handle_event(self):
        pass

    def test_handle_header_clicked(self):
        pass

    def test_handle_header_hovered(self):
        pass

    def test_handle_scrolling_list_options(self):
        pass

    def test_get_selected_algorithm(self):
        pass
