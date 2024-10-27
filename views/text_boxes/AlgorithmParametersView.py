from views.text_boxes.BaseTextBoxView import BaseTextBoxView
from constants.Colors import Colors

class AlgorithmParametersView(BaseTextBoxView):
    def __init__(self, screen, x, y, width, height, label_text) -> None:
        super().__init__(screen, x, y, width, height)
        self.label_text = label_text

    def draw_text(self, surface):
        '''
        Cette méthode dessine le texte dans la zone de texte (paramètre).
        
        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le texte.
        '''
        text = self.font.render(self.text_box_content, True, self.text_color)
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        surface.blit(text, text_rect)

        label_surface = self.font.render(self.label_text, True, Colors.BLACK.value)
        label_rect = label_surface.get_rect(topleft=(self.x, self.y - 25))
        self.screen.blit(label_surface, label_rect)