from constants.Colors import Colors
from controllers.FileExplorerController import FileExplorerController
from controllers.GraphController import GraphController
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from views.ParametersView import ParametersView
from views.ButtonView import ButtonView

class ButtonController(BaseButtonController):
    '''
    This class manages the buttons (Save, Import, Clear) in the ParametersView, and handles their events.

    Methods:
        save_action() -> None:
            Handles the action triggered by clicking the Save button, saving the graph.
        
        import_action() -> None:
            Handles the action triggered by clicking the Import button, opening the file explorer.
        
        clear_action() -> None:
            Handles the action triggered by clicking the Clear button, clearing the graph.
        
        disable_clear_button() -> None:
            Disables the Clear button, preventing the user from interacting with it.
        
        disable_save_button() -> None:
            Disables the Save button, preventing the user from interacting with it.

    Attributes:
        _file_explorer_controller (FileExplorerController): The controller managing file exploration for imports.
        _save_button (Button): The Save button object.
        _import_button (Button): The Import button object.
        _clear_button (Button): The Clear button object.
        _button_map (Dict[Button, ButtonView]): A map of Button objects to their corresponding ButtonView objects.
    '''
    def __init__(self,
                 parameters_view: ParametersView,
                 graph_controller: GraphController,
                 file_explorer_controller: FileExplorerController) -> None:
        super().__init__(parameters_view, graph_controller)

        self._file_explorer_controller = file_explorer_controller

        self._save_button = Button("Save", self.save_action)
        self._import_button = Button("Import", self.import_action)
        self._clear_button = Button("Clear", self.clear_action)

        # Creation of the button map and their models/views associated
        self._button_map = {
            self._save_button: ButtonView(
                parameters_view.screen,
                self._save_button.text,
                self._save_button.action,
                10,
                10,
                90,
                40,
                icon_path='assets/save.png'
            ),
            self._import_button: ButtonView(
                parameters_view.screen,
                self._import_button.text,
                self._import_button.action,
                110,
                10,
                90,
                40,
                icon_path='assets/import.png'
            ),
            self._clear_button: ButtonView(
                parameters_view.screen,
                self._clear_button.text,
                self._clear_button.action,
                210,
                10,
                90,
                40,
                color=Colors.BUTTON_RED,
                hover_color=Colors.BUTTON_RED_HOVER
            )
        }

    def save_action(self) -> None:
        '''
        Saves a graph to the computer when the Save button is clicked.
        '''
        self._graph_controller.save_graph()
        print("Save action triggered")

    def import_action(self) -> None:
        '''
        Imports a graph from the computer when the Import button is clicked.
        '''
        self._file_explorer_controller.set_is_opened(True)

    def clear_action(self) -> None:
        '''
        Clears the entire graph view when the Clear button is clicked.
        '''
        self._graph_controller.clear_graph()
        # TODO: add an info popup

    def disable_clear_button(self) -> None:
        '''
        Disables the Clear button, preventing the user from interacting with it.
        '''
        self._clear_button.set_enabled(False)
        
    def disable_save_button(self) -> None:
        '''
        Disables the Save button, preventing the user from interacting with it.
        '''
        self._save_button.set_enabled(False)
        
