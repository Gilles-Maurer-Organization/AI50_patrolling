from constants.Colors import Colors
from controllers.GraphController import GraphController
from controllers.ScrollingListController import ScrollingListController
from controllers.SimulationController import SimulationController
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from services.AStarService import AStarService
from services.ICompleteGraphService import ICompleteGraphService
from services.ICSVService import ICSVService
from views.ButtonView import ButtonView
from views.ParametersView import ParametersView

class StartButtonController(BaseButtonController):
    """
    This class manages the "Start simulation" button in the ParametersView and handles simulation-related actions.

    Methods:
        start_action() -> None:
            Starts the simulation by initializing agents and launching the selected algorithm.
        
        _compute_store_and_save_graph_data() -> None:
            Computes, stores, and saves the complete graph and shortest paths.
        
        _launch_algorithm() -> None:
            Launches the selected algorithm and starts the simulation.
        
        compute_complete_graph_and_shortest_paths() -> Tuple[Dict, Dict]:
            Computes the complete graph and shortest paths using A* algorithm.
        
        enable_start_button() -> None:
            Enables the "Start simulation" button, allowing the user to start the simulation.
        
        disable_start_button() -> None:
            Disables the "Start simulation" button, preventing the user from starting the simulation.
        
    Attributes:
        _complete_graph_service (ICompleteGraphService): Service for computing the complete graph.
        _csv_service (ICSVService): Service for handling CSV operations.
        _scrolling_list_controller (ScrollingListController): Controller for managing the scrolling list view of algorithms.
        _simulation_controller (SimulationController): Controller for handling simulation logic.
        _start_button (Button): The "Start simulation" button.
        _button_map (dict[Button, ButtonView]): A map of Button objects to their corresponding ButtonView objects.
        agents (List[Agent]): List of agents involved in the simulation.
    """
    def __init__(self,
                 parameters_view: ParametersView,
                 graph_controller: GraphController,
                 simulation_controller: SimulationController,
                 scrolling_list_controller: ScrollingListController,
                 complete_graph_service: ICompleteGraphService,
                 csv_service: ICSVService) -> None:
        super().__init__(parameters_view, graph_controller)

        self._complete_graph_service = complete_graph_service
        self._csv_service = csv_service
        self._scrolling_list_controller = scrolling_list_controller
        self._simulation_controller = simulation_controller
        self._scrolling_list_controller = scrolling_list_controller

        self._start_button = Button("Start simulation", self.start_action, enabled=False)

        # Création de la map des boutons et leurs vues
        self._button_map = {
            self._start_button: ButtonView(
                parameters_view.screen,
                self._start_button.text,
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
        """
        Starts the simulation by initializing agents and launching the selected algorithm.
        """
        paths = [
            [0, 1, 2, 3, 4],  # Agent 1 fait le tour du pentagone
            [4, 3, 2, 1, 0],  # Agent 2 fait le tour inverse
            [0, 2, 4],        # Agent 3 suit un chemin en étoile
            [1, 3, 0],        # Agent 4 suit un autre chemin en étoile
            [2, 0, 3, 4, 1]   # Agent 5 suit un chemin en zigzag
        ]

        # Initializing agents with predefined paths
        self._simulation_controller.initialize_agents(paths)

        # Setting the simulation as started
        self._simulation_controller.set_simulation_started(True)
        
        #complete_graph_data = self.csv_service.find_csv_reference("path/to/image")
        #if complete_graph_data:
        #    pass

        if self.graph_controller.is_graph_modified():
            self.graph_controller.save_graph()
            success = self._compute_store_and_save_graph_data()
            if success:
                self._launch_algorithm()
            else:
                self.graph_controller.raise_error_message('The graph must not have isolated subgraphs')
        
        elif not self.graph_controller.are_complements_saved():
            success = self._compute_store_and_save_graph_data()
            if success:
                self._launch_algorithm()
            else:
                self.graph_controller.raise_error_message('The graph must not have isolated subgraphs')

        elif self.graph_controller.are_complements_saved():
            self._launch_algorithm()

    def _compute_store_and_save_graph_data(self):
        """
        Computes, stores, and saves the complete graph and shortest paths.
        """
        complete_graph, shortest_paths = self.compute_complete_graph_and_shortest_paths()
        if not complete_graph:
            return False
        if not shortest_paths:
            raise ValueError('Shortest paths dictionnary is null while Complete Graph array exists.')
    
        self._graph_controller.store_complements_to_model(complete_graph, shortest_paths)

        self._graph_controller.save_complements(complete_graph, shortest_paths)
        return True

    def _launch_algorithm(self):
        """
        Launches the selected algorithm and starts the simulation.
        """
        self._graph_controller.raise_info('Algorithm launched')
        selected_algorithm = self._scrolling_list_controller.get_selected_algorithm()
        
        # TODO: interface for all the algorithm that owns a launch() method, that all the algorithm implement
        # paths = selected_algorithm.launch()
        # passer paths à la simulation
        print("Launching algorithm with complete graph", selected_algorithm)
    
        #self.graph_controller.raise_message('Simulation started')
            
    def compute_complete_graph_and_shortest_paths(self):
        """
        Computes the complete graph and shortest paths using the A* algorithm.

        Returns:
            complete_graph (Array): The complete graph with all paths.
            shortest_paths (dict): The shortest paths between all nodes.
        """
        simple_graph, node_positions = self._graph_controller._graph.compute_matrix()
        complete_graph = self._complete_graph_service(
            simple_graph=simple_graph,
            node_position=node_positions,
            path_finding_service=AStarService
        ).get_complete_graph()

        shortest_paths = {}
        for start in range(len(simple_graph)):
            for end in range(len(simple_graph)):
                if start != end:
                    a_star = AStarService(simple_graph, node_positions, start, end)
                    shortest_paths[(start, end)] = a_star.find_path()[0] # We don't want to store the cost 

        return complete_graph, shortest_paths

    def enable_start_button(self) -> None:
        """
        Enables the "Start simulation" button, allowing the user to start the simulation.
        """
        self._start_button.enabled = True

    def disable_start_button(self) -> None:
        """
        Disables the "Start simulation" button, preventing the user from starting the simulation.
        """
        self._start_button.enabled = False
