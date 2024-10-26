from constants.Colors import Colors

from models.TextBox import TextBox

from views.TextBoxView import TextBoxView

from controllers.TextBoxController import TextBoxController
from controllers.ButtonController import ButtonController
from controllers.ScrollingListController import ScrollingListController
from controllers.AlgorithmParametersController import AlgorithmParametersController


class ParametersView:
    def __init__(self, screen, graph_controller) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

        self.button_controller = ButtonController(self, graph_controller)
        self.text_box_controller = TextBoxController(self)
        self.scrolling_list_controller = ScrollingListController(self)
        self.algorithm_parameters_controller = AlgorithmParametersController(self)

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants.
        '''
        self.screen.fill(self.background_color)

        # Dessin de l'intégralité des boutons
        self.button_controller.draw_buttons()

        # Dessin de la zone de texte
        self.text_box_controller.draw_text_box()

        # Dessin de la liste déroulante

        self.algorithm_parameters_controller.draw_parameters()
        self.scrolling_list_controller.draw_scrolling_list()

    def handle_events(self, event) -> None:
        self.handle_button(event)
        self.handle_text_box(event)
        self.handle_scrolling_list(event)
        self.handle_algorithm_parameters(event)

    def handle_button(self, event) -> None:
        '''
        Cette méthode gère les interactions de clic de souris sur un bouton.
        
        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        self.button_controller.handle_event(event)

    def handle_text_box(self, event) -> None:
        '''
        Cette méthode gère les événements réalisés sur une text box.
        
        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur avec le programme.
        '''
        self.text_box_controller.handle_event(event)


    def handle_scrolling_list(self, event) -> None:
        '''
        Cette méthode gère les événements réalisés sur une text box.
        
        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur avec le programme.
        '''
        is_algorithm_selected = self.scrolling_list_controller.handle_event(event)
        if is_algorithm_selected:
            algorith_selected = self.scrolling_list_controller.get_selected_algorithm()
            self.algorithm_parameters_controller.handle_selected_algorithm(algorith_selected)

    def handle_algorithm_parameters(self, event) -> None:
        self.algorithm_parameters_controller.handle_algorithm_parameters(event)
