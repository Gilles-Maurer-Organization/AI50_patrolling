from constants.Colors import Colors
import pygame

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
        self.scrolling_list_content = None

        self.icon_path = 'assets/scrolling_icon.png'

        self.icon = pygame.image.load(self.icon_path)
        self.icon = pygame.transform.scale(self.icon, (20, 20))

        self.is_active = False
        self.selected_option = None
        self.options_rects = []

    def draw(self, algorithms: list[str]) -> None:
            self.draw_list_header()

            if self.is_active:
                self.draw_options(algorithms)
    
    def draw_list_header(self):
        pygame.draw.rect(self.screen, self.color, self.scrolling_list_rect, border_radius=6)
        text = self.font.render(self.selected_option if self.selected_option else 'Select algorithm', True, self.text_color)

        logo_x = self.width - self.icon.get_width() - 10
        logo_y = (self.height - self.icon.get_height()) // 2
        self.screen.blit(self.icon, (self.x + logo_x, self.y + logo_y))

        text_rect = text.get_rect(center=(self.x + self.width / 2 - self.icon.get_width() / 2, self.y + self.height / 2))
        self.screen.blit(text, text_rect)

    def draw_options(self, algorithms: list[str]) -> None:
        '''
        Affiche les options de la liste déroulante sous la tête de liste.
        '''
        option_height = 40
        self.options_rects = []

        for i, option in enumerate(algorithms):
            option_rect = pygame.Rect(self.x, self.y + (i + 1) * option_height, self.width, option_height)
            self.options_rects.append(option_rect)
            pygame.draw.rect(self.screen, Colors.BUTTON.value, option_rect, border_radius=6)
            text = self.font.render(option, True, Colors.TEXT_BOX_TEXT.value)
            text_rect = text.get_rect(center=(option_rect.x + option_rect.width / 2, option_rect.y + option_rect.height / 2))
            self.screen.blit(text, text_rect)

    def is_option_clicked(self, event_pos) -> str:
        '''
        Vérifie si une option a été cliquée et renvoie le texte de l'option.
        '''
        for rect, option in zip(self.options_rects, self.scrolling_list_content):
            if rect.collidepoint(event_pos):
                return option
        return None

    def set_active(self, is_active: bool) -> None:
        '''
        Active ou désactive l'état déroulant de la liste.
        '''
        self.is_active = is_active
        self.color = Colors.BUTTON_HOVER.value if is_active else Colors.BUTTON.value

    def set_selected_option(self, option: str) -> None:
        '''
        Définit l'option sélectionnée dans la liste déroulante.
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