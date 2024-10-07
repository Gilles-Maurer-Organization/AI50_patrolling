import pygame
from views.ParametersView import ParametersView

class TextBoxController:
    def __init__(self, parameters_view: ParametersView):
        self.parameters_view = parameters_view

        # TODO: modifier et ajouter ces propriétés dans un Model
        self.active = False
        self.first_input = True
        self.default_text = "Number of Agents"
        self.parameters_view.text_box_content = self.default_text

    def handle_event(self, event):
        '''
        Gère les événements liés à la zone de texte
        '''

        # Si un clic est réalisé
        if event.type == pygame.MOUSEBUTTONDOWN:
            # On vérifie si ce dernier est sur la zone de texte
            if self.is_click_in_text_box(event.pos):
                self.active = True
            else:
                self.active = False

        # Une fois la zone de texte active, on regarde si une touche a été pressée
        if event.type == pygame.KEYDOWN and self.active:

            # S'il s'agit de la première fois que la zone de texte est écrite et que la touche pressée est valide (un chiffre), on supprime le texte de base
            if self.first_input and event.unicode.isdigit():
                self.parameters_view.text_box_content = ""
                # On considère qu'il ne s'agit plus de la première saisie
                self.first_input = False

            # Si la touche de suppression est touchée
            if event.key == pygame.K_BACKSPACE:
                # On supprime le dernier caractère
                self.parameters_view.text_box_content = self.parameters_view.text_box_content[:-1]

                # Si le texte est vide après suppression de l'intégralité du texte, on remet le message par défaut
                if len(self.parameters_view.text_box_content) == 0:
                    self.parameters_view.text_box_content = self.default_text
                    # Il ne faut pas oublier de réinitialiser le first input pour la prochaine saisie
                    self.first_input = True
            else:
                # S'il ne s'agit pas de la touche de suppression, il ne peut s'agir que d'une touche de chiffre (digit)
                if event.unicode.isdigit():
                    # S'il s'agissait du texte par défaut, on le supprime
                    if self.parameters_view.text_box_content == self.default_text:
                        self.parameters_view.text_box_content = ""
                    # Et on ajoute nos chiffres à notre texte
                    self.parameters_view.text_box_content += event.unicode

    def is_click_in_text_box(self, mouse_pos):
        '''
        Vérifie si le clic de souris est dans la zone de texte
        '''
        
        # TODO: Recoder de manière plus propre
        mouse_pos_x = mouse_pos[0] - 960
        mouse_pos = (mouse_pos_x, mouse_pos[1])
        if self.parameters_view.text_box_rect:
            return self.parameters_view.text_box_rect.collidepoint(mouse_pos)
        return False