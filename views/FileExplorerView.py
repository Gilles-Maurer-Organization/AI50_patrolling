from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
import pygame
import pygame_gui

class FileExplorerView:
    '''
    This class represents the view of the file explorer UI.

    This class is responsible for drawing the file explorer, handling its appearance,
    and controlling its interactions within the user interface.

    Attributes:
        screen (pygame.Surface): The surface on which the file explorer is drawn.
        ui_manager (pygame_gui.UIManager): The manager responsible for managing UI elements.
        file_explorer (pygame_gui.windows.ui_file_dialog.UIFileDialog or None): The file dialog instance.
        explorer_width (int): The width of the file explorer window.
        explorer_height (int): The height of the file explorer window.
        rect (pygame.Rect or None): The rectangle defining the position and size of the file explorer.

    Methods:
        draw_file_explorer() -> None:
            Draws the file explorer UI on the screen if it isn't already created.

        _close_file_explorer() -> None:
            Closes the file explorer if it's open and resets its reference to None.

        _hide_delete_button() -> None:
            Hides the delete button in the file explorer dialog to prevent file deletion.
    '''

    def __init__(self, screen) -> None:
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT), 'assets/theme.json')

        self.file_explorer = None
        self.explorer_width = 300
        self.explorer_height = 350
        self.rect = None

    def draw_file_explorer(self) -> None:
        '''
        This method draws the file explorer in the User Interface.
        '''
        if self.file_explorer is not None:
            return

        # We define the rectangle of our file explorer
        self.rect = pygame.Rect((GRAPH_WINDOW_WIDTH, 0), (self.explorer_width, self.explorer_height))
        # We center the file explorer at the middle of the screen
        self.rect.center = self.screen.get_rect()

        # We create a new instance of the UIFileDialog class in order to create our file explorer
        self.file_explorer = pygame_gui.windows.ui_file_dialog.UIFileDialog(
            rect=self.rect,
            manager=self.ui_manager,
            window_title='Select an image or CSV',
            # We don't allow picking directories
            allow_picking_directories=False
        )

        # We hide the delete icon button to prevent file deletion
        self._hide_delete_button()

        # We don't allow the file explorer to be resizable
        self.file_explorer.resizable = False

    def _close_file_explorer(self) -> None:
        '''
        This method kills the file explorer (if it exists) and resets its reference to None.
        '''
        if self.file_explorer is not None:
            self.file_explorer.kill()
            self.file_explorer = None

    def _hide_delete_button(self) -> None:
        '''
        Private method that hides the delete button in the file dialog.
        It it used to prevent the user from deleting a file directly from the file dialog.

        The user is only supposed to import a file.
        '''
        for element in self.file_explorer.get_container().elements:
            # We hide the element if it is the delete icon button
            if '#delete_icon_button' in element.object_ids:
                element.hide()
