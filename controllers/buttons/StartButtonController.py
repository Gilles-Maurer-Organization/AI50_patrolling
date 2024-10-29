from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from models.Agent import AgentModel
from views.ButtonView import ButtonView
from constants.Colors import Colors
import pygame
import numpy as np

class StartButtonController(BaseButtonController):
    def __init__(self, parameters_view, graph_controller) -> None:
        super().__init__(parameters_view, graph_controller)

        self.start_button = Button("Start simulation", self.start_action, enabled=True)

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
        self.simulation_started = False

    def start_action(self) -> None:
        '''
        Cette méthode lance le programme selon l'algorithme sélectionné.
        '''
        print("Starting algorithm")
        # Mock up pour les agents
        paths = [
            [0, 1, 2, 3, 4],  # Agent 1 fait le tour du pentagone
            [4, 3, 2, 1, 0],  # Agent 2 fait le tour inverse
            [0, 2, 4],  # Agent 3 suit un chemin en étoile
            [1, 3, 0],  # Agent 4 suit un autre chemin en étoile
            [2, 0, 3, 4, 1]  # Agent 5 suit un chemin en zigzag
        ]
        self.agents = [AgentModel(path, self.graph_controller.graph) for path in paths]
        self.simulation_started = True

    def update_simulation(self):
        '''
        Met à jour la position de chaque agent dans la simulation.
        '''
        if self.simulation_started:
            for agent in self.agents:
                agent.move()

            # Vérifie si tous les agents ont fini leur parcours
            if all(agent.finished for agent in self.agents):
                # Si tous les agents ont fini, on les réinitialise pour un nouveau parcours
                for agent in self.agents:
                    agent.reset_path()

    def draw_simulation(self):

        self.graph_controller.draw_graph()

        for agent in self.agents:
            pygame.draw.circle(self.parameters_view.screen, Colors.AGENT_COLOR.value, (int(agent.x), int(agent.y)), 5)

        pygame.display.flip()

    def enable_start_button(self) -> None:
        '''
        Cette méthode active le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(True)

    def disable_start_button(self) -> None:
        '''
        Cette méthode désactive le bouton de démarrage de la simulation.
        '''
        self.start_button.set_enabled(False)
