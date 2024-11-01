from constants.Colors import Colors

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

    