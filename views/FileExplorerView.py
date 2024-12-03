import pygame
import pygame_gui

from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
from models.FileExplorer import FileExplorer

class FileExplorerView:
    """
    This class represents the view of the file explorer UI.

    It is responsible for managing and displaying the file explorer UI,
    handling its appearance, and controlling interactions with the file
    selection dialog. This class uses pygame_gui to manage the UI elements
    for browsing files, including selecting files and preventing file
    deletion.

    Attributes:
        _screen (pygame.Surface): The surface on which the file explorer UI
            is drawn.
        _ui_manager (pygame_gui.UIManager): The UI manager responsible for
            managing and updating UI elements.
        _file_explorer (pygame_gui.windows.ui_file_dialog.UIFileDialog or None):
            The file dialog instance used for file selection.
        _explorer_width (int): The width of the file explorer window.
        _explorer_height (int): The height of the file explorer window.
        _rect (pygame.Rect or None): The rectangle defining the position and
            size of the file explorer window.

    Methods:
        file_explorer:
            Returns the current file explorer instance.

        process_events(event):
            Processes events related to the UI, such as user interactions with the file explorer.

        draw_file_explorer():
            Initializes and draws the file explorer on the screen.

        _update_ui_manager():
            Updates the UI manager with the frame time delta to handle animations and interactions.

        _create_requirements():
            Initializes the file explorer window if it hasn't been created yet, including defining its position and size.

        _close_file_explorer():
            Closes the file explorer if it is open and resets the reference to None.

        _hide_delete_button():
            Hides the delete button in the file explorer dialog to prevent users from deleting files.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._ui_manager = pygame_gui.UIManager((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT), 'assets/theme.json')

        self._file_explorer = None
        self._explorer_width = 300
        self._explorer_height = 350
        self._rect = None

    @property
    def file_explorer(self) -> FileExplorer:
        """
        Returns the current file explorer instance.

        Returns:
            FileExplorer: The current instance of the file explorer.
        """
        return self._file_explorer
    
    def process_events(self, event: pygame.event.Event) -> None:
        """
        Processes events related to the UI components
        (such as button clicks or window interactions).

        Args:
            event (pygame.event.Event): The event that occurred in the
            application.
        """
        self._ui_manager.process_events(event)

    def draw_file_explorer(self) -> None:
        """
        Draws the file explorer on the screen.
        """
        self._create_requirements()
        self._ui_manager.draw_ui(self._screen)
        self._update_ui_manager()

    def _update_ui_manager(self) -> None:
        """
        Updates the state of the UI manager (for animations, interactions,
        etc.) with the frame time delta.
        """
        clock = pygame.time.Clock()
        time_delta = clock.tick(30)/1000.0
        self._ui_manager.update(time_delta)

    def _create_requirements(self) -> None:
        """
        Initializes and draws the file explorer UI on the screen if it isn't
        already created.
        """
        if self._file_explorer is not None:
            return

        # Define the position and size of the file explorer window
        self._rect = pygame.Rect((GRAPH_WINDOW_WIDTH, 0), (self._explorer_width, self._explorer_height))
        # Center the file explorer window on the screen
        self._rect.center = self._screen.get_rect().center

        # Create a new file dialog to open the file explorer window
        self._file_explorer = pygame_gui.windows.ui_file_dialog.UIFileDialog(
            rect=self._rect,
            manager=self._ui_manager,
            window_title='Select an image or CSV',
            # Prevent selecting directories
            allow_picking_directories=False
        )

        # Hide the delete button to prevent file deletion
        self._hide_delete_button()

        # Make the file explorer non-resizable
        self._file_explorer.resizable = False

    def _close_file_explorer(self) -> None:
        """
        Closes the file explorer UI if it is open and resets the reference
        to None.
        """
        if self._file_explorer is not None:
            self._file_explorer.kill()
            self._file_explorer = None

    def _hide_delete_button(self) -> None:
        """
        Prevents the user from deleting a file directly from the file
        explorer dialog.
        
        Hides the delete button (if it exists) to ensure that the user
        can only import files, not delete them.
        """
        for element in self._file_explorer.get_container().elements:
            # We hide the element if it is the delete icon button
            if '#delete_icon_button' in element.object_ids:
                element.hide()
