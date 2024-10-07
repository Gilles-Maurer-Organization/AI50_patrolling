import pygame
from constants.Colors import Colors

class ParametersView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value
        self.font = pygame.font.Font(None, 24)

        self.text_box_rect = None
        self.text_box_content = None

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants
        '''
        self.screen.fill(self.background_color)

        # Dessin des premiers boutons
        self.draw_button("save", [10, 10], 110, 40)
        self.draw_button("import", [130, 10], 120, 40)
        self.draw_button("clear", [260, 10], 120, 40)
        self.draw_button("clear", [10, 60], 120, 40)

        # Dessin de la zone de texte
        self.draw_text_box([10, 120], 240, 40)

    def draw_button(self, title: str, coordinates, width, height) -> None:
        '''
        Cette méthode dessine un bouton générique à une position spécifiée avec une largeur et une hauteur données.

        Args:
            title (str): Le texte à afficher sur le bouton.
            coordinates (tuple de int): Un tuple (x, y) représentant les coordonnées du coin supérieur gauche du bouton.
            width (int): La largeur du bouton.
            height (int): La hauteur du bouton.
        '''
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))
        text = self.font.render(title, True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))


        button_rect = pygame.Rect(coordinates[0], coordinates[1], width, height)
        pygame.draw.rect(button_surface, Colors.BUTTON.value, (0, 0, width, height), border_radius=10)

        button_surface.blit(text, text_rect)
        self.screen.blit(button_surface, (button_rect.x, button_rect.y))

    def draw_text_box(self, coordinates, width, height) -> None:
        '''
        Cette méthode dessine une zone de texte à une position spécifiée avec une largeur et une hauteur données.

        Args:
            coordinates (tuple de int): Un tuple (x, y) représentant les coordonnées du coin supérieur gauche de la zone de texte.
            width (int): La largeur de la zone de texte.
            height (int): La hauteur de la zone de texte.

        La zone de texte affichera le contenu actuel de la variable `text_box_content`, qui peut être modifié par
        l'utilisateur via des événements clavier gérés par le contrôleur associé.
        '''
        text_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(text_box_surface, Colors.BUTTON.value, (0, 0, width, height), border_radius=10)

        # Affichage du texte dans la zone
        text = self.font.render(self.text_box_content, True, (0, 0, 0))
        text_rect = text.get_rect(center=(text_box_surface.get_width()/2, text_box_surface.get_height()/2))

        # Ajout du texte dans la zone
        text_box_surface.blit(text, text_rect)

        # Stockage des informations de coordonnées et largeur/hauteur de la zone de texte afin de réaliser le texte de collision avec la souris dans le controleur
        self.text_box_rect = pygame.Rect(coordinates[0], coordinates[1], width, height)

        # Affichage de la zone de texte
        self.screen.blit(text_box_surface, coordinates)
    
    
