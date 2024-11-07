import pygame_gui
import pygame

from views.FileExplorerView import FileExplorerView

from models.FileExplorer import FileExplorer

class FileExplorerController:
    def __init__(self, screen):
        self.screen = screen
        
        self.file_explorer = FileExplorer()
        self.file_explorer_view = FileExplorerView(screen)

    def set_is_opened(self, is_opened: bool) -> None:
        self.file_explorer.set_is_opened(is_opened)

    def draw_file_explorer(self) -> None:
        if self.is_file_dialog_opened():
            self.file_explorer_view.draw_file_explorer()
            self.file_explorer_view.ui_manager.draw_ui(self.screen)
            self.file_explorer_view.ui_manager.update(30/1000)

    def handle_event(self, event) -> None:
        self.file_explorer_view.ui_manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if hasattr(event, 'ui_object_id') and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_close_button(event)
            elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self._handle_select_file(event)

    def _close_file_dialog(self) -> None:
        print("blabla")
        self.file_explorer_view.close_file_dialog()
        self.file_explorer.set_is_opened(False)

    def is_file_dialog_opened(self) -> bool:
        return self.file_explorer.is_opened()

    def _handle_close_button(self, event) -> None:
        if event.ui_object_id == '#file_dialog.#close_button':
            self._close_file_dialog()

    def _handle_select_file(self, event) -> None:
        if event.ui_element == self.file_explorer_view.file_dialog:
            file_path = event.text
            print(f'Fichier sélectionné: {file_path}')
            self.file_explorer.set_path(file_path)
        self._close_file_dialog()