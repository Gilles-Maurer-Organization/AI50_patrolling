from constants.Colors import Colors
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Agent import Agent
from models.Button import Button
from views.ButtonView import ButtonView


class StartButtonController(BaseButtonController):
    def __init__(self, parameters_view, graph_controller, parameters_controller) -> None:
        super().__init__(parameters_view, graph_controller)

        # Référence à ParametersController pour accéder à l'état centralisé
        self.parameters_controller = parameters_controller
        self.start_button = Button("Start simulation", self.start_action, enabled=False)

        # Création de la map des boutons et leurs vues
        self.button_map = {
            self.start_button: ButtonView(
                parameters_view.screen,
                self.start_button.text,
                self.start_button.action,
                160,
                490,
                140,
                40,
                color=Colors.BUTTON_GREEN,
                hover_color=Colors.BUTTON_GREEN_HOVER
            )
        }

        # Initialisation des agents et de la vue de simulation
        self.agents = []

    def start_action(self) -> None:
        self.parameters_controller.simulation_started = True

        # Mock pour les agents
        paths = [
            [0, 1, 2, 3, 4],  # Agent 1 fait le tour du pentagone
            [4, 3, 2, 1, 0],  # Agent 2 fait le tour inverse
            [0, 2, 4],        # Agent 3 suit un chemin en étoile
            [1, 3, 0],        # Agent 4 suit un autre chemin en étoile
            [2, 0, 3, 4, 1]   # Agent 5 suit un chemin en zigzag
        ]
        self.agents = [Agent(path, self.graph_controller.graph) for path in paths]

    def draw_simulation(self):
        if self.parameters_controller.simulation_started:
            self.graph_controller.graph_view.draw_simulation(self.agents)

    def enable_start_button(self) -> None:
        '''
        Active le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(True)

    def disable_start_button(self) -> None:
        '''
        Désactive le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(False)
