from controllers.buttons.ButtonController import ButtonController
from controllers.text_boxes.TextBoxController import TextBoxController
from controllers.ScrollingListController import ScrollingListController
from controllers.text_boxes.AlgorithmParametersController import AlgorithmParametersController

class ParametersController:
    def __init__(self, view, graph_controller) -> None:
        self.view = view
        self.graph_controller = graph_controller

        # Initialise les contrôleurs pour gérer les interactions
        self.button_controller = ButtonController(self.view.button_views, graph_controller)
        self.start_button_controller = StartButtonController(self.view.start_button_view, graph_controller)
        self.text_box_controller = TextBoxController(self.view.text_box_views)
        self.scrolling_list_controller = ScrollingListController(self.view.scrolling_list_view)
        self.algorithm_parameters_controller = AlgorithmParametersController(self.view)

    def handle_events(self, event) -> None:
        '''
        Cette méthode gère les événements utilisateur et les distribue aux contrôleurs appropriés.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button_controller.handle_event(event)
            self.start_button_controller.handle_event(event)
        elif event.type == pygame.KEYDOWN:
            self.text_box_controller.handle_event(event)
        
        # Gestion des événements de la liste déroulante
        self.scrolling_list_controller.handle_event(event)