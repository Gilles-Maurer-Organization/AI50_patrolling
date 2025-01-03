import pygame

from constants.Colors import Colors
from constants.Config import PARAMETERS_WINDOW_WIDTH

class IdlenessView:
    
    def __init__(
        self,
        screen: pygame.Surface
        
    ) -> None:
        self._screen = screen
        self._label_average_idleness_value = 0
        self._label_max_idleness_value = 0
        self._label_ath_idleness_value = 0
        self._title_font = pygame.font.SysFont("Arial", 20)
        self._name_font = pygame.font.SysFont("Arial", 14)
        self._value_font = pygame.font.SysFont("Arial", 16)

    def update_values(self, 
        average_idleness: float, 
        max_idleness: float, 
        ath_idleness: float
    ) -> None:
        """
        Updates the values of average, max and all-tim highest idleness in the view.
        """
        self._label_average_idleness_value = round(average_idleness, 2)
        self._label_max_idleness_value = max_idleness
        self._label_ath_idleness_value = ath_idleness

        
    def draw_text(self) -> None:
        """
        Draws the idleness statistics on the Simulation Data View.
        """
        padding = 10
        border_radius = 6
        gray_color = Colors.FOG_GRAY.value
        text_color = Colors.BLACK.value
        section_height = 50

        element_width = (PARAMETERS_WINDOW_WIDTH - 3 * padding) // 2
        
        center_x = PARAMETERS_WINDOW_WIDTH // 2

        # Title (Centered)
        title_surface = self._title_font.render(
            "Simulation Statistics",
            True,
            text_color
        )

        title_rect = title_surface.get_rect(center=(center_x, padding * 2))
        self._screen.blit(title_surface, title_rect)

        current_y = title_rect.bottom + padding * 2

        def draw_stat_block(
            label: str,
            value: str,
            x: int,
            y: int,
            width: int
        ) -> None:
            block_height = section_height + padding
            rect = pygame.Rect(x, y, width, block_height)
            pygame.draw.rect(self._screen, gray_color, rect, border_radius=border_radius)

            label_surface = self._name_font.render(label, True, text_color)
            value_surface = self._value_font.render(value, True, text_color)

            label_rect = label_surface.get_rect(midtop=(rect.centerx, rect.top + padding))
            value_rect = value_surface.get_rect(midtop=(rect.centerx, label_rect.bottom + padding))

            self._screen.blit(label_surface, label_rect)
            self._screen.blit(value_surface, value_rect)

        # Average Idleness (Left)
        draw_stat_block(
            "Average idleness",
            str(self._label_average_idleness_value),
            padding,
            current_y,
            element_width
        )

        # Maximum Idleness (Right)
        draw_stat_block(
            "Maximum idleness",
            str(self._label_max_idleness_value),
            element_width + 2 * padding,
            current_y,
            element_width
        )

        current_y += section_height + padding * 2

        # All-time Highest Idleness (Full Width)
        draw_stat_block(
            "All-time highest idleness",
            str(self._label_ath_idleness_value),
            padding,
            current_y,
            PARAMETERS_WINDOW_WIDTH - 2 * padding
        )