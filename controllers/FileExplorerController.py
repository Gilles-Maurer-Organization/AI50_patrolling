import pygame
import pygame_gui

from models.FileExplorer import FileExplorer
from views.FileExplorerView import FileExplorerView


class FileExplorerController:
    '''
    This class is responsible for controlling the behavior of the file explorer, managing its view and model.

    This class handles the logic for opening/closing the file explorer, drawing the file explorer on the screen,
    handling user events (such as file selection or closing the file explorer), and updating the file explorer's state.

    Attributes:
        screen (pygame.Surface): The surface on which the file explorer is drawn.
        file_explorer (FileExplorer): The model of the file explorer that holds data such as file's path.
        file_explorer_view (FileExplorerView): The view of the file explorer that manages its drawing.

    Methods:
        set_is_opened(is_opened: bool) -> None:
            Sets the file explorer's opened state (True for opened, False for closed).
        
        draw_file_explorer() -> None:
            Draws the file explorer on the screen if it is opened.
        
        handle_event(event) -> None:
            Processes events related to the file explorer, including button presses and file selection.

        _close_file_explorer() -> None:
            Closes the file explorer and updates its state.

        is_file_explorer_opened() -> bool:
            Returns whether the file explorer is currently opened.

        _handle_close_button(event) -> None:
            Handles the close button event to close the file explorer.

        _handle_select_file(event) -> None:
            Handles file selection, storing the selected file path in the model.
    '''
    def __init__(self, screen, graph_controller):
        self.screen = screen
        self.graph_controller = graph_controller
        
        # We instanciate our model and view of file explorer
        self.file_explorer = FileExplorer()
        self.file_explorer_view = FileExplorerView(screen)

    def set_is_opened(self, is_opened: bool) -> None:
        '''
        This method sets the file explorer to opened.
        '''
        self.file_explorer.set_is_opened(is_opened)

    def draw_file_explorer(self) -> None:
        '''
        This method draws the file explorer, only if the file explorer is opened.
        '''
        if self.is_file_explorer_opened():
            self.file_explorer_view.draw_file_explorer()
            # We draw the file explorer on the screen
            self.file_explorer_view.ui_manager.draw_ui(self.screen)

            # We update the file explorer thanks to the manager with a frequency
            clock = pygame.time.Clock()
            time_delta = clock.tick(30)/1000.0
            self.file_explorer_view.ui_manager.update(time_delta)

    def handle_event(self, event) -> None:
        '''
        This method handle the events sent to the file explorer.
        '''
        # Processing of the events thanks to the UIManager
        self.file_explorer_view.ui_manager.process_events(event)
        
        # If the event is a user event
        if event.type == pygame.USEREVENT:
            # We check if this is a button pressed
            if hasattr(event, 'ui_object_id') and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # If this is the case, we handle the close condition
                self._handle_close_button(event)
            # If this is a UI_FILE_DIALOG_PATH_PICKED event, it means that
            # a file was selected by the user.
            elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self._handle_select_file(event)

    def _close_file_explorer(self) -> None:
        '''
        This method closes the file explorer.
        '''
        self.file_explorer_view._close_file_explorer()
        self.file_explorer.set_is_opened(False)

    def is_file_explorer_opened(self) -> bool:
        '''
        This methods returns if the file explorer is opened or not.
        '''
        return self.file_explorer.is_opened()

    def _handle_close_button(self, event) -> None:
        '''
        This method checks if the button clicked is the close button.
        '''
        # If this is the case, we close the file explorer
        if event.ui_object_id == '#file_dialog.#close_button' or event.ui_object_id == '#file_dialog.#cancel_button':
            self._close_file_explorer()

    def _handle_select_file(self, event) -> None:
        '''
        This method selects and stores the path of the file selected by the user.
        '''
        if event.ui_element == self.file_explorer_view.file_explorer:
            file_path = event.text
            # We store the path into the file explorer model
            self.file_explorer.set_path(file_path)
            if file_path.endswith('.csv'):
                self.graph_controller.import_graph_from_csv(file_path)
            else:
                self.graph_controller.import_graph_from_image(file_path)
        self._close_file_explorer()