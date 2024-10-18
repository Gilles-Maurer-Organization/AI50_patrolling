import pygame
from models.TextBox import TextBox
from views.TextBoxView import TextBoxView

from constants.Config import GRAPH_WINDOW_WIDTH

class TextBoxController:
    def __init__(self, parameters_view):
        self.parameters_view = parameters_view

        self.text_box_view = TextBoxView(parameters_view.screen, 10, 60, 190, 40, icon_path='assets/number_agents.png')
        self.text_box = TextBox(default_text="Number of Agents")

    def handle_event(self, event):
        '''
        Cette méthode gère les événements liés à la zone de texte.

        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur avec le programme.
        '''

        # Si un clic est réalisé
        if event.type == pygame.MOUSEBUTTONDOWN:
            # On vérifie si ce dernier est sur la zone de texte
            if self.is_text_box_hovered(event):
                self.text_box.active = True
                # On indique à la vue que la zone de texte a été cliquée
                self.text_box_view.set_clicked()
            else:
                self.text_box.active = False
                # On indique à la vue que la zone de texte n'est plus active
                self.text_box_view.set_normal()

        if event.type == pygame.MOUSEMOTION:
            if self.text_box.active == False:
                if self.is_text_box_hovered(event):
                    # On indique à la vue que la zone de texte est survolée
                    self.text_box_view.set_hovered()
                else:
                    # On indique à la vue que la zone de texte n'est pas survolée
                    # (réinitialisation en normal)
                    self.text_box_view.set_normal()

        # Une fois la zone de texte active, on regarde si une touche a été pressée
        if event.type == pygame.KEYDOWN and self.text_box.active:
            # S'il s'agit de la première fois que la zone de texte est écrite et que la touche pressée est valide (un chiffre), on supprime le texte de base
            if self.text_box.first_input and event.unicode.isdigit():
                self.text_box.reset()

            # Si la touche de suppression est touchée
            if event.key == pygame.K_BACKSPACE:
                self.text_box.handle_backspace()
            # S'il ne s'agit pas de la touche de suppression, il ne peut s'agir que d'une touche de chiffre (digit)
            elif event.unicode.isdigit():
                self.text_box.add_character(event.unicode)
            
        self.text_box_view.change_text(self.text_box.text_content)
        # On indique à la vue si la zone de texte est complétée ou non pour modifier la couleur du texte
        self.text_box_view.set_text_completed(self.is_text_box_text_completed())

    def is_text_box_text_completed(self) -> bool:
        return self.text_box.default_text != self.text_box.text_content

    def is_text_box_hovered(self, event):
        '''
        Cette méthode vérifie si la souris est située dans les limites de la zone de texte.

        Args:
            event: L'événement Pygame contenant des informations sur les coordonnées de la souris.
        '''
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if self.text_box_view.text_box_rect:
            return self.text_box_view.text_box_rect.collidepoint(mouse_pos)
        return False

    def draw_text_box(self) -> None:
        self.text_box_view.draw()