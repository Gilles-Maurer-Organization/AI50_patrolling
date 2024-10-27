from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH

from models.Button import Button
from views.ButtonView import ButtonView
import pygame

class BaseButtonController:
    def __init__(self, parameters_view, graph_controller) -> None:
        self.parameters_view = parameters_view
        self.graph_controller = graph_controller

        # Création de la map des boutons et leurs vues
        self.button_map = {}

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
                if button_view.is_hovered(mouse_pos) and button.is_enabled():
                    button.action()
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
            for button_view in self.button_map.values():
                if button_view.is_hovered(mouse_pos):
                    button_view.set_hovered()
                else:
                    button_view.set_normal()
