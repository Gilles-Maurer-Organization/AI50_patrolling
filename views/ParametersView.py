from constants.Colors import Colors
from views.TextBoxView import TextBoxView
from controllers.TextBoxController import TextBoxController

from controllers.ButtonController import ButtonController

class ParametersView:
    def __init__(self, screen, graph_controller) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

        self.text_box = TextBoxView(self.screen, 10, 60, 240, 40, logo_path='assets/number_agents.png')

        self.button_controller = ButtonController(self, graph_controller)
        self.text_box_controller = TextBoxController(self)

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants.
        '''
        self.screen.fill(self.background_color)

        self.button_controller.draw_buttons()

        # Dessin de la zone de texte
        self.text_box.draw()

    def handle_button(self, event) -> None:
        '''
        Cette méthode gère les interactions de clic de souris sur un bouton.
        
        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        self.button_controller.handle_mouse(event)

    
    def handle_text_box_event(self, event) -> None:
        '''
        Cette méthode gère les événements réalisés sur une text box.
        
        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur avec le programme.
        '''
        self.text_box_controller.handle_event(event)

    def get_text_box_view(self) -> TextBoxView:
        return self.text_box