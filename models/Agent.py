import numpy as np

class AgentModel:
    def __init__(self, path, graph):
        self.path = path
        self.current_index = 0
        self.graph = graph
        self.finished = False  # Indicateur de fin de parcours

        initial_node = self.graph.nodes[self.path[self.current_index]]
        self.x, self.y = initial_node.x, initial_node.y
        self.speed = 2

    def move(self):
        '''
        Déplace l'agent vers le prochain nœud dans le chemin.
        '''
        if not self.finished and self.current_index < len(self.path) - 1:
            target_node = self.graph.nodes[self.path[self.current_index + 1]]
            target_x, target_y = target_node.x, target_node.y
            dx = target_x - self.x
            dy = target_y - self.y
            distance = np.sqrt(dx ** 2 + dy ** 2)

            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

            if distance < self.speed:
                self.current_index += 1

        if self.current_index >= len(self.path) - 1:
            self.finished = True

    def reset_path(self):
        '''
        Réinitialise le chemin de l'agent pour recommencer depuis le premier nœud.
        '''
        self.current_index = 0
        start_node = self.graph.nodes[self.path[self.current_index]]
        self.x, self.y = start_node.x, start_node.y
        self.finished = False
