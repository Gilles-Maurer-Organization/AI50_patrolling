import pygame
import pygame_gui

from controllers.GraphController import GraphController
from models.FileExplorer import FileExplorer
from views.FileExplorerView import FileExplorerView


class FileExplorerController:
    """
    This class is responsible for controlling the behavior of the file
    explorer, managing its view and model.

    This class handles the logic for opening/closing the file explorer,
    drawing the file explorer on the screen, handling user events
    (such as file selection or closing the file explorer), and updating
    the file explorer's state.

    Attributes:
        _screen (pygame.Surface): The surface on which the file
            explorer is drawn.
        _graph_controller (GraphController): The controller of the
            graph.
        _file_explorer (FileExplorer): The model of the file explorer
            that holds data such as file's path.
        _file_explorer_view (FileExplorerView): The view of the file
            explorer that manages its drawing.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        graph_controller: GraphController,
        on_file_imported: callable = None  # Callback for button updates
    ) -> None:
        self._screen = screen
        self._graph_controller = graph_controller
        
        # We instanciate our model and view of file explorer
        self._file_explorer = FileExplorer()
        self._file_explorer_view = FileExplorerView(screen)
        self._on_file_imported = on_file_imported  # Store the callback

    def set_is_opened(self, is_opened: bool) -> None:
        """
        This method sets the file explorer to opened.
        """
        self._file_explorer.opened = is_opened

    def draw_file_explorer(self) -> None:
        """
        This method draws the file explorer, only if the file explorer
        is opened.
        """
        if self.is_file_explorer_opened():
            self._file_explorer_view.draw_file_explorer()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        This method handle the events sent to the file explorer.
        """
        # Processing of the events thanks to the UIManager
        self._file_explorer_view.process_events(event)
        
        # If the event is a user event
        if event.type == pygame.USEREVENT:
            # We check if this is a button pressed
            if (
                hasattr(event, 'ui_object_id')
                and event.user_type == pygame_gui.UI_BUTTON_PRESSED
                ):
                # If this is the case, we handle the close condition
                self._handle_close_button(event)
            # If this is a UI_FILE_DIALOG_PATH_PICKED event, it means that
            # a file was selected by the user.
            elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self._handle_select_file(event)

    def _close_file_explorer(self) -> None:
        """
        This method closes the file explorer.
        """
        self._file_explorer_view._close_file_explorer()
        self._file_explorer.opened = False

    def is_file_explorer_opened(self) -> bool:
        """
        This methods returns if the file explorer is opened or not.
        """
        return self._file_explorer.opened

    def _handle_close_button(self, event: pygame.event.Event) -> None:
        """
        This method checks if the button clicked is the close button.
        """
        # If this is the case, we close the file explorer
        if (
            event.ui_object_id == '#file_dialog.#close_button'
            or event.ui_object_id == '#file_dialog.#cancel_button'
            ):
            self._close_file_explorer()

    def _handle_select_file(self, event: pygame.event.Event) -> None:
        """
        This method selects and stores the path of the file selected by
        the user.
        """
        if event.ui_element == self._file_explorer_view.file_explorer:
            file_path = event.text

            success = False

            # We store the path into the file explorer model
            self._file_explorer.path = file_path
            if file_path.endswith('.csv'):
                success = self._graph_controller.import_graph_from_csv(file_path)
                self._graph_controller.raise_message("Graph successfully imported!")
            else:
                success = self._graph_controller.import_graph_from_image(file_path)
                self._graph_controller.raise_message("Image successfully imported!")

            if success and self._on_file_imported:
                self._on_file_imported()
            elif not success:
                print(f"Failed to import file: {file_path}")

            self._close_file_explorer()
