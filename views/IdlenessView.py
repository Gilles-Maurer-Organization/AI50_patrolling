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
        label_text: str,
    ) -> None:
        self._screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._label_text = label_text
        self._font = pygame.font.SysFont("Arial", 16)
        self._rect = pygame.Rect(
            self._x,
            self._y,
            self._width,
            self._height
        )

       
    def draw_text(self) -> None:
        """
        Draws the idleness on the Simulation Data View.
        """
        #name associated to the value
        label_text_surface = self._font.render(
            self._label_text,
            True,
            Colors.BLACK.value
        )
        
        label_text_rect = label_text_surface.get_rect(topleft=(self._x, self._y))

        self._screen.blit(label_text_surface, label_text_rect)

        

        