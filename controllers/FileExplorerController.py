from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
import pygame_gui

from views.FileExplorerView import FileExplorerView

class FileExplorerController:
    def __init__(self, screen):
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.file_explorer_view = FileExplorerView(screen, self.ui_manager)

    def draw_file_explorer(self):
        self.file_explorer_view.draw_file_explorer()
        
        self.ui_manager.draw_ui(self.screen)
