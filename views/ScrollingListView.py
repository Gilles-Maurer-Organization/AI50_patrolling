from typing import Union
import pygame

from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH
from models.algorithms.IAlgorithmModel import IAlgorithmModel

class ScrollingListView:
    """
    This class represents a scrolling list view used for displaying selectable
    algorithm options.
    
    It handles the rendering of the dropdown header, list options, and the
    interaction state (active, hovered, clicked).
    
    Attributes:
        _screen (pygame.Surface): The screen where the view elements are
            drawn.
        _x (int): The x-coordinate of the top-left corner of the scrolling
            list.
        _y (int): The y-coordinate of the top-left corner of the scrolling
            list.
        _width (int): The width of the scrolling list.
        _height (int): The height of the scrolling list.
        _color (pygame.Color): The color of the scrolling list header.
        _text_color (pygame.Color): The color of the text in the header.
        _font (pygame.font.Font): The font used to render the text in the
            list.
        _scrolling_list_rect (pygame.Rect): The rectangle representing the
            area of the scrolling list.
        _icon_path (str): Path to the icon image used for the dropdown
            indicator.
        _icon (pygame.Surface): The image of the dropdown indicator icon.
        _flipped_icon (pygame.Surface): The flipped version of the icon
            (for the dropdown).
        _is_active (bool): Indicates whether the list is active (open) or not.
        _options_rects (list[pygame.Rect]): A list of rectangles for the
            options in the dropdown.

    Methods:
        draw(algorithms, selected_algorithm=None, has_an_algorithm_selected=False):
            Renders the scrolling list with its header and options if active.
        
        _draw_list_header(selected_algorithm=None):
            Renders the header of the scrolling list, showing the selected
            algorithm name or a placeholder.
        
        _draw_options(algorithms: list[IAlgorithmModel]):
            Renders the available options under the list header.
        
        _change_header_text_color():
            Changes the header text color when an algorithm is selected.
        
        is_option_clicked(event, algorithms: list[str]):
            Checks if an option in the list has been clicked and returns the
            selected option.
        
        set_active(is_active: bool):
            Sets the active (open) state of the dropdown list.
        
        set_selected_option(option: str):
            Sets the selected option in the dropdown list.
        
        set_hovered():
            Changes the state of the dropdown list to hovered.
        
        set_clicked():
            Changes the state of the dropdown list to clicked.
        
        set_normal():
            Changes the state of the dropdown list to normal
            (neither hovered nor clicked).
        
        is_hovered(event: pygame.event.Event):
            Checks if the dropdown list is hovered by the mouse.
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

        self._font = pygame.font.SysFont("Arial", 16)
        self._scrolling_list_rect = pygame.Rect(self._x,
                                                self._y,
                                                self._width,
                                                self._height)

        self._icon_path = 'assets/scrolling_icon.png'

        self._icon = pygame.image.load(self._icon_path)
        self._icon = pygame.transform.scale(self._icon, (20, 20))
        self._flipped_icon = pygame.transform.flip(self._icon, False, True)

        self._is_active = False
        self._options_rects = []

    @property
    def is_active(self) -> bool:
        return self._is_active

    def draw(self,
             algorithms: list[IAlgorithmModel],
             selected_algorithm: IAlgorithmModel = None,
             has_an_algorithm_selected: bool = False
             ) -> None:
        """
        Renders the dropdown list with its header and options if active.

        Args:
            algorithms (list[IAlgorithmModel]): A list of available algorithms.
            selected_algorithm (IAlgorithmModel, optional): The selected
                algorithm. Defaults to None.
            has_an_algorithm_selected (bool, optional): Whether an algorithm
                is selected. Defaults to False.
        """
        if has_an_algorithm_selected:
            self._change_header_text_color()
        self._draw_list_header(selected_algorithm)

        if self._is_active:
            self._draw_options(algorithms)
    
    def _draw_list_header(self, selected_algorithm = None):
        """
        Renders the header of the scrolling list.

        Args:
            selected_algorithm (IAlgorithmModel, optional): The selected
                algorithm. Defaults to None.
        """
        pygame.draw.rect(self._screen,
                         self._color,
                         self._scrolling_list_rect,
                         border_radius=6)
        
        text = self._font.render(
            selected_algorithm.name if selected_algorithm else 'Select algorithm',
            True,
            self._text_color
        )

        # If the dropdown list is expanded, flip the icon horizontally to
        # reverse the arrow direction
        icon_to_draw = self._flipped_icon if self._is_active else self._icon

        icon_x = self._width - icon_to_draw.get_width() - 10
        icon_y = (self._height - icon_to_draw.get_height()) // 2
        self._screen.blit(icon_to_draw, (self._x + icon_x, self._y + icon_y))

        text_rect = text.get_rect(
            center=(
                self._x + self._width / 2 - icon_to_draw.get_width() / 2,
                self._y + self._height / 2
            )
        )
        self._screen.blit(text, text_rect)

    def _draw_options(self, algorithms: list[IAlgorithmModel]) -> None:
        """
        Renders the available options under the list header.

        Args:
            algorithms (list[IAlgorithmModel]): A list of available
                algorithms.
        """
        option_height = 40
        self._options_rects = []

        for i, option in enumerate(algorithms):
            option_name = option.name
            option_rect = pygame.Rect(self._x,
                                      self._y + (i + 1) * option_height,
                                      self._width,
                                      option_height)
            
            self._options_rects.append(option_rect)

            pygame.draw.rect(self._screen,
                             Colors.LIGHT_GRAY.value,
                             option_rect)
            
            text = self._font.render(option_name, True, Colors.BLACK.value)
            text_rect = text.get_rect(
                center=(
                    option_rect.x + option_rect.width / 2,
                    option_rect.y + option_rect.height / 2
                )
            )
            self._screen.blit(text, text_rect)

    def _change_header_text_color(self) -> None:
        """
        Changes the header text color when an algorithm is selected.
        """
        self._text_color = Colors.BLACK.value

    def is_option_clicked(self, event, algorithms: list[str]) -> Union[None, str]:
        """
        Checks if an option in the list has been clicked and returns the
        selected option.

        Args:
            event: The Pygame event containing mouse coordinates.
            algorithms (list[str]): The list of available algorithms in the
                model.

        Returns:
            Union[None, str]: The name of the selected algorithm, or None if
                no option is clicked.
        """

        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        for rect, option in zip(self._options_rects, algorithms):
            if rect.collidepoint(mouse_pos):
                return option
        return None

    def set_active(self, is_active: bool) -> None:
        """
        Sets the active (open) state of the dropdown list.

        Args:
            is_active (bool): The active state of the dropdown list
                (open or closed).
        """
        self._is_active = is_active
        self._color = Colors.TEXT_BOX_CLICKED.value if is_active else Colors.BUTTON.value

    def set_selected_option(self, option: str) -> None:
        """
        Sets the selected option in the scrolling list.

        Args:
            option (str): The selected option.
        """
        self._selected_option = option
        self._is_active = False

    def set_hovered(self) -> None:
        """
        Changes the state of the scrolling list to hovered.
        """
        self._color = Colors.BUTTON_HOVER.value

    def set_clicked(self) -> None:
        """
        Changes the state of the scrolling list to clicked.
        """
        self._color = Colors.TEXT_BOX_CLICKED.value
        self._stroke_color = Colors.BLACK.value

    def set_normal(self) -> None:
        """
        Changes the state of the dropdown list to normal
            (neither hovered nor clicked).
        """
        self._color = Colors.BUTTON.value
        self._stroke_color = Colors.GRAY_TEXT.value

    def is_hovered(self, event: pygame.event.Event) -> bool:
        """
        Checks if the dropdown list is hovered by the mouse.

        Args:
            event: The Pygame event containing mouse coordinates.

        Returns:
            bool: True if the dropdown list is hovered, False otherwise.
        """
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if self._scrolling_list_rect:
            return self._scrolling_list_rect.collidepoint(mouse_pos)
        return False