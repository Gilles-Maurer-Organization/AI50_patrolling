import pygame

from views.text_boxes.BaseTextBoxView import BaseTextBoxView
from constants.Colors import Colors

class IdlenessView(BaseTextBoxView):
    
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        label_text: str,
        label_value : str
    ) -> None:
        super().__init__(screen, x, y, width, height)
        self._label_text = label_text
        self._label_value = label_value

       
    def draw_text(self) -> None:
        """
        Draws the text content within the text box and the label above
        it.
        """

        
        #name associated to the value
        label_text_surface = self._font.render(self._label_text,
                                          True,
                                          Colors.BLACK.value)
        
        label_text_rect = label_text_surface.get_rect(topleft=(self._x, self._y))

        self._screen.blit(label_text_surface, label_text_rect)

        #value associated
        label_value_surface = self._font.render(self._label_value,
                                          True,
                                          Colors.BLACK.value)
        
        label_value_rect = label_value_surface.get_rect(topleft=(self._x, self._y - 25))

        self._screen.blit(label_value_surface, label_value_rect)
        

        