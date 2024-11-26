import pygame

from constants.Colors import Colors

class PopupView:
    def __init__(self, screen, message: str) -> None:
        self._screen = screen
        self._message = message
        self._font = pygame.font.SysFont("Arial", 16)
        self._width, self._height = 300, 40
        self._bg_color = Colors.POPUP_COLOR.value
        self._text_color = (255, 255, 255)
        self._stroke_color = (0, 0, 0)
        self._radius = 6
        self._popup_start_time = None
        self._popup_duration = 2000
        self._active = False

    def show(self) -> None:
        if self._active:
            popup_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
            
            popup_surface.fill((0, 0, 0, 0))
            pygame.draw.rect(
                popup_surface,
                self._bg_color,
                (0, 0, self._width, self._height),
                border_radius=self._radius
            )

            text_surface = self._font.render(self._message, True, self._text_color)
            text_rect = text_surface.get_rect(center=(self._width // 2, self._height // 2))
            
            popup_surface.blit(text_surface, text_rect)

            screen_rect = self._screen.get_rect()
            popup_rect = popup_surface.get_rect(center=(screen_rect.centerx, self._height // 2 + 10))

            self._screen.blit(popup_surface, popup_rect)
            pygame.display.flip()

    def start_popup(self):
        self._popup_start_time = pygame.time.get_ticks()
        self._active = True

    def check_popup_expiration(self):
        if self._active:
            elapsed_time = pygame.time.get_ticks() - self._popup_start_time
            if elapsed_time >= self._popup_duration:
                self._active = False
