import os
import re

import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT
from controllers.EdgeController import EdgeController
from controllers.NodeController import NodeController
from models.Agent import Agent
from models.Graph import Graph
from models.GraphData import GraphData
from models.GraphDataComplements import GraphDataComplements
from models.Node import Node
from services import IImageService
from services.ICSVService import ICSVService
from views.AgentView import AgentView
from views.GraphView import GraphView


class GraphController:
    """
    This class manages the graph's operations and user interactions.

    The GraphController is responsible for handling user input,
    managing the graph's model (nodes, edges), and updating the
    graphical view. It also integrates with CSV and image services to
    enable saving/loading graphs and importing images as graph
    backgrounds.

    Attributes:
        _graph: The graph model, representing nodes and edges.
        _csv_service: A service for managing CSV file operations.
        _image_service: A service for handling image-related tasks.
        _graph_view: The view responsible for rendering the graph.
        _node_controller: The controller managing individual nodes.
        _edge_controller: The controller managing edges and links
            between nodes.
        _image_name: The name of the current background image for the
            graph.
        _disable_mark: A flag to temporarily disable marking the graph
            as modified.
    """

    def __init__(self,
                 screen: pygame.Surface,
                 csv_service: ICSVService,
                 image_service: IImageService
                 ) -> None:
        self._graph = Graph()
        self._csv_service = csv_service
        self._image_service = image_service

        self._disable_mark = False

        # Initialize the view
        self._graph_view = GraphView(
            screen.subsurface((0, 0, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        )

        # Initialize node and edge controllers
        self._node_controller = NodeController(self._graph)
        self._edge_controller = EdgeController(
            self._graph,
            self._node_controller
        )

        self._image_name = ""

        self._alignment_lines = {}
        self._snapping_enabled = False

        self._is_in_simulation = False

    @property
    def graph(self) -> Graph:
        """
        Returns the current graph model.

        Returns:
            Graph: The graph model.
        """
        return self._graph
    
    @property
    def is_in_simulation(self):
        return self._is_in_simulation

    @is_in_simulation.setter
    def is_in_simulation(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_in_simulation must be a boolean")
        self._is_in_simulation = value

    def mark_graph_as_modified(func):
        """
        Decorator to mark the graph as modified when a function makes
        changes.

        Args:
            func: The function to be wrapped by the decorator.
        """
        def wrapper(self, *args, **kwargs):
            if not self._disable_mark:
                result = func(self, *args, **kwargs)
                self._graph.mark_as_modified()
                return result
            return func(self, *args, **kwargs)
        return wrapper

    @mark_graph_as_modified
    def _add_node(self, pos: tuple[int, int]) -> None:
        """
        Adds a new node to the graph at a specified position.

        Args:
            pos: A tuple representing the (x, y) coordinates of the new
                node.
        """
        self._node_controller.add_node(pos)

    @mark_graph_as_modified
    def _delete_node(self, node: Node) -> None:
        """
        Deletes a specified node from the graph.

        Args:
            node: The node to be removed from the graph.
        """
        self._node_controller.delete_node(node)

    @mark_graph_as_modified
    def _drag_node(self, pos: tuple[int, int]) -> None:
        """
        Drags the currently selected node to a new position.

        Args:
            pos: A tuple representing the (x, y) coordinates of the new
                position.
        """
        candidates = self._node_controller.drag_node(pos, self._snapping_enabled)

        if candidates:
            self._alignment_lines = candidates

    @mark_graph_as_modified
    def _create_link(self, pos: tuple[int, int]) -> None:
        """
        Creates a link between two nodes based on the given position.

        Args:
            pos: A tuple representing the (x, y) position where the
                link is initiated.
        """
        self._edge_controller.create_link(pos)

    def _select_node(self, node: Node) -> None:
        """
        Selects a node in the graph.

        Args:
            node: The node to be selected.
        """
        self._node_controller.select_node(node)
        
    def _start_drag(self, pos: tuple[int, int]) -> None:
        """
        Starts the dragging operation for a node.

        Args:
            pos: A tuple representing the initial (x, y) position of
                the drag.
        """
        self._node_controller.start_drag(pos)
    
    def _end_drag(self) -> None:
        """
        Ends the current node dragging operation.
        """
        self._node_controller.end_drag()
        self._alignment_lines.clear()

    def _clear_selection(self) -> None:
        """
        Clears the current selection of nodes in the graph.
        """
        self._node_controller.clear_selection()

    def is_graph_modified(self) -> bool:
        """
        Checks if the graph has been modified since the last save.

        Returns:
            bool: True if the graph has been modified, otherwise False.
        """
        return self._graph.modified
    
    def is_graph_empty(self) -> bool:
        """
        Checks if the graph is empty (contains no nodes or edges).

        Returns:
            bool: True if the graph is empty, otherwise False.
        """
        return self._graph.empty

    def _load_background_image(self, image_name: str) -> None:
        """
        Loads and scales the background image for the graph view.

        Args:
            image_name: The name of the image file to be loaded.
        """
        # Ensure the image exists in the "backgrounds" folder
        image_path = os.path.join("backgrounds", image_name)
        self._image_service.ensure_image_exists_and_copy(image_path)

        # Check if the image exists in the folder
        if self._image_service.check_if_image_exists(image_path):
            background_image = pygame.image.load(image_path)
            self._graph_view.set_background_image(background_image)
        else:
            print(f"Image {image_name} not found or could not be copied.")
            self._graph_view.set_background_image(None)


    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles user input events such as mouse clicks and motions.

        Args:
            event: The event triggered by user interaction.
        """
        pos = pygame.mouse.get_pos()

        # TODO : Si en simulation alors on bloque ça 

        if not self.is_in_simulation:
            if event.type == pygame.MOUSEBUTTONDOWN:
                node = self._node_controller.get_node_at_position(pos)
                if event.button == 1:
                    self._handle_left_click(pos, node)
                elif event.button == 3 and node is not None:
                    self._handle_right_click(pos, node)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._end_drag()

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if self._is_within_bounds(pos):
                    self._drag_node(pos)

    def _handle_left_click(self, pos: tuple[int, int], node: Node) -> None:
        """
        Handles a left-click event in the graph.

        If the CTRL key is pressed and a node is selected, the node is
        deleted.

        Otherwise:
        - Clears any current node selection.
        - Starts dragging a node if a valid one exists.
        - Adds a new node if none exists at the clicked position and
            the position is within bounds.

        Args:
            pos: A tuple (x, y) representing the position of the mouse
                click.
            node: The node located at the clicked position, if any.
        """
        if not self.graph_has_an_image() and self.is_graph_empty():
            return

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_LCTRL]
            or keys[pygame.K_RCTRL]
            and node is not None
            ):
            self._delete_node(node)
        else:
            self._clear_selection()
            self._start_drag(pos)
            if node is None and self._is_within_bounds(pos):
                self._add_node(pos)

    def _handle_right_click(self, pos: tuple[int, int], node: Node) -> None:
        """
        Handles a right-click event in the graph.

        Performs the following actions:
        - Creates a link at the clicked position.
        - Selects the node at the clicked position, if any.

        Args:
            pos: A tuple (x, y) representing the position of the mouse
                click.
            node: The node located at the clicked position, if any.
        """
        self._create_link(pos)
        self._select_node(node)

    def _is_within_bounds(self, pos) -> bool:
        """
        Checks if the given position is within the bounds of the graph view.

        Args:
            pos (tuple[int, int]): The position to check.

        Returns:
            bool: True if the position is within bounds, otherwise False.
        """
        bounds = self._graph_view.get_image_bounds()
        margin_left = bounds["margin_left"]
        margin_top = bounds["margin_top"]
        scaled_width = bounds["scaled_width"]
        scaled_height = bounds["scaled_height"]

        return (margin_left < pos[0] < margin_left + scaled_width and
                margin_top < pos[1] < margin_top + scaled_height)

    def update(self) -> None:
        """
        Updates the graph view to reflect the current state of the model.
        """
        self._graph_view.draw_graph(
            self._graph,
            self._node_controller.selected_node,
            self._node_controller.dragging_node
        )
        self._graph_view.draw_popup()
        self._draw_alignment_lines()
        
    def _draw_alignment_lines(self) -> None:
        """
        Draws the alignment's line for each candidate found.
        """
        for axis, candidate in self._alignment_lines.items():
            if candidate:
                self._graph_view.draw_line_full_extent(
                    candidate,
                    axis,
                )

    def save_graph(self) -> None:
        """
        Saves the graph's structure (nodes and edges) to a CSV file.
        """
        edges_matrix, nodes_list = self._graph.compute_matrix()
        self._csv_service.save(edges_matrix, nodes_list, self._image_name)

    def save_complements(
        self,
        graph_data_complements: GraphDataComplements
    ) -> None:
        """
        Saves additional data such as the complete graph and shortest
        paths.

        Args:
            graph_data_complements (GraphDataComplements): The
                complements of the Graph such as the complete
                adjacency matrix and the shortest paths
        """
        self._csv_service.save_complements(
            graph_data_complements,
            self._image_name
        )

    def clear_graph(self) -> None:
        """
        Clears all nodes and edges from the graph.
        """
        self._graph.nodes.clear()
        self._graph.edges.clear()

    def load_graph_from_csv(self, file_number: str) -> None:
        """
        Loads a graph's data from a CSV file based on the given file number.

        Args:
            file_number: The number of the CSV file to load.
        """
        graph_data = self._csv_service.load_from_num_file(file_number)

        self._load_graph(graph_data)

    def import_graph_from_image(self, image_path: str) -> None:
        """
        Imports a graph background from an image file.

        Args:
            image_path: The path to the image file to be imported.
        """
        image_name = os.path.basename(image_path)

        if not self._image_service.is_an_image(image_path):
            raise ValueError(f"{image_path} is not a valid image file.")

        # If the image is not found in the project folder, copy it there
        self._image_service.ensure_image_exists_and_copy(image_path)
        self._image_name = image_name
        csv_path = self._csv_service.find_csv_reference(image_name)

        # load the image as background
        self._load_background_image(self._image_name)

        # if the image has no associated csv file, display it only
        if csv_path is None:
            print(f"{image_name} not found in references.csv.\
                  Displaying image only.")
            self.clear_graph()
            self.update()
            return

        # if a csv file exists, load the associated graph
        match = re.search(r'graph_(\d+)\.csv', csv_path)
        if match:
            file_number = match.group(1)
            self.load_graph_from_csv(file_number)
        else:
            raise ValueError(f"Unexpected CSV path format: {csv_path}")

    def import_graph_from_csv(self, csv_path: str) -> None:
        """
        Imports a graph's data from a specified CSV file.

        Args:
            csv_path: The path to the CSV file to be imported.
        """
        if not csv_path.endswith('.csv'):
            print(f"{csv_path} is not a valid CSV file.")
            return

        self._image_name = self._csv_service.get_image_name(csv_path).strip()
        self._load_background_image(self._image_name)
        graph_data = self._csv_service.load(csv_path)
        
        self._load_graph(graph_data)

    def _load_graph(self, graph_data: GraphData) -> None:
        """
        Loads a graph's structure and metadata into the model.

        Args:
            graph_data (GraphData): The Graph data containing
                the adjacency matrix, the nodes list and the
                graph's complements.
        """
        if graph_data.adjacency_matrix and graph_data.nodes_list:
            self.clear_graph()
            for coords in graph_data.nodes_list:
                self._node_controller.add_node(coords)
            for i, row in enumerate(graph_data.adjacency_matrix):
                for j, distance in enumerate(row):
                    if distance > 0:
                        node1 = self._graph.nodes[i]
                        node2 = self._graph.nodes[j]
                        self._graph.add_edge(node1, node2)
            self.store_complements_to_model(
                graph_data
            )

            self.update()
            print("Graph imported and displayed successfully.")
        else:
            print("No valid graph data found in the CSV file.")

    def graph_has_an_image(self) -> bool:
        """
        Checks if the graph currently has a background image.

        Returns:
            bool: True if a background image is set, otherwise False.
        """
        return self._graph_view.has_an_image()
    
    def draw_simulation(self, agents: list[Agent]) -> None:
        """
        Draws a simulation of agents view moving on the graph.

        Args:
            agents: A list of agents view to be simulated on the graph.
        """
        self._graph_view.draw_simulation(agents)
    
    def are_complements_saved(self):
        """
        Checks if complements (e.g., shortest paths and complete graph)
        are saved for the graph.

        Returns:
            bool: True if complements are saved, otherwise False.
        """
        return self._csv_service.are_complements_saved(self._image_name)

    def store_complements_to_model(
        self,
        graph_data_complements: GraphDataComplements
    ) -> None:
        """
        Stores complement data like adjacency matrices and shortest
        paths into the model.

        Args:
            graph_data_complements (GraphDataComplements): The
                complements of the Graph such as the complete
                adjacency matrix and the shortest paths
        """
        if graph_data_complements.complete_adjacency_matrix:
            self._graph.set_complete_adjacency_matrix(
                graph_data_complements.complete_adjacency_matrix
            )
            if not graph_data_complements.shortest_paths:
                raise ValueError("Shortest paths are missing despite a \
                                 complete adjacency matrix being present.")
            else:
                self._graph.set_shortest_paths(
                    graph_data_complements.shortest_paths
                )

    def raise_error_message(self, message: str) -> None:
        """
        This method triggers an error popup with a specific message.
        """
        self._graph_view.show_error_popup(message)

    def raise_info(self, message: str) -> None:
        """
        This method triggers an error popup with a specific message.
        """
        self._graph_view.show_info_popup(message)

    
    def raise_message(self, message: str) -> None:
        """
        This method triggers an error popup with a specific message.
        """
        self._graph_view.show_popup(message)

    def set_snapping_enabled(self, snapping_enabled) -> None:
        self._snapping_enabled = snapping_enabled