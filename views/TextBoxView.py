import pygame
from constants.Colors import Colors

class TextBoxView:
    def __init__(self, screen, x, y, width, height) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.font = pygame.font.Font(None, 24)
        self.text_box_rect = None
        self.text_box_content = None

    def draw(self) -> None:
        '''
        Cette méthode dessine une zone de texte à une position spécifiée avec une largeur et une hauteur données.

        La zone de texte affichera le contenu actuel de la variable `text_box_content`, qui peut être modifié par
        l'utilisateur via des événements clavier gérés par le contrôleur associé.
        '''
        text_box_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        border_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(border_surface, Colors.GRAY_TEXT.value, (0, 0, self.width + 4, self.height + 4), border_radius=10)

        self.screen.blit(border_surface, (self.x - 2, self.y - 2))

        pygame.draw.rect(text_box_surface, Colors.BUTTON.value, (0, 0, self.width, self.height), border_radius=10)

        text = self.font.render(self.text_box_content, True, (0, 0, 0))
        text_rect = text.get_rect(center=(text_box_surface.get_width() / 2, text_box_surface.get_height() / 2))

        text_box_surface.blit(text, text_rect)

        self.text_box_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.screen.blit(text_box_surface, [self.x, self.y])


    def change_text(self, new_text):
        '''
        Cette méthode modifie le texte de la zone de texte en relation avec les informations envoyées par le contrôleur depuis la source du Model.
        
        Args:
            new_text (string): le nouveau texte envoyé à la vue.
        '''
        self.text_box_content = new_text