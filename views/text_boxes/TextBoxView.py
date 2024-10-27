import pygame

from views.text_boxes.BaseTextBoxView import BaseTextBoxView

class TextBoxView(BaseTextBoxView):
    def __init__(self, screen, x, y, width, height, icon_path=None) -> None:
        super().__init__(screen, x, y, width, height)
        
        if icon_path:
            self.icon = pygame.image.load(icon_path)
            self.icon = pygame.transform.scale(self.icon, (20, 20))
        else:
            self.icon = None

    def draw_text(self, surface):
        '''
        Cette méthode dessine le texte dans la zone de texte, avec une icône si elle est présente.
        
        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le texte.
        '''
        if self.icon:
            icon_x = 10
            icon_y = (self.height - self.icon.get_height()) // 2
            surface.blit(self.icon, (icon_x, icon_y))

        text = self.font.render(self.text_box_content, True, self.text_color)
        text_rect = text.get_rect(center=(self.width / 2 + (self.icon.get_width() if self.icon else 0) / 2, self.height / 2))
        surface.blit(text, text_rect)