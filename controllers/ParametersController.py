from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH
from controllers.ScrollingListController import ScrollingListController
from controllers.SimulationController import SimulationController
from controllers.buttons.ButtonController import ButtonController
from controllers.buttons.StartButtonController import StartButtonController
from controllers.text_boxes.AlgorithmParametersController import AlgorithmParametersController
from controllers.text_boxes.TextBoxController import TextBoxController
from views.ParametersView import ParametersView


class ParametersController:
    def __init__(self, screen, graph_controller, file_explorer_controller, simulation_controller: SimulationController) -> None:
        # Centralisation de l'état de simulation dans ParametersController
        self.simulation_controller = simulation_controller

        # Création de la vue des paramètres avec un sous-écran
        self.parameters_view = ParametersView(
            screen.subsurface((GRAPH_WINDOW_WIDTH, 0, PARAMETERS_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)))

        # Initialisation des différents contrôleurs avec self passé à StartButtonController
        self.graph_controller = graph_controller
        self.button_controller = ButtonController(self.parameters_view, graph_controller, file_explorer_controller)
        self.start_button_controller = StartButtonController(self.parameters_view, graph_controller, simulation_controller)
        self.text_box_controller = TextBoxController(self.parameters_view)
        self.scrolling_list_controller = ScrollingListController(self.parameters_view)
        self.algorithm_parameters_controller = AlgorithmParametersController(self.parameters_view)

        # Désactiver certains boutons si le graph n'a pas d'image
        if not graph_controller.graph_has_an_image():
            self.button_controller.disable_clear_button()
            self.button_controller.disable_save_button()

    def draw_parameters(self) -> None:
        '''
        Cette méthode dessine les paramètres de la vue de paramètres: boutons, menus déroulants.
        '''
        self.parameters_view.draw()
        self.parameters_view.draw_buttons(self.button_controller)
        self.parameters_view.draw_start_button(self.start_button_controller)
        self.parameters_view.draw_text_boxes(self.text_box_controller)
        self.parameters_view.draw_algorithm_parameters(self.algorithm_parameters_controller)

        # Dessin de la liste déroulante pour être au premier plan
        self.parameters_view.draw_scrolling_list(self.scrolling_list_controller)

    def handle_events(self, event) -> None:
        '''
        Gère les événements pour chaque composant interactif de l'interface.
        '''
        self.handle_button(event)
        self.handle_text_box(event)
        self.handle_scrolling_list(event)
        self.handle_algorithm_parameters(event)
        self.check_start_button_state()

    def handle_button(self, event) -> None:
        '''
        Gère les interactions de clic de souris sur un bouton.

        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        self.button_controller.handle_event(event)
        self.start_button_controller.handle_event(event)

    def handle_text_box(self, event) -> None:
        '''
        Gère les événements sur une text box.

        Args:
            event: L'événement Pygame contenant des informations concernant l'interaction de l'utilisateur.
        '''
        self.text_box_controller.handle_event(event)

    def handle_scrolling_list(self, event) -> None:
        '''
        Gère les événements sur la liste déroulante.

        Args:
            event: L'événement Pygame contenant des informations sur l'interaction de l'utilisateur.
        '''
        is_algorithm_selected = self.scrolling_list_controller.handle_event(event)
        if is_algorithm_selected:
            selected_algorithm = self.scrolling_list_controller.get_selected_algorithm()
            self.algorithm_parameters_controller.handle_selected_algorithm(selected_algorithm)

    def handle_algorithm_parameters(self, event) -> None:
        '''
        Gère les événements pour les paramètres de l'algorithme.

        Args:
            event: L'événement Pygame contenant des informations sur l'interaction de l'utilisateur.
        '''
        self.algorithm_parameters_controller.handle_event(event)

    def enable_start_button(self) -> bool:
        '''
        Active le bouton de démarrage de la simulation.
        '''
        self.start_button_controller.enable_start_button()

    def disable_start_button(self) -> bool:
        '''
        Désactive le bouton de démarrage de la simulation.
        '''
        self.start_button_controller.disable_start_button()

    def check_start_button_state(self) -> None:
        '''
        Vérifie si le bouton de démarrage doit être activé ou non.
        '''
        if (
                self.scrolling_list_controller.get_selected_algorithm() is not None
                and self.text_box_controller.is_everything_filled()
        ):
            self.enable_start_button()
        else:
            self.disable_start_button()

