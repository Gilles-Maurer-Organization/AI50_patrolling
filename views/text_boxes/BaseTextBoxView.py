import pygame
from abc import ABC, abstractmethod
from constants.Colors import Colors

class BaseTextBoxView(ABC):
    """
    A base class for text box views, providing common functionalities and properties
    for drawing and interacting with text boxes in the user interface.
    
    Attributes:
        _screen (pygame.Surface): The surface where the text box is drawn.
        _x (int): The x-coordinate of the text box.
        _y (int): The y-coordinate of the text box.
        _width (int): The width of the text box.
        _height (int): The height of the text box.
        _color (tuple): The current background color of the text box.
        _text_color (tuple): The color of the text inside the text box.
        _stroke_color (tuple): The color of the text box's border.
        _font (pygame.Font): The font used for rendering text in the text box.
        _text_box_rect (pygame.Rect): The rectangle defining the text box's position and size.
        _text_box_content (str): The current content of the text box.
    
    Methods:
        draw():
            Draws the text box and its content onto the screen.
        
        draw_text(surface):
            Abstract method to draw the text content in the text box.
        
        change_text(new_text):
            Updates the content of the text box.
        
        set_hovered():
            Sets the text box's appearance to a hovered state.
        
        set_clicked():
            Sets the text box's appearance to a clicked state.
        
        set_normal():
            Resets the text box's appearance to its normal state.
        
        set_text_completed(is_completed):
            Updates the text color based on whether the content is considered complete.

        is_hovered():
            Returns whether the mouse is inside the text box or not.
    """
    def __init__(self,
                 screen: pygame.Surface,
                 x: int,
                 y: int,
                 width: int,
                 height: int
                 ) -> None:
        self._screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._color = Colors.BUTTON.value
        self._text_color = Colors.TEXT_BOX_TEXT.value
        self._stroke_color = Colors.GRAY_TEXT.value

        self._font = pygame.font.SysFont("Arial", 16)
        self._text_box_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._text_box_content = None

    def draw(self) -> None:
        """
        Draws the text box on the screen at the specified position with the current
        background and border colors.
        """
        text_box_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)

        # Create and draw the border surface.
        border_surface = pygame.Surface((self._width + 2, self._height + 2), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(border_surface, self._stroke_color, (0, 0, self._width + 2, self._height + 2), border_radius=6)
        self._screen.blit(border_surface, (self._x - 1, self._y - 1))

        # Draw the text box surface.
        pygame.draw.rect(text_box_surface, self._color, (0, 0, self._width, self._height), border_radius=6)

        # Draw the text inside the text box.
        self.draw_text(text_box_surface)

        # Blit the text box onto the screen.
        self._screen.blit(text_box_surface, (self._x, self._y))

    @abstractmethod
    def draw_text(self, surface: pygame.Surface) -> None:
        """
        Abstract method to draw the text content inside the text box. 
        Must be implemented in derived classes.

        Args:
            surface (pygame.Surface): The surface where the text will be drawn.
        """
        pass

    def change_text(self, new_text: str) -> None:
        """
        Updates the text content of the text box based on data received 
        from the controller.

        Args:
            new_text (str): The new text to be displayed in the text box.
        """
        self._text_box_content = new_text

    def set_hovered(self) -> None:
        """
        Changes the text box's appearance to indicate a hovered state.
        """
        self._color = Colors.BUTTON_HOVER.value

    def set_clicked(self) -> None:
        """
        Changes the text box's appearance to indicate a clicked state.
        """
        self._color = Colors.TEXT_BOX_CLICKED.value
        self._stroke_color = Colors.BLACK.value

    def set_normal(self) -> None:
        """
        Resets the text box's appearance to its normal, unhovered, and unclicked state.
        """
        self._color = Colors.BUTTON.value
        self._stroke_color = Colors.GRAY_TEXT.value

    def set_text_completed(self, is_completed: bool) -> None:
        """
        Changes the text color based on whether the text box content is considered complete.

        Args:
            is_completed (bool): True if the text box content is complete, otherwise False.
        """
        self._text_color = Colors.BLACK.value if is_completed else Colors.TEXT_BOX_TEXT.value

    def is_hovered(self, mouse_pos: tuple[int]) -> bool:
        """
        Checks if the mouse position is within the bounds of the text box.

        Args:
            mouse_pos (tuple[int]): The (x, y) coordinates of the mouse.

        Returns:
            bool: True if the mouse is inside the text box, False otherwise.
        """
        if self._text_box_rect:
            return self._text_box_rect.collidepoint(mouse_pos)
        return False
