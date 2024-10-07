import pygame
from constants.Colors import Colors

class ParametersView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants
        '''
        self.screen.fill(self.background_color)
        self.draw_button("save", [10, 10])
        self.draw_button("import", [170, 10])
        self.draw_button("clear", [330, 10])

    def draw_button(self, title, coordinates) -> None:
        '''
        Cette méthode dessine un bouton générique, dont les propriétés doivent être renseignées en paramètres de méthode.
        TODO : Modifier en une méthode générique
        '''
        font = pygame.font.Font(None, 24)
        button_surface = pygame.Surface((150, 50), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))
        text = font.render(title, True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))


        button_rect = pygame.Rect(coordinates[0], coordinates[1], 150, 50)
        pygame.draw.rect(button_surface, Colors.BUTTON.value, (0, 0, 150, 50), border_radius=10)

        button_surface.blit(text, text_rect)
        self.screen.blit(button_surface, (button_rect.x, button_rect.y))
    
    
