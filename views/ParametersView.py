import pygame
from constants.Colors import Colors
from views.TextBoxView import TextBoxView

class ParametersView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

        self.font = pygame.font.Font(None, 24)
        self.text_box = TextBoxView(self.screen, 10, 60, 240, 40)

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants
        '''
        self.screen.fill(self.background_color)

        # Dessin des premiers boutons
        self.draw_button("save", [10, 10], 110, 40)
        self.draw_button("import", [130, 10], 120, 40)
        self.draw_button("clear", [260, 10], 120, 40)

        # Dessin de la zone de texte
        self.text_box.draw()

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
    
    
