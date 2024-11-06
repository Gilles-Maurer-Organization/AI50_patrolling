from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
import pygame_gui
import pygame

from views.FileExplorerView import FileExplorerView

class FileExplorerController:
    def __init__(self, screen):
        self.is_opened = False
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.file_explorer_view = FileExplorerView(screen, self.ui_manager)

    def set_is_opened(self, is_opened):
        self.is_opened = is_opened

    def draw_file_explorer(self):
        self.file_explorer_view.draw_file_explorer()
        self.ui_manager.draw_ui(self.screen)
        self.ui_manager.update(30/1000)

    def handle_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                if event.ui_element == self.file_explorer_view.file_dialog:
                    file_path = event.text
                    print(f'Fichier sélectionné: {file_path}')
                else:
                    self.file_explorer_view.close_file_dialog()
