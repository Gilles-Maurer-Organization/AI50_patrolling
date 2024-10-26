import pygame
from constants.Colors import Colors

class ButtonView:
    def __init__(self, screen, text: str, action, x, y, width, height, icon_path = None, color: Colors = Colors.BUTTON, hover_color: Colors = Colors.BUTTON_HOVER) -> None:
        self.screen = screen
        self.text = text
        self.text_color = Colors.BLACK
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.hovered = False

        self.hover_color = hover_color
        self.normal_color = color

        self.disabled_color = Colors.BUTTON_DISABLED  # Color when disabled
        self.text_disabled_color = Colors.GRAY_TEXT  # Text color when disabled

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 16)

        if icon_path:
            self.icon = pygame.image.load(icon_path)
            self.icon = pygame.transform.scale(self.icon, (20, 20))
        else:
            self.icon = None


    def draw(self, enabled: bool) -> None:
        '''
        Cette méthode dessine un bouton générique à une position spécifiée avec une largeur et une hauteur données.
        
        Args:
            text (str): Le texte à afficher sur le bouton.
            coordinates (tuple de int): Un tuple (x, y) représentant les coordonnées du coin supérieur gauche du bouton.
            width (int): La largeur du bouton.
            height (int): La hauteur du bouton.
        '''
        
        self.update_colors(enabled)
        
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(button_surface, self.color.value, (0, 0, self.width, self.height), border_radius=6)

        # On dessine le icon s'il existe
        if self.icon:
            icon_x = 10
            icon_y = (self.height - self.icon.get_height()) // 2

            button_surface.blit(self.icon, (icon_x, icon_y))

        text = self.font.render(self.text, True, self.text_color.value)
        text_rect = text.get_rect(center=(self.width / 2 + (self.icon.get_width() if self.icon else 0) / 2, self.height / 2))

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
    
    def update_colors(self, enabled: bool) -> None:
        '''
        Cette méthode met à jour les couleurs du bouton en fonction de son état.
        '''
        if not enabled:
            self.color = self.disabled_color
            self.text_color = self.text_disabled_color
        elif self.hovered:
            self.color = self.hover_color
            self.text_color = Colors.BLACK
        else:
            self.color = self.normal_color
            self.text_color = Colors.BLACK

    def set_hovered(self) -> None:
        '''
        Cette méthode change l'état du bouton en état survolé.
        '''
        self.color = self.hover_color
        self.hovered = True

    def set_normal(self) -> None:
        '''
        Cette méthode change l'état du bouton en état non survolé.
        '''
        self.color = self.normal_color
        self.hovered = False

    