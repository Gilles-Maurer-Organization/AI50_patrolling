from constants.Config import GRAPH_WINDOW_HEIGHT, GRAPH_WINDOW_WIDTH, PARAMETERS_WINDOW_WIDTH
import pygame
import pygame_gui

class FileExplorerView:
    def __init__(self, screen):
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager((GRAPH_WINDOW_WIDTH + PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT), 'assets/theme.json')

        self.file_dialog = None
        self.dialog_width = 300
        self.dialog_height = 350
        self.rect = None

    def draw_file_explorer(self):
        if self.file_dialog is not None:
            return

        screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect((GRAPH_WINDOW_WIDTH, 0), (self.dialog_width, self.dialog_height))
        self.rect.center = screen_rect.center

        self.file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(
            rect=self.rect,
            manager=self.ui_manager,
            window_title='Select an image or CSV',
            allow_picking_directories=False
        )

        # Hide the delete icon button to prevent file deletion
        self._hide_delete_button()

        self.file_dialog.resizable = False

    def close_file_dialog(self):
        if self.file_dialog is not None:
            self.file_dialog.kill()
            self.file_dialog = None

    def _hide_delete_button(self):
        """This method hides the delete button in the file dialog."""
        for element in self.file_dialog.get_container().elements:
            if '#delete_icon_button' in element.object_ids:
                element.hide()
