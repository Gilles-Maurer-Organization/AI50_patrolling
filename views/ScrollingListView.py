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
        self.scrolling_list_rect = None
        self.scrolling_list_content = None

        self.icon_path = 'assets/scrolling_icon.png'

        self.icon = pygame.image.load(self.icon_path)
        self.icon = pygame.transform.scale(self.icon, (20, 20))

    def draw(self) -> None:
        scrolling_list_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        border_surface = pygame.Surface((self.width + 2, self.height + 2), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(scrolling_list_surface, self.color, (0, 0, self.width, self.height), border_radius=6)

        logo_x = self.width - self.icon.get_width() - 10
        logo_y = (self.height - self.icon.get_height()) // 2

        scrolling_list_surface.blit(self.icon, (logo_x, logo_y))

        text = self.font.render(self.scrolling_list_content, True, self.text_color)
        text_rect = text.get_rect(center=(self.width / 2 + (self.icon.get_width() if self.icon else 0) / 2, self.height / 2))

        scrolling_list_surface.blit(text, text_rect)

        self.scrolling_list_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.screen.blit(scrolling_list_surface, [self.x, self.y])

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