import pygame

class AlignmentCheckBoxView:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> None:
        self._screen = screen
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self):
        check_box_surface = pygame.Surface(
            (self._width, self._height),
            pygame.SRCALPHA
        )
        check_box_surface.fill((0, 0, 0, 0))