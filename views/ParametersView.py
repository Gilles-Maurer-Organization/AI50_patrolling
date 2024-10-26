from constants.Colors import Colors

from models.TextBox import TextBox

from views.TextBoxView import TextBoxView

from controllers.TextBoxController import TextBoxController
from controllers.ButtonController import ButtonController
from controllers.StartButtonController import StartButtonController
from controllers.ScrollingListController import ScrollingListController
from controllers.AlgorithmParametersController import AlgorithmParametersController

class ParametersView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = Colors.WHITE.value

    def draw(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants.
        '''
        self.screen.fill(self.background_color)

    def draw_buttons(self, button_controller) -> None:
        button_controller.draw_buttons()

    def draw_start_button(self, start_button_controller) -> None:
        start_button_controller.draw_buttons()

    def draw_text_boxes(self, text_box_controller) -> None:
        text_box_controller.draw_text_boxes()

    def draw_scrolling_list(self, scrolling_list_controller) -> None:
        scrolling_list_controller.draw_scrolling_list()

    def draw_algorithm_parameters(self, algorithm_parameters_controller) -> None:
        algorithm_parameters_controller.draw_text_boxes()

    def handle_scrolling_list(self, event) -> None:
        '''
        Cette méthode gère les événements réalisés sur une text box.
        
        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur avec le programme.
        '''
        is_algorithm_selected = self.scrolling_list_controller.handle_event(event)
        if is_algorithm_selected:
            algorith_selected = self.scrolling_list_controller.get_selected_algorithm()
            self.enable_start_button()
            self.algorithm_parameters_controller.handle_selected_algorithm(algorith_selected)

    def handle_algorithm_parameters(self, event) -> None:
        self.algorithm_parameters_controller.handle_event(event)

    def enable_start_button(self) -> bool:
        self.start_button_controller.enable_start_button()
