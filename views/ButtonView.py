import pygame


from constants.Config import GRAPH_WINDOW_WIDTH
from constants.Colors import Colors

class ButtonView:
    """
    This class represents a customizable button in a graphical user
    interface.

    This class provides methods for rendering a button on a Pygame
    screen, handling its visual states (normal, hovered, disabled), and
    optionally displaying an icon alongside the text.

    Attributes:
        _screen (pygame.Surface): The Pygame surface where the button
            will be drawn.
        _text (str): The text displayed on the button.
        _text_color (Colors): The color of the text when the button is
            enabled.
        _width (int): The width of the button.
        _height (int): The height of the button.
        _color (Colors): The current background color of the button.
        _hover_color (Colors): The background color of the button when
            hovered.
        _normal_color (Colors): The default background color of the
            button.
        _disabled_color (Colors): The background color of the button
            when disabled.
        _text_disabled_color (Colors): The text color when the button
            is disabled.
        _hovered (bool): Indicates whether the button is currently
            hovered by the mouse.
        _rect (pygame.Rect): The rectangular area representing the
            button's bounds.
        _font (pygame.font.Font): The font used for rendering the
            button's text.
        _icon (pygame.Surface, optional): The icon image displayed on
            the button, if provided.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        icon_path: str = None,
        color: Colors = Colors.BUTTON,
        hover_color: Colors = Colors.BUTTON_HOVER
    ) -> None:
        self._screen = screen
        self._text = text
        self._text_color = Colors.BLACK
        self._width = width
        self._height = height
        self._color = color

        self._hovered = False

        self._hover_color = hover_color
        self._normal_color = color

        # Color when disabled
        self._disabled_color = Colors.BUTTON_DISABLED
        # Text color when disabled
        self._text_disabled_color = Colors.GRAY_TEXT 

        self._rect = pygame.Rect(x, y, width, height)
        self._font = pygame.font.SysFont("Arial", 16)

        if icon_path:
            self._icon = pygame.image.load(icon_path)
            self._icon = pygame.transform.scale(self._icon, (20, 20))
        else:
            self._icon = None


    def draw(self, enabled: bool) -> None:
        """
        Draws the button on the screen, with its current state
        (enabled/disabled and hovered/non-hovered).

        Args:
            enabled (bool): Indicates whether the button is enabled.
        """
        
        self.update_colors(enabled)
        
        button_surface = pygame.Surface(
            (self._width, self._height),
            pygame.SRCALPHA
        )
        button_surface.fill((0, 0, 0, 0))

        pygame.draw.rect(
            button_surface,
            self._color.value,
            (0, 0, self._width, self._height),
            border_radius=6
        )

        # Draws the icon if it exists
        if self._icon:
            icon_x = 10
            icon_y = (self._height - self._icon.get_height()) // 2

            button_surface.blit(self._icon, (icon_x, icon_y))

        text = self._font.render(self._text, True, self._text_color.value)
        text_rect = text.get_rect(
            center=(
                self._width / 2 + (self._icon.get_width() if self._icon else 0) / 2,
                self._height / 2
            )
        )

        button_surface.blit(text, text_rect)

        self._screen.blit(button_surface, (self._rect.x, self._rect.y))
    
    def is_hovered(self, event: pygame.event.Event) -> bool:
        """
        Checks whether the button is currently being hovered by the
        mouse.

        Args:
            event (pygame.event.Event): The current position of the
                mouse cursor.

        Returns:
            bool: True if the mouse cursor is within the button's
                boundaries, False otherwise.
        """
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        return self._rect.collidepoint(mouse_pos)
    
    def update_colors(self, enabled: bool) -> None:
        """
        Updates the button's colors based on its state (enabled/
        disabled, hovered/non-hovered).

        Args:
            enabled (bool): Indicates whether the button is enabled.
        """
        if not enabled:
            self._color = self._disabled_color
            self._text_color = self._text_disabled_color
        elif self._hovered:
            self._color = self._hover_color
            self._text_color = Colors.BLACK
        else:
            self._color = self._normal_color
            self._text_color = Colors.BLACK

    def set_hovered(self) -> None:
        """
        Sets the button to its hovered state, changing its appearance
        to the hover color.
        """
        self._color = self._hover_color
        self._hovered = True

    def set_normal(self) -> None:
        """
        Resets the button to its normal state, changing its appearance
        to the default color.
        """
        self._color = self._normal_color
        self._hovered = False