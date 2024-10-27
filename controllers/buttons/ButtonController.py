from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH

from models.Button import Button
from controllers.buttons.BaseButtonController import BaseButtonController
from views.ButtonView import ButtonView
import pygame

class ButtonController(BaseButtonController):
    def __init__(self, parameters_view, graph_controller) -> None:
        super().__init__(parameters_view, graph_controller)

        self.save_button = Button("Save", self.save_action)
        self.import_button = Button("Import", self.import_action)
        self.clear_button = Button("Clear", self.clear_action)

        # Création de la map des boutons et leurs vues
        self.button_map = {
            self.save_button: ButtonView(
                parameters_view.screen,
                self.save_button.text,
                self.save_button.action,
                10,
                10,
                90,
                40,
                icon_path='assets/save.png'
            ),
            self.import_button: ButtonView(
                parameters_view.screen,
                self.import_button.text,
                self.import_button.action,
                110,
                10,
                90,
                40,
                icon_path='assets/import.png'
            ),
            self.clear_button: ButtonView(
                parameters_view.screen,
                self.clear_button.text,
                self.clear_button.action,
                210,
                10,
                90,
                40,
                color=Colors.BUTTON_RED,
                hover_color=Colors.BUTTON_RED_HOVER
            )
        }

    def draw_buttons(self) -> None:
        '''
        Cette méthode dessine l'intégralité des boutons sur la vue.
        '''
        for button, button_view in self.button_map.items():
            button_view.draw(button.is_enabled())

    def handle_event(self, event) -> None:
        '''
        Gère l'événement de clic sur les boutons.

        Cette méthode vérifie si l'événement reçu correspond à un clic gauche de souris. 
        Si tel est le cas, elle déclenche l'action associée au bouton sur lequel l'utilisateur a cliqué.

        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
            for button, button_view in self.button_map.items():
                if button_view.is_hovered(mouse_pos):
                    button.action()
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
            for button_view in self.button_map.values():
                if button_view.is_hovered(mouse_pos):
                    button_view.set_hovered()
                else:
                    button_view.set_normal()

    def save_action(self) -> None:
        '''
        Cette méthode sauvegarde un graphe sur l'ordinateur lorsque le bouton Save est cliqué.
        '''
        self.graph_controller.save_graph()
        print("Save action triggered")

    def import_action(self) -> None:
        '''
        Cette méthode importe un graphe depuis l'ordinateur lorsque le bouton Import est cliqué.
        TODO : remplacer load_graph(1) par le graphe correspondant
        '''
        #self.graph_controller.load_graph(1)
        print("Import action triggered")

    def clear_action(self) -> None:
        '''
        Cette méthode nettoie l'intégralité de la vue du graphe lorsque le bouton Clear est cliqué.
        '''
        self.graph_controller.clear_graph()
        print("Clear action triggered")

    def disable_clear_button(self) -> None:
        self.clear_button.set_enabled(False)
        
    def disable_save_button(self) -> None:
        self.save_button.set_enabled(False)
        
