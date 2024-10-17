import pygame
from constants.Colors import Colors
from views.TextBoxView import TextBoxView
from views.ButtonView import ButtonView

class ParametersView:
    def __init__(self, screen, button_controllers) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

        self.button_controllers = button_controllers
        self.text_box = TextBoxView(self.screen, 10, 60, 240, 40)


    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants
        '''
        self.screen.fill(self.background_color)

        # Dessin des premiers boutons
        for controller in self.button_controllers:
            controller.view.draw()

        # Dessin de la zone de texte
        self.text_box.draw()

    def handle_events(self, event) -> None:
        for controller in self.button_controllers:
            controller.handle_event(event)
