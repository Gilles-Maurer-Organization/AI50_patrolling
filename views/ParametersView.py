import pygame

from constants.Colors import Colors

class ParametersView:
    """
    This class represents the parameters view of the application.

    Attributes:
        _screen (pygame.Surface): The surface on which the view elements are
            drawn.
        _background_color (pygame.Color): The background color of the
            parameters view.

    Methods:
        draw() -> None:
            Renders the parameters view with the UI elements
            (without specific elements).
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._background_color = Colors.WHITE.value

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    def draw(self) -> None:
        """
        Renders the parameters view with a background color.

        This method fills the screen with the background color.
        """
        self._screen.fill(self._background_color)