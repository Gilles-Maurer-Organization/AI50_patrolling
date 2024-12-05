import unittest
from unittest.mock import MagicMock, Mock, patch
import pygame
import pygame_gui
from pygame_gui import UIManager
from models.FileExplorer import FileExplorer
from views.FileExplorerView import FileExplorerView
from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController


class TestFileExplorerController(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.graph_controller = Mock(spec=GraphController)
        self.controller = FileExplorerController(self.screen, self.graph_controller)
        
        self.controller._file_explorer_view = MagicMock(spec=FileExplorerView)
        self.controller._file_explorer = MagicMock(spec=FileExplorer)
        self.controller._file_explorer_view.ui_manager = MagicMock(spec=UIManager)

        self.controller._file_explorer.opened = False

        self.controller._file_explorer_view.close_file_explorer = MagicMock()

    def test_initial_state(self):
        # We assert that the initial state of the file explorer is set to
        # opened = False
        self.assertFalse(self.controller._file_explorer.opened)
        # We assert that the file_explorer is not opened
        self.assertFalse(self.controller.is_file_explorer_opened())

    def test_open_file_explorer(self):
        # We set the dialog to opened
        self.controller._file_explorer.opened = MagicMock()
        self.controller.set_is_opened(True)
        # We verify that the opened variable is set to True
        self.assertTrue(self.controller._file_explorer.opened)
        
        # We assert that the file dialog is opened
        self.assertTrue(self.controller.is_file_explorer_opened())

    def test_close_file_explorer(self):
        # We mock the methods that are called in the close_file_explorer() method
        self.controller._file_explorer_view._close_file_explorer = MagicMock()

        self.controller._file_explorer.opened = MagicMock()

        # We test our function
        self.controller._close_file_explorer()

        # We verify that the close_file_explorer() of the view was called
        self.controller._file_explorer_view._close_file_explorer.assert_called_once()

        # We verify that the opened variable is set to False
        self.assertFalse(self.controller._file_explorer.opened)
    
    def test_handle_event_close_button(self):
        # We create a new Magic Mock of an event
        event = MagicMock()
        # We set it to a type of USEREVENT and UI_BUTTON_PRESSED in order
        # to simulate a click of the user in the file dialog
        event.type = pygame.USEREVENT
        event.user_type = pygame_gui.UI_BUTTON_PRESSED
        # We say that the id of the object clicked is the close button
        event.ui_object_id = '#file_dialog.#close_button'

        # We mock the close_file_explorer() method
        self.controller._close_file_explorer = MagicMock()

        # We test the method
        self.controller.handle_event(event)

        # We assert that the close_file_explorer() method was called only one time
        self.controller._close_file_explorer.assert_called_once()
    
    def test_handle_event_select_file(self):
        # We create a new Magic Mock of an event
        event = MagicMock()
        # And we set it to a type of USEREVENT and UI_FILE_DIALOG_PATH_PICKED
        # in order to simulate that a file was selected by the user
        event.type = pygame.USEREVENT
        event.user_type = pygame_gui.UI_FILE_DIALOG_PATH_PICKED
        # We set the text of the event to the path we want to check
        event.text = 'path/to/the/file.csv'

        # We create a new mock of our file dialog
        self.controller._file_explorer_view.file_explorer = MagicMock()
        self.controller._close_file_explorer = MagicMock()
        
        event.ui_element = self.controller._file_explorer_view.file_explorer

        # We call our event
        self.controller.handle_event(event)

        # We check that the path equalt to the good path
        self.assertEqual(self.controller._file_explorer.path, 'path/to/the/file.csv')

        # We check that the close_file_explorer() method was called
        self.controller._close_file_explorer.assert_called_once()
    
    def test_draw_file_explorer_when_opened(self):
        # We say that the file explorer is opened
        self.controller._file_explorer.opened = True

        # We test the method
        self.controller.draw_file_explorer()

        # We check that the draw_file_explorer() method of the view was called
        self.controller._file_explorer_view.draw_file_explorer.assert_called_once()
    
    def test_draw_file_explorer_when_closed(self):
        # We simulate that the file explorer is closed
        self.controller._file_explorer.opened = False
        # We test the method
        self.controller.draw_file_explorer()

        # We verify that the draw_file_explorer() method of the view was not called
        self.controller._file_explorer_view.draw_file_explorer.assert_not_called()

    def tearDown(self):
        pygame.quit()
