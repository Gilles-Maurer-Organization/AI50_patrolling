import pygame

from constants.Colors import Colors

class IdlenessView:
    
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        label_average_idleness_value : float,
        label_max_idleness_value : float,
        label_ath_idleness_value : float
        
    ) -> None:
        self._screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._label_average_idleness_value = label_average_idleness_value
        self._label_max_idleness_value = label_max_idleness_value
        self._label_ath_idleness_value = label_ath_idleness_value
        self._title_font = pygame.font.SysFont("Arial", 30)
        self._name_font = pygame.font.SysFont("Arial", 20)
        self._value_font = pygame.font.SysFont("Arial", 16)
        self._rect = pygame.Rect(
            self._x,
            self._y,
            self._width,
            self._height
        )

    def update_values(self, average_idleness: float, max_idleness: float, ath_idleness: float) -> None:
        """
        Updates the values of average and max idleness in the view.
        """
        self._label_average_idleness_value = average_idleness
        self._label_max_idleness_value = max_idleness
        self._label_ath_idleness_value = ath_idleness

        
    def draw_text(self) -> None:
        """
        Draws the idleness on the Simulation Data View.
        """

        #offsets
        title_offset = 10
        statistic_name_x_offset = 60
        statistic_value_x_offset = 123

        #---section Title
        label_text_surface = self._title_font.render(
            "Simulation statistics",
            True,
            Colors.BLACK.value
        )
        
        label_text_rect = label_text_surface.get_rect(topleft=(self._x+title_offset, self._y))
        self._screen.blit(label_text_surface, label_text_rect)

        #---Average idleness
        # -> Name
        label_text_surface = self._name_font.render(
            "Average idleness",
            True,
            Colors.BLACK.value
        )
        label_text_rect = label_text_surface.get_rect(topleft=(self._x+statistic_name_x_offset, self._y+75))
        self._screen.blit(label_text_surface, label_text_rect)

        # -> value
        label_value_surface = self._value_font.render(
            str(self._label_average_idleness_value),
            True,
            Colors.BLACK.value
        )
        label_value_rect = label_value_surface.get_rect(topleft=(self._x+statistic_value_x_offset-5, self._y+150))
        self._screen.blit(label_value_surface, label_value_rect)

        #---Max idleness
        # -> Name
        label_text_surface = self._name_font.render(
            "Maximum idleness",
            True,
            Colors.BLACK.value
        )
        label_text_rect = label_text_surface.get_rect(topleft=(self._x+statistic_name_x_offset-5, self._y+225))
        self._screen.blit(label_text_surface, label_text_rect)

        # -> value
        label_value_surface = self._value_font.render(
            str(self._label_max_idleness_value),
            True,
            Colors.BLACK.value
        )
        label_value_rect = label_value_surface.get_rect(topleft=(self._x+statistic_value_x_offset, self._y+300))
        self._screen.blit(label_value_surface, label_value_rect)
        
        #---all-time highest idleness
        # -> Name
        label_text_surface = self._name_font.render(
            "All-time highest idleness",
            True,
            Colors.BLACK.value
        )
        label_text_rect = label_text_surface.get_rect(topleft=(self._x+statistic_name_x_offset-20, self._y+375))
        self._screen.blit(label_text_surface, label_text_rect)

        # -> value
        label_value_surface = self._value_font.render(
            str(self._label_ath_idleness_value),
            True,
            Colors.BLACK.value
        )
        label_value_rect = label_value_surface.get_rect(topleft=(self._x+statistic_value_x_offset, self._y+450))
        self._screen.blit(label_value_surface, label_value_rect)

        

        