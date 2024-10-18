from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH

from models.Button import Button
from views.ButtonView import ButtonView
import pygame

class ButtonController:
    def __init__(self, parameters_view, graph_controller) -> None:
        self.parameters_view = parameters_view
        self.graph_controller = graph_controller

        # Création des modèles de boutons, 1 de chaque type (save, import, clear)
        self.buttons = [
            Button("Save", self.save_action),
            Button("Import", self.import_action),
            Button("Clear", self.clear_action),
            Button("Start simulation", self.start_action)
        ]
        
        # Création des vues de chaque bouton
        self.button_views = [
            ButtonView(
                parameters_view.screen,
                self.buttons[0].text,
                self.buttons[0].action,
                10,
                10,
                90,
                40,
                icon_path = 'assets/save.png'
            ),
            ButtonView(
                parameters_view.screen,
                self.buttons[1].text,
                self.buttons[1].action,
                110,
                10,
                90,
                40,
                icon_path = 'assets/import.png'
            ),
            ButtonView(
                parameters_view.screen,
                self.buttons[2].text,
                self.buttons[2].action,
                210,
                10,
                90,
                40,
                icon_path = 'assets/clear.png',
                color = Colors.BUTTON_RED,
                hover_color=Colors.BUTTON_RED_HOVER
            ),
            ButtonView(
                parameters_view.screen,
                self.buttons[3].text,
                self.buttons[3].action,
                160,
                490,
                140,
                40,
                color = Colors.BUTTON_GREEN,
                hover_color=Colors.BUTTON_GREEN_HOVER
            ),
        ]

    def draw_buttons(self) -> None:
        '''
        Cette méthode dessine l'intégralité des boutons sur la vue.
        '''
        for button_view in self.button_views:
            button_view.draw()

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
            for button, button_view in zip(self.buttons, self.button_views):
                if button_view.is_hovered(mouse_pos):
                    button.action()
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
            for button_view in self.button_views:
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
        '''
        self.graph_controller.load_graph(1)
        print("Import action triggered")

    def clear_action(self) -> None:
        '''
        Cette méthode nettoie l'intégralité de la vue du graphe lorsque le bouton Clear est cliqué.
        '''
        self.graph_controller.clear_graph()
        print("Clear action triggered")

    def start_action(self) -> None:
        '''
        Cette méthode lance le programme selon l'algorithme sélectionné.
        '''
        print("Starting algorithm")
