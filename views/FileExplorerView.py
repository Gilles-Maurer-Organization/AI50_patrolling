from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
import pygame
import pygame_gui

class FileExplorerView:
    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager
        self.file_dialog = None
        self.dialog_width = 260
        self.dialog_height = 300
        self.rect = None

    def draw_file_explorer(self):
        screen_rect = self.screen.get_rect()

        self.rect = pygame.Rect((GRAPH_WINDOW_WIDTH, 0), (self.dialog_width, self.dialog_height))
        self.rect.center = screen_rect.center
        self.file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(
            rect=self.rect,
            manager=self.ui_manager,
            allow_picking_directories=False
        )