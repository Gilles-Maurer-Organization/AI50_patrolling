import numpy as np
import pygame

class Agent:
    """
    This class represents an agent that follows a predefined path
    through a graph.

    Attributes:
        path (list): The sequence of node indices that defines the path.
        current_index (int): The index of the current node in the path.
        graph (Graph): The graph containing the nodes of the path.
        x (float): The x coordinate of the agent's current position.
        y (float): The y coordinate of the agent's current position.
        speed (float): The speed at which the agent moves.
    """
    def __init__(self, path, graph):
        """
        Initializes an agent with a specified path and graph.

        Args:
            path (list): The path as a list of node indices.
            graph (Graph): The graph containing the nodes.
        """
        self.path = path
        self.current_index = 0
        self.graph = graph

        initial_node = self.graph.nodes[self.path[self.current_index]]
        self.x, self.y = initial_node.x, initial_node.y
        self.speed = 2

    def move(self):
        """
        Moves the agent toward the next node in the path.

        If the agent reaches the target node, it moves to the next
        node in the path. The movement is normalized to ensure smooth
        progression at the specified speed.
        """
        if self.current_index < len(self.path) - 1:
            # Move to the next node
            target_node = self.graph.nodes[self.path[self.current_index + 1]]
            target_x, target_y = target_node.x, target_node.y
            dx = target_x - self.x
            dy = target_y - self.y
            distance = np.sqrt(dx ** 2 + dy ** 2)

            if distance != 0:
                # Normalize the movement by distance and apply speed
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

            # Check if the agent has reached his target node
            if distance < self.speed:
                self.current_index += 1

    def reset_path(self):
        """
        Resets the agent's path to start again from the first node.
        """
        self.current_index = 0
        start_node = self.graph.nodes[self.path[self.current_index]]
        self.x, self.y = start_node.x, start_node.y
