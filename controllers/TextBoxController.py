import pygame
from models.TextBox import TextBox

class TextBoxController:
    def __init__(self, parameters_view):
        self.parameters_view = parameters_view

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
            if self.is_click_in_text_box(event):
                self.text_box.active = True
            else:
                self.text_box.active = False

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
            
        self.parameters_view.text_box.change_text(self.text_box.text_content)

    def is_click_in_text_box(self, event):
        '''
        Cette méthode vérifie si le clic de souris réalisé est situé dans les limites de la zone de texte.

        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        # Ajout de l'offset 960 (largeur de la fenetre de graphe)
        # TODO: Modifier par une variable globale de largeur de la fenêtre
        mouse_pos = (event.pos[0] - 960, event.pos[1])
        if self.parameters_view.text_box.text_box_rect:
            return self.parameters_view.text_box.text_box_rect.collidepoint(mouse_pos)
        return False