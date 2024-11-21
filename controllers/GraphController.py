import os
import re

import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, NODE_RADIUS
from views.GraphView import GraphView
from controllers.NodeController import NodeController
from controllers.EdgeController import EdgeController
from controllers.NodeController import NodeController
from models.Agent import Agent
from models.Graph import Graph
from services import IImageService
from services.ICSVService import ICSVService


class GraphController:
    """
    Controller for managing the graph's operations and user interactions.
    """

    def __init__(self, screen, csv_service: ICSVService, image_service: IImageService) -> None:
        self.graph = Graph()
        self.csv_service = csv_service
        self.image_service = image_service

        self.disable_mark = False

        # Initialize the view
        self.graph_view = GraphView(screen.subsurface((0, 0, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)))

        # Initialize node and edge controllers
        self.node_controller = NodeController(self.graph)
        self.edge_controller = EdgeController(self.graph, self.node_controller)

        # Load initial background image
        self.image_name = "image1.jpg"
        self.load_background_image(self.image_name)

    def mark_graph_as_modified(func):
        def wrapper(self, *args, **kwargs):
            if not self.disable_mark:
                result = func(self, *args, **kwargs)
                self.graph.mark_as_modified()
                return result
            return func(self, *args, **kwargs)
        return wrapper

    @mark_graph_as_modified
    def add_node(self, pos):
        self.node_controller.add_node(pos)

    @mark_graph_as_modified
    def delete_node(self, node):
        self.node_controller.delete_node(node)

    @mark_graph_as_modified
    def drag_node(self, pos):
        self.node_controller.drag_node(pos)

    @mark_graph_as_modified
    def create_link(self, pos):
        self.edge_controller.create_link(pos)

    def select_node(self, node):
        self.node_controller.select_node(node)
        
    def start_drag(self, pos):
        self.node_controller.start_drag(pos)
    
    def end_drag(self):
        self.node_controller.end_drag()

    def clear_selection(self):
        self.node_controller.clear_selection()

    def is_graph_modified(self):
        return self.graph.is_modified()
    
    def is_graph_empty(self):
        return self.graph.is_empty()

    def load_background_image(self, image_name: str) -> None:
        """
        Load and scale the background image for the view.
        The image service ensures the image exists, but the view sets the background.
        """
        # Ensure the image exists in the "backgrounds" folder
        image_path = os.path.join("backgrounds", image_name)
        self.image_service.ensure_image_exists_and_copy(image_path)

        # Check if the image exists in the folder
        if self.image_service.check_if_image_exists(image_path):
            background_image = pygame.image.load(image_path)
            background_image = pygame.transform.scale(background_image, (GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
            self.graph_view.set_background_image(background_image)
        else:
            print(f"Image {image_name} not found or could not be copied.")
            self.graph_view.set_background_image(None)


    def handle_event(self, event) -> None:
        """
        Handle user mouse events for graph interactions.
        """
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            node = self.node_controller.get_node_at_position(pos)
            if event.button == 1:
                self.handle_left_click(pos, node)
            elif event.button == 3 and node is not None:
                self.handle_right_click(pos, node)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.end_drag()

        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if self.is_within_bounds(pos):
                self.drag_node(pos)

    def handle_left_click(self, pos, node) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] and node is not None:
            self.delete_node(node)
        else:
            self.clear_selection()
            self.start_drag(pos)
            if node is None and self.is_within_bounds(pos):
                self.add_node(pos)

    def handle_right_click(self, pos, node) -> None:
        self.create_link(pos)
        self.select_node(node)

    def is_within_bounds(self, pos) -> bool:
        return (NODE_RADIUS < pos[0] < GRAPH_WINDOW_WIDTH - NODE_RADIUS and
                NODE_RADIUS < pos[1] < GRAPH_WINDOW_HEIGHT - NODE_RADIUS)

    def update(self) -> None:
        """
        Update the view with the current state of the graph.
        """
        self.graph_view.draw_graph(self.graph, self.node_controller.selected_node, self.node_controller.dragging_node)

    def save_graph(self) -> None:
        edges_matrix, nodes_list = self.graph.compute_matrix()
        self.csv_service.save(edges_matrix, nodes_list, self.image_name)

    def save_complements(self, complete_graph, shortest_paths) -> None:
        '''
        This method saves the complete graph and shortest paths into the CSV file.
        '''
        self.csv_service.save_complements(complete_graph, shortest_paths, self.image_name)

    def load_graph(self, num_file) -> None:
        edges_matrix, nodes_list = self.csv_service.load_from_num_file(num_file)
        if edges_matrix and nodes_list:
            self.graph.nodes = {i: coords for i, coords in enumerate(nodes_list)}
            self.graph.edges = {(i, j) for i, row in enumerate(edges_matrix) for j, distance in enumerate(row) if distance > 0}
            print("Edges matrix:", edges_matrix)
            print("Nodes list:", nodes_list)

    def clear_graph(self) -> None:
        self.graph.nodes.clear()
        self.graph.edges.clear()

    def load_graph_from_csv(self, file_number: str) -> None:
        """
        Load a graph from a CSV file based on the file number, and update the graph with nodes and edges.
        """
        edges_matrix, nodes_list = self.csv_service.load_from_num_file(file_number)
        self._load_graph(edges_matrix, nodes_list)

    def import_graph_from_image(self, image_path) -> None:
        """
        Import a graph based on an image file, check if a CSV file is associated with it, and display it.
        """
        image_name = os.path.basename(image_path)

        if not self.image_service.is_an_image(image_path):
            print(f"{image_path} is not a valid image file.")
            return

        # If the image is not found in the project folder, copy it there
        self.image_service.ensure_image_exists_and_copy(image_path)
        self.image_name = image_name
        csv_path = self.csv_service.find_csv_reference(image_name)

        # load the image as background
        self.load_background_image(self.image_name)

        # if the image has no associated csv file, display it only
        if csv_path is None:
            print(f"{image_name} not found in references.csv. Displaying image only.")
            self.clear_graph()
            self.update()
            return

        # if a csv file exists, load the associated graph
        match = re.search(r'graph_(\d+)\.csv', csv_path)
        if match:
            file_number = match.group(1)
            self.load_graph_from_csv(file_number)
        else:
            raise ValueError("Path does not match expected format.")

    def import_graph_from_csv(self, csv_path) -> None:
        """
        Import a graph based on a CSV file, and display it.
        """
        if not csv_path.endswith('.csv'):
            print(f"{csv_path} is not a valid CSV file.")
            return

        self.image_name = self.csv_service.get_image_name(csv_path).strip()
        self.load_background_image(self.image_name)
        edges_matrix, nodes_list = self.csv_service.load(csv_path)
        self._load_graph(edges_matrix, nodes_list)

    def _load_graph(self, edges_matrix, nodes_list) -> None:
        """
        A helper method to load the nodes and edges into the graph, reducing duplication.
        """
        if edges_matrix and nodes_list:
            self.clear_graph()
            for coords in nodes_list:
                self.node_controller.add_node(coords)
            for i, row in enumerate(edges_matrix):
                for j, distance in enumerate(row):
                    if distance > 0:
                        node1 = self.graph.nodes[i]
                        node2 = self.graph.nodes[j]
                        self.graph.add_edge(node1, node2)
            self.update()
            print("Graph imported and displayed successfully.")
        else:
            print("No valid graph data found in the CSV file.")

    def graph_has_an_image(self) -> bool:
        return self.graph_view.has_an_image()
    
    def draw_simulation(self, agents: list[Agent]) -> None:
        self.graph_view.draw_simulation(agents)
    
    def get_graph(self) -> Graph:
        return self.graph    
    def are_complements_not_saved(self):
        return self.csv_service.are_complements_not_saved(self.image_name)
