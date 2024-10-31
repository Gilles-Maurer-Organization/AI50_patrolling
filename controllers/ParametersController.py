from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH
from controllers.buttons.ButtonController import ButtonController
from controllers.buttons.StartButtonController import StartButtonController
from controllers.text_boxes.TextBoxController import TextBoxController
from controllers.ScrollingListController import ScrollingListController
from controllers.text_boxes.AlgorithmParametersController import AlgorithmParametersController
from views.ParametersView import ParametersView

class ParametersController:
    def __init__(self, screen, graph_controller) -> None:
        
        self.parameters_view = ParametersView(screen.subsurface((GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)))

        self.button_controller = ButtonController(self.parameters_view, graph_controller)
        self.start_button_controller = StartButtonController(self.parameters_view, graph_controller)
        self.text_box_controller = TextBoxController(self.parameters_view)
        self.scrolling_list_controller = ScrollingListController(self.parameters_view)
        self.algorithm_parameters_controller = AlgorithmParametersController(self.parameters_view)

        if not graph_controller.graph_has_an_image():
            self.button_controller.disable_clear_button()
            self.button_controller.disable_save_button()

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: bouttons, menus déroulants.
        '''
        self.parameters_view.draw()
        self.parameters_view.draw_buttons(self.button_controller)
        self.parameters_view.draw_start_button(self.start_button_controller)
        self.parameters_view.draw_text_boxes(self.text_box_controller)
        self.parameters_view.draw_algorithm_parameters(self.algorithm_parameters_controller)

        # We need to draw the scrolling list last in order to have the option elements
        # on the foreground
        self.parameters_view.draw_scrolling_list(self.scrolling_list_controller)

    def handle_events(self, event) -> None:
        self.handle_button(event)
        self.handle_text_box(event)
        self.handle_scrolling_list(event)
        self.handle_algorithm_parameters(event)
        self.check_start_button_state()


    def handle_button(self, event) -> None:
        '''
        Cette méthode gère les interactions de clic de souris sur un bouton.
        
        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        self.button_controller.handle_event(event)
        self.start_button_controller.handle_event(event)

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
        self.algorithm_parameters_controller.handle_event(event)

    def enable_start_button(self) -> bool:
        self.start_button_controller.enable_start_button()

    def disable_start_button(self) -> bool:
        self.start_button_controller.disable_start_button()

    def check_start_button_state(self) -> None:
        if (
            self.scrolling_list_controller.get_selected_algorithm() is not None
            and self.text_box_controller.is_everything_filled()
        ):
            self.enable_start_button()
        else:
            self.disable_start_button()
        
