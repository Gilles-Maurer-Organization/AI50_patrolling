from constants.Colors import Colors
from controllers.SimulationController import SimulationController
from controllers.buttons.BaseButtonController import BaseButtonController
from controllers.GraphController import GraphController
from models.Agent import Agent
from models.Button import Button
from services.AStarService import AStarService
from services.ICompleteGraphService import ICompleteGraphService
from views.ButtonView import ButtonView
from services.ICSVService import ICSVService

class StartButtonController(BaseButtonController):
    def __init__(self, parameters_view, graph_controller, simulation_controller: SimulationController) -> None:
        super().__init__(parameters_view, graph_controller)

        self._simulation_controller = simulation_controller

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
        # Mock pour les agents
        paths = [
            [0, 1, 2, 3, 4],  # Agent 1 fait le tour du pentagone
            [4, 3, 2, 1, 0],  # Agent 2 fait le tour inverse
            [0, 2, 4],        # Agent 3 suit un chemin en étoile
            [1, 3, 0],        # Agent 4 suit un autre chemin en étoile
            [2, 0, 3, 4, 1]   # Agent 5 suit un chemin en zigzag
        ]
        # self.agents = [Agent(path, self.graph_controller.graph) for path in paths]
        
        self._simulation_controller.initialize_agents(paths)

        self._simulation_controller.set_simulation_started(True)
        
        #complete_graph_data = self.csv_service.find_csv_reference("path/to/image")
        #if complete_graph_data:
        #    pass

        if self.graph_controller.is_graph_modified():
            self.graph_controller.save_graph()
            complete_graph, shortest_paths = self.compute_complete_graph_and_shortest_paths()

            self.graph_controller.save_complements(complete_graph, shortest_paths)
        
        elif not self.graph_controller.are_complements_saved():
            complete_graph, shortest_paths = self.compute_complete_graph_and_shortest_paths()
            
            self.graph_controller.save_complements(complete_graph, shortest_paths)

        elif self.graph_controller.are_complements_saved():
            selected_algorithm = self.parameters_controller.scrolling_list_controller.get_selected_algorithm()
            print(self.graph_controller.graph.shortest_paths)
            # TODO: interface for all the algorithm that owns a launch() method, that all the algorithm implement
            # paths = selected_algorithm.launch()
            # passer paths à la simulation
            print("Launching algorithm with complete graph", selected_algorithm)

            
    def compute_complete_graph_and_shortest_paths(self):

        simple_graph, node_positions = self.graph_controller.graph.compute_matrix()
        complete_graph = self.complete_graph_service(
            simple_graph=simple_graph,
            node_position=node_positions,
            path_finding_service=AStarService
        ).get_complete_graph()

        # TODO: Check if the gomplete graph is None, and if it is the case,
        # create a pop-up to the user interface
        shortest_paths = {}
        for start in range(len(simple_graph)):
            for end in range(len(simple_graph)):
                if start != end:
                    a_star = AStarService(simple_graph, node_positions, start, end)
                    shortest_paths[(start, end)] = a_star.find_path()
        print(shortest_paths)            

        return complete_graph, shortest_paths

    def draw_simulation(self):
        pass
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
