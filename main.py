import pygame
from models.Graph import Graph
from views.View import View
from controllers.GraphController import GraphController
from controllers.CSVController import CSVController

# Initialisation de Pygame
pygame.init()

# Initialisation du modèle de graphe
graph = Graph()

# TODO : déplacer la référence background_image, elle n'a pas de lien direct avec la vue générale mais seulement avec la GraphView
view = View()
view.initialize_graph_view()

# Initialisation du controller de graphe
graph_controller = GraphController(graph, view.get_graphView())

view.initialize_parameters_view(graph_controller)

edges_matrix, nodes_list = graph.compute_matrix()

# Initialisation du controller de CSV
csv_controller = CSVController()
    
running = True
is_saved = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # On vérifie les événements de l'utilisateur dès qu'une action est réalisée tout au long du programme
        # (pour le moment, voué à être modifié, il ne faut pas les vérifier tout au long de la vie du programme)
        graph_controller.handle_event(event)
        
        view.handle_actions(event)
    
    # Une fois l'événement géré, on met à jour la vue
    view.draw(graph_controller)

    pygame.display.flip()
    
pygame.quit()
