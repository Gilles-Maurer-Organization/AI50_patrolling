import pygame

from constants.Colors import Colors

class PopupView:
    def __init__(self, screen, message: str) -> None:
        self._screen = screen
        self._message = message
        self._font = pygame.font.SysFont("Arial", 16)
        self._height = 44
        self._popup_y_offset = 10
        self._horizontal_padding = 20
        self._icon_spacing = 10

        self._bg_color = Colors.POPUP_COLOR.value
        self._text_color = (255, 255, 255)
        self._stroke_color = (0, 0, 0)
        self._radius = 6

        self._icon_path = "assets/popup/check-mark.png"
        self._load_icon()
        
        self._popup_start_time = None
        self._popup_duration = 2000
        self._active = False

    def _load_icon(self) -> None:
        self._icon = pygame.image.load(self._icon_path)
        self._icon = pygame.transform.scale(self._icon, (20, 20))

    def _calculate_width(self):
        text_surface = self._font.render(self._message, True, self._text_color)
        text_width = text_surface.get_width()
        icon_width = self._icon.get_width()
        return text_width + self._horizontal_padding * 2 + icon_width + self._icon_spacing

    def show(self) -> None:
        
        if self._active:
            self._width = self._calculate_width()

            popup_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
            popup_surface.fill((0, 0, 0, 0))
            pygame.draw.rect(
                popup_surface,
                self._bg_color,
                (0, 0, self._width, self._height),
                border_radius=self._radius
            )

            if self._icon:
                icon_x = self._horizontal_padding
                icon_y = (self._height - self._icon.get_height()) // 2

                popup_surface.blit(self._icon, (icon_x, icon_y))
            else:
                raise ValueError(f"Logo not found in class {self}")

            text_surface = self._font.render(self._message, True, self._text_color)
            text_x = self._horizontal_padding + (self._icon.get_width() if self._icon else 0) + self._icon_spacing
            text_rect = text_surface.get_rect(midleft=(text_x, self._height // 2))
            popup_surface.blit(text_surface, text_rect)

            popup_surface.blit(text_surface, text_rect)

            screen_rect = self._screen.get_rect()
            popup_rect = popup_surface.get_rect(center=(screen_rect.centerx, self._height // 2 + self._popup_y_offset))

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
