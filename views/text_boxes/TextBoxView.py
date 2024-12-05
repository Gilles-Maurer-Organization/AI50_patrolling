import pygame

from views.text_boxes.BaseTextBoxView import BaseTextBoxView

class TextBoxView(BaseTextBoxView):
    """
    This class is a specialized view for a text box that supports
    displaying an optional icon alongside the text.

    Attributes:
        _icon (pygame.Surface or None): The icon image displayed in the
            text box, or None if no icon is specified.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        icon_path: str = None
    ) -> None:
        super().__init__(screen, x, y, width, height)
        
        if icon_path:
            self._icon = pygame.image.load(icon_path)
            self._icon = pygame.transform.scale(self._icon, (20, 20))
        else:
            self._icon = None

    def draw_text(self, surface: pygame.Surface) -> None:
        """
        Draws the text inside the text box, including an optional icon if
        provided.

        Args:
            surface (pygame.Surface): The surface where the text and icon 
                will be drawn.
        """
        if self._icon:
            # Calculate the position of the icon (aligned vertically to the center).
            icon_x = 10 # Padding from the left edge of the text box.
            icon_y = (self._height - self._icon.get_height()) // 2
            surface.blit(self._icon, (icon_x, icon_y))

        # Render the text content with the specified font and color.
        text = self._font.render(self._text_box_content, True, self._text_color)
        
        # Adjust the text position based on the presence of the icon.
        text_rect = text.get_rect(
            center=(
                self._width / 2 + (self._icon.get_width() if self._icon else 0) / 2,
                self._height / 2
            )
        )

        # Draw the text onto the provided surface.
        surface.blit(text, text_rect)