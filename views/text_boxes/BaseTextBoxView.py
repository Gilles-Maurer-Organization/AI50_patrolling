import pygame
from abc import ABC, abstractmethod
from constants.Colors import Colors

class BaseTextBoxView(ABC):
    def __init__(self, screen, x, y, width, height) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = Colors.BUTTON.value
        self.text_color = Colors.TEXT_BOX_TEXT.value
        self.stroke_color = Colors.GRAY_TEXT.value

        self.font = pygame.font.SysFont("Arial", 16)
        self.text_box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_box_content = None

    def draw(self) -> None:
        '''
        Cette méthode dessine une zone de texte à une position spécifiée avec une largeur et une hauteur données.
        '''
        text_box_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        border_surface = pygame.Surface((self.width + 2, self.height + 2), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(border_surface, self.stroke_color, (0, 0, self.width + 2, self.height + 2), border_radius=6)
        self.screen.blit(border_surface, (self.x - 1, self.y - 1))

        pygame.draw.rect(text_box_surface, self.color, (0, 0, self.width, self.height), border_radius=6)

        self.draw_text(text_box_surface)

        self.screen.blit(text_box_surface, (self.x, self.y))

    @abstractmethod
    def draw_text(self, surface):
        '''
        Méthode abstraite pour dessiner le texte dans la zone de texte.
        
        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le texte.
        '''
        pass

    def change_text(self, new_text):
        '''
        Cette méthode modifie le texte de la zone de texte en relation avec les informations envoyées par le contrôleur depuis la source du Model.
        
        Args:
            new_text (string): le nouveau texte envoyé à la vue.
        '''
        self.text_box_content = new_text

    def set_hovered(self) -> None:
        '''
        Cette méthode change l'état de la zone de texte en état survolé.
        '''
        self.color = Colors.BUTTON_HOVER.value

    def set_clicked(self) -> None:
        '''
        Cette méthode change l'état de la zone de texte en état cliqué.
        '''
        self.color = Colors.TEXT_BOX_CLICKED.value
        self.stroke_color = Colors.BLACK.value

    def set_normal(self) -> None:
        '''
        Cette méthode change l'état de la zone de texte en état non survolé ou non cliqué.
        '''
        self.color = Colors.BUTTON.value
        self.stroke_color = Colors.GRAY_TEXT.value

    def set_text_completed(self, is_completed: bool) -> None:
        '''
        Cette méthode change la couleur du texte de la zone de texte dans le cas où celle-ci
        est soit complétée par l'utilisateur, soit vide.
        '''
        self.text_color = Colors.BLACK.value if is_completed else Colors.TEXT_BOX_TEXT.value
