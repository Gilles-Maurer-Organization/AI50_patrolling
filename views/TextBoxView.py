import pygame
from constants.Colors import Colors

class TextBoxView:
    def __init__(self, screen, x, y, width, height, logo_path = None) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = Colors.BUTTON.value
        self.normal_color = self.color
        self.hover_color = Colors.BUTTON_HOVER.value
        self.click_color = Colors.TEXT_BOX_CLICKED.value

        self.text_color = Colors.TEXT_BOX_TEXT.value
        self.text_color_uncompleted = Colors.TEXT_BOX_TEXT.value
        self.text_color_completed = Colors.BLACK.value

        self.stroke_color = Colors.GRAY_TEXT.value

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

        pygame.draw.rect(border_surface, self.stroke_color, (0, 0, self.width + 2, self.height + 2), border_radius=6)

        self.screen.blit(border_surface, (self.x - 1, self.y - 1))

        pygame.draw.rect(text_box_surface, self.color, (0, 0, self.width, self.height), border_radius=6)

        if self.logo:
            logo_x = 10
            logo_y = (self.height - self.logo.get_height()) // 2

            text_box_surface.blit(self.logo, (logo_x, logo_y))

        text = self.font.render(self.text_box_content, True, self.text_color)
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
    
    def set_hovered(self) -> None:
        '''
        Cette méthode change l'état de la textbox en état survolé.
        '''
        self.color = self.hover_color

    def set_clicked(self) -> None:
        '''
        Cette méthode change l'état de la textbox en état cliqué.
        '''
        self.color = self.click_color
        self.stroke_color = Colors.BLACK.value

    def set_normal(self) -> None:
        '''
        Cette méthode change l'état de la textbox en état non survolé ou non cliqué.
        '''
        self.color = self.normal_color
        self.stroke_color = Colors.GRAY_TEXT.value

    def set_text_completed(self, is_completed: bool) -> None:
        self.text_color = self.text_color_completed if is_completed else self.text_color_uncompleted