import pygame
from constants.Colors import Colors

class ButtonView:
    def __init__(self, screen, text: str, action, x, y, width, height, logo_path = None, color: Colors = Colors.BUTTON, hover_color: Colors = Colors.BUTTON_HOVER) -> None:
        self.screen = screen
        self.text = text
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.hover_color = hover_color
        self.normal_color = color

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 16)

        if logo_path:
            self.logo = pygame.image.load(logo_path)
            self.logo = pygame.transform.scale(self.logo, (20, 20))
        else:
            self.logo = None

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

        pygame.draw.rect(button_surface, self.color.value, (0, 0, self.width, self.height), border_radius=6)

        # On dessine le logo s'il existe
        if self.logo:
            logo_x = 10
            logo_y = (self.height - self.logo.get_height()) // 2

            button_surface.blit(self.logo, (logo_x, logo_y))

        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width / 2 + (self.logo.get_width() if self.logo else 0) / 2, self.height / 2))

        button_surface.blit(text, text_rect)

        self.screen.blit(button_surface, (self.rect.x, self.rect.y))

    
    def is_hovered(self, mouse_pos) -> bool:
        '''
        Vérifie si le bouton a été survolé.

        Cette méthode détermine si la position de la souris, passée en argument,
        se trouve à l'intérieur des limites du bouton. Elle retourne True si
        le bouton est survolé, sinon False.
        '''
        return self.rect.collidepoint(mouse_pos)
    
    def set_hovered(self) -> None:
        '''
        Cette méthode change l'état du bouton en état survolé.
        '''
        self.color = self.hover_color

    def set_normal(self) -> None:
        '''
        Cette méthode change l'état du bouton en état non survolé.
        '''
        self.color = self.normal_color

    