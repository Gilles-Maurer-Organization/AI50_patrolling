import pygame

from controllers.ScrollingListController import ScrollingListController
from constants.Config import GRAPH_WINDOW_WIDTH
from models.Algorithm import Algorithm
from models.TextBox import TextBox
from views.TextBoxView import TextBoxView

class AlgorithmParametersController:
    def __init__(self, parameters_view) -> None:
        self.parameters_view = parameters_view
        self.text_box_views = {} 
        self.algorithm = None

    def handle_selected_algorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm
        self.text_box_views = {}
        offset_y = 0
        for parameter in algorithm.parameters:
            text_box_view = TextBoxView(self.parameters_view.screen, 10, 160 + offset_y, 190, 40)
            self.text_box_views[parameter] = text_box_view
            offset_y += 50

    def is_text_box_text_completed(self, parameter) -> bool:
        return parameter.default_text != parameter.text_content

    def is_text_box_hovered(self, event, text_box_view) -> bool:
        '''
        Vérifie si la souris est sur une zone de texte spécifique.
        '''
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if text_box_view.text_box_rect:
            return text_box_view.text_box_rect.collidepoint(mouse_pos)
        return False

    def handle_algorithm_parameters(self, event):
        '''
        Gère les événements pour chaque zone de texte dans text_box_views.
        '''
        if self.algorithm is None:
            return

        for parameter, text_box_view in self.text_box_views.items():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_text_box_hovered(event, text_box_view):
                    parameter.active = True
                    text_box_view.set_clicked()
                else:
                    parameter.active = False
                    text_box_view.set_normal()

            if event.type == pygame.MOUSEMOTION and not parameter.active:
                if self.is_text_box_hovered(event, text_box_view):
                    text_box_view.set_hovered()
                else:
                    text_box_view.set_normal()

            if event.type == pygame.KEYDOWN and parameter.active:
                if parameter.first_input and event.unicode.isdigit():
                    parameter.reset()

                if event.key == pygame.K_BACKSPACE:
                    parameter.handle_backspace()
                elif event.unicode.isdigit():
                    parameter.add_character(event.unicode)

            text_box_view.change_text(parameter.text_content)
            text_box_view.set_text_completed(self.is_text_box_text_completed(parameter))

    def draw_parameters(self):
        for text_box_view in self.text_box_views.values():
            text_box_view.draw()