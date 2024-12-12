import pygame
from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH

class CheckBoxView:
    """
    Represents the visual representation of a checkbox, including a label
    and the ability to draw it on the Parameters view.

    Attributes:
        _screen (pygame.Surface): The surface where the checkbox and label are
            drawn.
        _width (int): The width of the checkbox.
        _height (int): The height of the checkbox.
        _rect (pygame.Rect): The rectangle that defines the position and size of
            the checkbox.
        _label (str): The text to display next to the checkbox.
        _font (pygame.font.Font): The font used to render the label.
        _label_color (Colors): The color of the label.
        _color (Colors): The color of the checkbox when it is not clicked.
        _clicked_color (str): The color of the checkbox when it is clicked.
        _border_radius (int): The radius for rounded corners of the checkbox.
        _tick_image (pygame.Surface): The image representing a tick mark to be
            displayed when the checkbox is checked.
        _label_surface (pygame.Surface): The rendered surface for the label
            text.
        _label_rect (pygame.Rect): The rectangle defining the position of the
            label.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        clicked_color: str,
        label: str,
    ) -> None:
        self._screen = screen
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)
        self._label = label
        self._font = pygame.font.SysFont("Arial", 16)
        self._label_color = Colors.BLACK

        self._color = Colors.BUTTON
        self._clicked_color = clicked_color
        self._border_radius = 6

        self._tick_image = pygame.image.load("assets/checkbox/tick.png")
        self._tick_image = pygame.transform.scale(
            self._tick_image, (int(self._width * 0.5), int(self._height * 0.5))
        )
        self._label_surface = self._font.render(self._label, True, self._label_color.value)
        self._label_rect = self._label_surface.get_rect(midleft=(x + width + 10, y + height // 2))


    def draw(self, enabled: bool) -> None:
        """
        Draws the checkbox and its label on the screen.

        Args:
            enabled (bool): Whether the checkbox is checked (enabled) or not.
        """
        self._screen.blit(self._label_surface, self._label_rect)

        # Draw the main checkbox (a square with border-radius)
        pygame.draw.rect(
            self._screen,
            self._color.value,
            self._rect,
            border_radius=self._border_radius
        )

        # If clicked, draw a slightly smaller square inside the checkbox
        if enabled:
            # Make the inner square smaller
            smaller_rect = self._rect.inflate(-6, -6) 
            pygame.draw.rect(
                self._screen,
                self._clicked_color.value,
                smaller_rect,
                border_radius=self._border_radius - 2
            )

            tick_rect = self._tick_image.get_rect(center=self._rect.center)
            self._screen.blit(self._tick_image, tick_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        Checks if the checkbox is clicked.

        Args:
            event (pygame.event.Event): The Pygame event containing mouse
                coordinates.

        Returns:
            bool: True if the checkbox is clicked, False otherwise.
        """
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if self._rect.collidepoint(mouse_pos):
            return True
        return False