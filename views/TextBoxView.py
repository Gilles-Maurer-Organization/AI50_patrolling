import pygame
from constants.Colors import Colors

class TextBoxView:
    def __init__(self, screen, x, y, width, height, logo_path = None) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.logo_path = logo_path

        self.font = pygame.font.SysFont("Arial", 16)
        self.text_box_rect = None
        self.text_box_content = None

        if logo_path:
            self.logo = pygame.image.load(logo_path)
            self.logo = pygame.transform.scale(self.logo, (20, 20))
        else:
            self.logo = None

    def draw(self) -> None:
        '''
        Cette méthode dessine une zone de texte à une position spécifiée avec une largeur et une hauteur données.

        La zone de texte affichera le contenu actuel de la variable `text_box_content`, qui peut être modifié par
        l'utilisateur via des événements clavier gérés par le contrôleur associé.
        '''
        text_box_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        border_surface = pygame.Surface((self.width + 2, self.height + 2), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(border_surface, Colors.BLACK.value, (0, 0, self.width + 2, self.height + 2), border_radius=6)

        self.screen.blit(border_surface, (self.x - 1, self.y - 1))

        pygame.draw.rect(text_box_surface, Colors.BUTTON.value, (0, 0, self.width, self.height), border_radius=6)

        if self.logo:
            logo_x = 10
            logo_y = (self.height - self.logo.get_height()) // 2

            text_box_surface.blit(self.logo, (logo_x, logo_y))

        text = self.font.render(self.text_box_content, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width / 2 + (self.logo.get_width() if self.logo else 0) / 2, self.height / 2))

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