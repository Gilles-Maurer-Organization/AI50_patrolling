import os
import shutil
import tkinter as tk
from tkinter import filedialog
import re

import pygame

from constants.Config import GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT, NODE_RADIUS
from controllers.EdgeController import EdgeController
from controllers.NodeController import NodeController
from models.Graph import Graph
from services.ICSVService import ICSVService
from views.GraphView import GraphView


class GraphController:
    """
    Controller for managing the graph's operations and user interactions.
    """

    def __init__(self, screen, csv_service: ICSVService) -> None:
        self.graph = Graph()
        self.csv_service = csv_service

        # Initialize the view
        self.graph_view = GraphView(screen, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT)

        # Initialize node and edge controllers
        self.node_controller = NodeController(self.graph)
        self.edge_controller = EdgeController(self.graph, self.node_controller)

        # Set up Tkinter for file dialog
        self.root = tk.Tk()
        self.root.withdraw()

        # Load initial background image
        self.image_name = "image1.jpg"
        self.load_background_image(self.image_name)

    def load_background_image(self, image_name: str) -> None:
        """
        Load and scale the background image for the view.
        """
        background_image = pygame.image.load(image_name)
        background_image = pygame.transform.scale(background_image, (GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT))
        self.graph_view.set_background_image(background_image)

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
            self.node_controller.end_drag()

        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if self.is_within_bounds(pos):
                self.node_controller.drag_node(pos)

    def handle_left_click(self, pos, node) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] and node is not None:
            self.node_controller.delete_node(node)
        else:
            self.node_controller.clear_selection()
            self.node_controller.start_drag(pos)
            if node is None and self.is_within_bounds(pos):
                self.node_controller.add_node(pos)

    def handle_right_click(self, pos, node) -> None:
        self.edge_controller.create_link(pos)
        self.node_controller.select_node(node)

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

    def load_graph(self, num_file) -> None:
        edges_matrix, nodes_list = self.csv_service.load(num_file)
        if edges_matrix and nodes_list:
            self.graph.nodes = {i: coords for i, coords in enumerate(nodes_list)}
            self.graph.edges = {(i, j) for i, row in enumerate(edges_matrix) for j, distance in enumerate(row) if distance > 0}
            print("Edges matrix:", edges_matrix)
            print("Nodes list:", nodes_list)

    def clear_graph(self) -> None:
        self.graph.nodes.clear()
        self.graph.edges.clear()

    def open_file_dialog_and_import_graph(self):
        image_path = filedialog.askopenfilename(
            title="Select a graph image",
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        image_name = os.path.basename(image_path)

        if image_name:
            self.import_graph_from_image(image_path)

    def import_graph_from_image(self, image_path):
        image_name = os.path.basename(image_path)
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("Selected file is not an image.")
            return

        self.image_name = image_name
        csv_path = self.csv_service.find_csv_reference(image_name)

        if csv_path is None:
            print(f"{image_name} not found in references.csv. Displaying image only.")
            shutil.copy(image_path, image_name)
            self.load_background_image(self.image_name)
            self.clear_graph()
            self.update()
            return

        self.load_background_image(self.image_name)
        match = re.search(r'graph_(\d+)\.csv', csv_path)

        if match:
            file_number = match.group(1)
            edges_matrix, nodes_list = self.csv_service.load(file_number)

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

            print("Edges matrix:", edges_matrix)
            print("Nodes list:", nodes_list)

            self.update()
            print("Graph imported and displayed successfully.")
        else:
            raise ValueError("Path does not match expected format.")
