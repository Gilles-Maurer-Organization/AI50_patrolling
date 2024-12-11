import pygame

from constants.Colors import Colors

class SimulationDataView:
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._background_color = Colors.WHITE.value

    def draw(self) -> None:
        """
        Renders the simulation data view with a background color.

        This method fills the screen with the background color.
        """
        self._screen.fill(self._background_color)
        