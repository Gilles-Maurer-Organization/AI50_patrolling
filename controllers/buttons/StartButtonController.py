from constants.Colors import Colors
from constants.Config import PARAMETERS_WINDOW_WIDTH, PARAMETERS_WINDOW_HEIGHT
from controllers.GraphController import GraphController
from controllers.ScrollingListController import ScrollingListController
from controllers.SimulationController import SimulationController
from controllers.buttons.BaseButtonController import BaseButtonController
from controllers.text_boxes.TextBoxController import TextBoxController
from models.Button import Button
from models.GraphData import GraphData
from services.AStarService import AStarService
from services.ICompleteGraphService import ICompleteGraphService
from services.ICSVService import ICSVService
from views.ButtonView import ButtonView
from views.ParametersView import ParametersView

class StartButtonController(BaseButtonController):
    """
    This class manages the "Start simulation" button in the
    ParametersView and handles simulation-related actions.

    Attributes:
        _complete_graph_service (ICompleteGraphService): Service for
            computing the complete graph.
        _csv_service (ICSVService): Service for handling CSV
            operations.
        _scrolling_list_controller (ScrollingListController):
            Controller for managing the scrolling list view of algorithms.
        _simulation_controller (SimulationController):
            Controller for handling simulation logic.
        _start_button (Button): The "Start simulation" button.
        _button_map (dict[Button, ButtonView]): A map of Button objects
            to their corresponding ButtonView objects.
        agents (List[Agent]): List of agents involved in the simulation.
    """
    def __init__(
        self,
        parameters_view: ParametersView,
        graph_controller: GraphController,
        simulation_controller: SimulationController,
        scrolling_list_controller: ScrollingListController,
        text_box_controller: TextBoxController,
        complete_graph_service: ICompleteGraphService,
        csv_service: ICSVService
    ) -> None:
        super().__init__(parameters_view, graph_controller)

        self._complete_graph_service = complete_graph_service
        self._csv_service = csv_service
        self._scrolling_list_controller = scrolling_list_controller
        self._simulation_controller = simulation_controller
        self._scrolling_list_controller = scrolling_list_controller
        self._text_box_controller = text_box_controller

        self._start_button = Button(
            "Start simulation",
            self.start_action,
            enabled=False
        )

        # Création de la map des boutons et leurs vues
        self._button_map = {
            self._start_button: ButtonView(
                parameters_view.screen,
                self._start_button.text,
                PARAMETERS_WINDOW_WIDTH - 140 - 10,
                PARAMETERS_WINDOW_HEIGHT - 40 - 10,
                140,
                40,
                color=Colors.BUTTON_GREEN,
                hover_color=Colors.BUTTON_GREEN_HOVER
            )
        }

    def start_action(self) -> None:
        """
        Starts the simulation by initializing agents and launching the
        selected algorithm.
        """

        if self._graph_controller.is_graph_modified():
            self._graph_controller.save_graph()
            success = self._compute_store_and_save_graph_data()
            if success:
                self._launch_algorithm()
            else:
                self._graph_controller.raise_error_message('The graph must not have isolated subgraphs')
        
        elif not self._graph_controller.are_complements_saved():
            success = self._compute_store_and_save_graph_data()
            if success:
                self._launch_algorithm()
            else:
                self._graph_controller.raise_error_message('The graph must not have isolated subgraphs')

        elif self._graph_controller.are_complements_saved():
            self._launch_algorithm()

    def _compute_store_and_save_graph_data(self):
        """
        Computes, stores, and saves the complete graph and shortest paths.
        """
        graph_data = self.compute_complete_graph_and_shortest_paths()
        if not graph_data.adjacency_matrix:
            return False
        if not graph_data.shortest_paths:
            raise ValueError('Shortest paths dictionnary is null while Complete Graph array exists.')
    
        self._graph_controller.store_complements_to_model(graph_data.complements)

        self._graph_controller.save_complements(graph_data.complements)
        return True

    def _launch_algorithm(self) -> None:
        """
        Launches the selected algorithm and starts the simulation.
        """
        self._graph_controller.raise_info('Algorithm launched')
        selected_algorithm = self._scrolling_list_controller.get_selected_algorithm()
        
        # TODO: interface for all the algorithm that owns a launch() method,
        # that all the algorithm 
        try:
            nb_agents =  int(self._text_box_controller.text_content)
        except ValueError:
            self._graph_controller.raise_error_message('Invalid number of agents. Please enter a valid integer.')
            return

        graph = self._graph_controller.graph
        self._algorithm = selected_algorithm.initialize_algorithm(nb_agents, graph)
        
        solution: list[list[int]] = self._algorithm.launch()

        # Convert the solution paths to use the shortest paths in the real graph
        real_paths = []
        for agent_path in solution:
            real_path = []
            for i in range(len(agent_path) - 1):
                start_node = agent_path[i]
                end_node = agent_path[i + 1]
                real_path.extend(self._graph_controller.graph.get_shortest_paths()[(start_node, end_node)])
                real_paths.append(real_path)
            # Ajouter le chemin de retour au premier nœud
            if (len(agent_path) > 1):
                start_node = agent_path[-1]
                end_node = agent_path[0]
                real_path.extend(self._graph_controller.graph.get_shortest_paths()[(start_node, end_node)])
                
                real_paths.append(real_path)

        # Initializing agents with the real paths
        self._simulation_controller.initialize_agents(real_paths)


        # Setting the simulation as started
        self._simulation_controller.set_simulation_started(True)
            
    def compute_complete_graph_and_shortest_paths(self):
        """
        Computes the complete graph and shortest paths using the A*
        algorithm.

        Returns:
            GraphData: An instanciation of GraphData class containing
                all the data about shortest paths, adjacency matrix,
                complete adjacency matrix and nodes list.
        """
        simple_graph, node_positions = self._graph_controller._graph.compute_matrix()
        complete_graph = self._complete_graph_service(
            simple_graph=simple_graph,
            node_position=node_positions,
            path_finding_service=AStarService
        ).complete_graph

        shortest_paths = {}
        for start in range(len(simple_graph)):
            for end in range(len(simple_graph)):
                if start != end:
                    a_star = AStarService(simple_graph,
                                          node_positions,
                                          start,
                                          end)
                    # We don't want to store the cost
                    shortest_paths[(start, end)] = a_star.find_path()[0] 

        return GraphData(
            adjacency_matrix=simple_graph,
            nodes_list=node_positions,
            complete_adjacency_matrix=complete_graph,
            shortest_paths=shortest_paths
        )

    def enable_start_button(self) -> None:
        """
        Enables the "Start simulation" button, allowing the user to
        start the simulation.
        """
        self._start_button.enabled = True

    def disable_start_button(self) -> None:
        """
        Disables the "Start simulation" button, preventing the user
        from starting the simulation.
        """
        self._start_button.enabled = False
