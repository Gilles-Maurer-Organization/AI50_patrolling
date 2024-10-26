import pygame
from constants.Config import GRAPH_WINDOW_WIDTH

class BaseTextBoxController:
    def __init__(self, parameters_view):
        self.parameters_view = parameters_view
        # Clé : modèle (TextBox), Valeur : vue (TextBoxView)
        self.text_boxes = {}

    def add_text_box(self, model, text_box_view):
        '''
        Cette méthode associe un modèle de zone de texte (TextBox) à sa vue correspondante.
        '''
        self.text_boxes[model] = text_box_view

    def handle_event(self, event):
        '''
        Cette méthode gère les événements pour toutes les zones de texte enregistrées dans text_boxes.
        '''
        for model, view in self.text_boxes.items():
            # Si un clic est réalisé
            if event.type == pygame.MOUSEBUTTONDOWN:
                # On vérifie si ce dernier est sur la zone de texte
                if self.is_text_box_hovered(event, view):
                    model.active = True
                    # On indique à la vue que la zone de texte a été cliquée
                    view.set_clicked()
                else:
                    model.active = False
                    # On indique à la vue que la zone de texte n'est plus active
                    view.set_normal()

            # Gère le survol de la souris
            if event.type == pygame.MOUSEMOTION and not model.active:
                if self.is_text_box_hovered(event, view):
                    # On indique à la vue que la zone de texte est survolée
                    view.set_hovered()
                else:
                    # On indique à la vue que la zone de texte n'est pas survolée
                    # (réinitialisation en normal)
                    view.set_normal()

            # Gestion de l'entrée clavier si la zone de texte est active
            if event.type == pygame.KEYDOWN and model.active:
                # S'il s'agit de la première fois que la zone de texte est écrite et que la touche pressée est valide (un chiffre), on supprime le texte de base
                if model.first_input and event.unicode.isdigit():
                    model.reset()

                # Si la touche de suppression est touchée
                if event.key == pygame.K_BACKSPACE:
                    model.handle_backspace()
                # S'il ne s'agit pas de la touche de suppression, il ne peut s'agir que d'une touche de chiffre (digit)
                elif event.unicode.isdigit():
                    model.add_character(event.unicode)

            # Mise à jour du contenu de la zone de texte et de son état
            view.change_text(model.text_content)
            # On indique à la vue si la zone de texte est complétée ou non pour modifier la couleur du texte
            view.set_text_completed(self.is_text_box_text_completed(model))

    def is_text_box_text_completed(self, model) -> bool:
        '''
        Cette méthode vérifie si le contenu de la zone de texte est différent du texte par défaut.
        '''
        return model.default_text != model.text_content

    def is_text_box_hovered(self, event, text_box_view) -> bool:
        '''
        Cette méthode vérifie si la souris est située dans les limites de la zone de texte.
        '''
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if text_box_view.text_box_rect:
            return text_box_view.text_box_rect.collidepoint(mouse_pos)
        return False

    def draw_text_boxes(self):
        '''
        Cette méthode dessine toutes les zones de texte enregistrées dans text_boxes.
        '''
        for text_box in self.text_boxes.values():
            text_box.draw()