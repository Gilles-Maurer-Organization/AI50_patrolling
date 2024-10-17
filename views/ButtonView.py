import pygame
from constants.Colors import Colors

class ButtonView:
    def __init__(self, screen, text: str, action, x, y, width, height) -> None:
        self.screen = screen
        self.text = text
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 16)

    def draw(self) -> None:
        '''
        Cette méthode dessine un bouton générique à une position spécifiée avec une largeur et une hauteur données.

        Args:
            text (str): Le texte à afficher sur le bouton.
            coordinates (tuple de int): Un tuple (x, y) représentant les coordonnées du coin supérieur gauche du bouton.
            width (int): La largeur du bouton.
            height (int): La hauteur du bouton.
        '''
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))

        pygame.draw.rect(button_surface, Colors.BUTTON.value, (0, 0, self.width, self.height), border_radius=10)

        button_surface.blit(text, text_rect)
        self.screen.blit(button_surface, (self.rect.x, self.rect.y))
    
    def is_clicked(self, mouse_pos) -> bool:
        '''
        Vérifie si le bouton a été cliqué.

        Cette méthode détermine si la position de la souris, passée en argument,
        se trouve à l'intérieur des limites du bouton. Elle retourne True si
        le bouton est cliqué, sinon False.
        '''
        return self.rect.collidepoint(mouse_pos)

    