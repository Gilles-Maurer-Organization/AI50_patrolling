from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from views.ButtonView import ButtonView

from constants.Colors import Colors

class StartButtonController(BaseButtonController):
    def __init__(self, parameters_view, graph_controller) -> None:
        super().__init__(parameters_view, graph_controller)

        self.start_button = Button("Start simulation", self.start_action, enabled=False)

        # Création de la map des boutons et leurs vues
        self.button_map = {
            self.start_button: ButtonView(
                parameters_view.screen,
                self.start_button.text,
                self.start_button.action,
                160,
                490,
                140,
                40,
                color=Colors.BUTTON_GREEN,
                hover_color=Colors.BUTTON_GREEN_HOVER
            )
        }

    def start_action(self) -> None:
        '''
        Cette méthode lance le programme selon l'algorithme sélectionné.
        '''
        print("Starting algorithm")

    def enable_start_button(self) -> None:
        '''
        Cette méthode active le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(True)

    def disable_start_button(self) -> None:
        '''
        Cette méthode désactive le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(False)