import pygame

from views.text_boxes.BaseTextBoxView import BaseTextBoxView
from constants.Colors import Colors

class AlgorithmParametersView(BaseTextBoxView):
    """
    This class is representing a parameter view for algorithms with an
    associated label.

    Inherits from BaseTextBoxView and extends its functionality by
    adding a label to the text box.

    Attributes:
        _label_text (str): The text for the label associated with the
            parameter.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        label_text: str
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self._label_text = label_text

    def draw_text(self, surface: pygame.Surface) -> None:
        """
        Draws the text content within the text box and the label above
        it.

        Args:
            surface (pygame.Surface): The surface on which to draw the
                text and label.
        """
        text = self._font.render(self._text_box_content,
                                 True,
                                 self._text_color)
        text_rect = text.get_rect(
            center=(
                self._width / 2,
                self._height / 2
            )
        )
        surface.blit(text, text_rect)

        label_surface = self._font.render(self._label_text,
                                          True,
                                          Colors.BLACK.value)
        
        label_rect = label_surface.get_rect(topleft=(self._x, self._y - 25))
        self._screen.blit(label_surface, label_rect)