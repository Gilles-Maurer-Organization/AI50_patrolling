import pygame

from constants.Config import GRAPH_WINDOW_WIDTH
from constants.Colors import Colors

from models.algorithms.Algorithm import Algorithm

class ScrollingListView:
    def __init__(self, screen, x, y, width, height) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = Colors.BUTTON.value
        self.text_color = Colors.TEXT_BOX_TEXT.value

        self.font = pygame.font.SysFont("Arial", 16)
        self.scrolling_list_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.icon_path = 'assets/scrolling_icon.png'

        self.icon = pygame.image.load(self.icon_path)
        self.icon = pygame.transform.scale(self.icon, (20, 20))
        self.flipped_icon = pygame.transform.flip(self.icon, False, True)

        self.is_active = False
        self.options_rects = []

    def draw(self, algorithms: list[Algorithm], selected_algorithm = None, has_an_algorithm_selected: bool = False) -> None:
        '''
        Cette méthode dessine les caractéristiques de la liste déroulante : header et options de la liste déroulante
        dans le cas où celle-ci est active (déroulée).
        '''
        if has_an_algorithm_selected:
            self.change_header_text_color()
        self.draw_list_header(selected_algorithm)

        if self.is_active:
            self.draw_options(algorithms)
    
    def draw_list_header(self, selected_algorithm = None):
        '''
        Cette méthode dessine le header de la liste déroulante.

        Args:
            selected_algorithm (string): L'algorithme sélectionné dans la liste déroulante, peut être Null.
        '''
        pygame.draw.rect(self.screen, self.color, self.scrolling_list_rect, border_radius=6)
        text = self.font.render(selected_algorithm.name if selected_algorithm else 'Select algorithm', True, self.text_color)

        # Si la liste déroulante est déroulée, on réalise un miroir sur horizontal pour inverser le sens de la flèche
        icon_to_draw = self.flipped_icon if self.is_active else self.icon

        icon_x = self.width - icon_to_draw.get_width() - 10
        icon_y = (self.height - icon_to_draw.get_height()) // 2
        self.screen.blit(icon_to_draw, (self.x + icon_x, self.y + icon_y))

        text_rect = text.get_rect(center=(self.x + self.width / 2 - icon_to_draw.get_width() / 2, self.y + self.height / 2))
        self.screen.blit(text, text_rect)

    def draw_options(self, algorithms: list[Algorithm]) -> None:
        '''
        Cette méthode affiche les options de la liste déroulante sous la tête de liste.
        '''
        option_height = 40
        self.options_rects = []

        for i, option in enumerate(algorithms):
            option_name = option.name
            option_rect = pygame.Rect(self.x, self.y + (i + 1) * option_height, self.width, option_height)
            self.options_rects.append(option_rect)
            pygame.draw.rect(self.screen, Colors.LIGHT_GRAY.value, option_rect)
            text = self.font.render(option_name, True, Colors.BLACK.value)
            text_rect = text.get_rect(center=(option_rect.x + option_rect.width / 2, option_rect.y + option_rect.height / 2))
            self.screen.blit(text, text_rect)

    def change_header_text_color(self) -> None:
        '''
        Cette méthode change la couleur du texte du header de la liste déroulante.
        Elle est utilisée lorsqu'un algorithme est sélectionné par l'utilisateur.
        '''
        self.text_color = Colors.BLACK.value

    def is_option_clicked(self, event, algorithms: list[str]) -> str | None:
        '''
        Cette méthode vérifie si une option a été cliquée et renvoie le texte de l'option.

        Args:
            event: L'événement Pygame contenant des informations sur les coordonnées de la souris.
            algorithms (list[str]) : la liste des algorithmes disponibles stockés côté modèle.
        '''

        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        for rect, option in zip(self.options_rects, algorithms):
            if rect.collidepoint(mouse_pos):
                return option
        return None

    def set_active(self, is_active: bool) -> None:
        '''
        Cette méthode active ou désactive l'état déroulant de la liste.

        Args:
            is_active (bool): L'état de la liste déroulante, active (déroulée) ou non.
        '''
        self.is_active = is_active
        self.color = Colors.TEXT_BOX_CLICKED.value if is_active else Colors.BUTTON.value

    def set_selected_option(self, option: str) -> None:
        '''
        Cette méthode définit l'option sélectionnée dans la liste déroulante.
        '''
        self.selected_option = option
        self.is_active = False

    def set_hovered(self) -> None:
        '''
        Cette méthode change l'état de la liste déroulante en état survolé.
        '''
        self.color = Colors.BUTTON_HOVER.value

    def set_clicked(self) -> None:
        '''
        Cette méthode change l'état de la liste déroulante en état cliqué.
        '''
        self.color = Colors.TEXT_BOX_CLICKED.value
        self.stroke_color = Colors.BLACK.value

    def set_normal(self) -> None:
        '''
        Cette méthode change l'état de la liste déroulante en état non survolé ou non cliqué.
        '''
        self.color = Colors.BUTTON.value
        self.stroke_color = Colors.GRAY_TEXT.value