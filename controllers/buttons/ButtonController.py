from constants.Colors import Colors
from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from views.ParametersView import ParametersView
from views.ButtonView import ButtonView

class ButtonController(BaseButtonController):
    """
    This class manages the buttons (Save, Import, Clear) in the
    ParametersView, and handles their events.

    Attributes:
        _file_explorer_controller (FileExplorerController): The
            controller managing file exploration for imports.
        _save_button (Button): The Save button object.
        _import_button (Button): The Import button object.
        _clear_button (Button): The Clear button object.
        _button_map (dict[Button, ButtonView]): A map of Button objects
            to their corresponding ButtonView objects.
    """
    def __init__(
        self,
        parameters_view: ParametersView,
        graph_controller: GraphController,
        file_explorer_controller: FileExplorerController
    ) -> None:
        super().__init__()
        self._parameters_view = parameters_view
        self._graph_controller = graph_controller

        self._file_explorer_controller = file_explorer_controller
        self._file_explorer_controller._on_file_imported = self._enable_buttons  # Set callback

        self._save_button = Button("Save", self.save_action)
        self._import_button = Button("Import", self.import_action)
        self._clear_button = Button("Clear", self.clear_action)

        # Creation of the button map and their models/views associated
        self._button_map = {
            self._save_button: ButtonView(
                self._parameters_view.screen,
                self._save_button.text,
                10,
                10,
                90,
                40,
                icon_path='assets/widgets/save.png'
            ),
            self._import_button: ButtonView(
                parameters_view.screen,
                self._import_button.text,
                110,
                10,
                90,
                40,
                icon_path='assets/widgets/import.png'
            ),
            self._clear_button: ButtonView(
                parameters_view.screen,
                self._clear_button.text,
                210,
                10,
                90,
                40,
                color=Colors.RED,
                hover_color=Colors.DARK_RED,
                icon_path='assets/widgets/clear.png'
            )
        }

    def save_action(self) -> None:
        """
        Saves a graph to the computer when the Save button is clicked.
        """
        self._graph_controller.save_graph()

    def import_action(self) -> None:
        """
        Imports a graph from the computer when the Import button is
        clicked.
        """
        self._file_explorer_controller.set_is_opened(True)

    def clear_action(self) -> None:
        """
        Clears the entire graph view when the Clear button is clicked.
        """
        self._graph_controller.clear_graph()
        self._enable_buttons()

    def disable_clear_button(self) -> None:
        """
        Disables the Clear button, preventing the user from interacting
        with it.
        """
        self._clear_button.enabled = False
        
    def disable_save_button(self) -> None:
        """
        Disables the Save button, preventing the user from interacting
        with it.
        """
        self._save_button.enabled = False

    def enable_clear_button(self) -> None:
        """
        Enables the Clear button.
        """
        self._clear_button.enabled = True

    def enable_save_button(self) -> None:
        """
        Enables the Save button.
        """
        self._save_button.enabled = True

    def _enable_buttons(self) -> None:
        """
        Toggles the Save and Clear buttons based on the current state of
        the graph.
        """
        self.enable_save_button()
        self.enable_clear_button()