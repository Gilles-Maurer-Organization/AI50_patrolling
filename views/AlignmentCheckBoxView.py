import pygame
from constants.Colors import Colors
from constants.Config import GRAPH_WINDOW_WIDTH
from utils.utils import resource_path

class AlignmentCheckBoxView:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        self._screen = screen
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)

        self._color = Colors.FOG_GRAY
        self._clicked_color = Colors.GREEN
        self._border_radius = 6

        self._tick_image = pygame.image.load(resource_path("assets/checkbox/tick.png"))
        self._tick_image = pygame.transform.scale(
            self._tick_image,
            (int(self._width * 0.5), int(self._height * 0.5))
        )


    def draw(self, alignment_enabled: bool) -> None:
        # Draw the main checkbox (a square with border-radius)
        pygame.draw.rect(
            self._screen,
            self._color.value,
            self._rect,
            border_radius=self._border_radius
        )

        # If clicked, draw a slightly smaller square inside the checkbox
        if alignment_enabled:
            # Make the inner square smaller
            smaller_rect = self._rect.inflate(-6, -6) 
            pygame.draw.rect(
                self._screen,
                self._clicked_color.value,
                smaller_rect,
                border_radius=self._border_radius 
            )

            tick_rect = self._tick_image.get_rect(center=self._rect.center)
            self._screen.blit(self._tick_image, tick_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        Checks if the checkbox is clicked.

        Args:
            event: The Pygame event containing mouse coordinates.

        Returns:
            bool: True if the checkbox is clicked, False otherwise.
        """
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if self._rect.collidepoint(mouse_pos):
            return True
        return False