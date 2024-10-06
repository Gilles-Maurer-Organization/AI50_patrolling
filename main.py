import pygame
from models.Graph import Graph
from views.GraphView import GraphView
from controllers.GraphController import GraphController
from controllers.CSVController import CSVController

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre (1/2 de 1920 par 1080)
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Chargement de l'image d'arrière plan
# TODO : Chargement dynamique, cf. Arnaud
background_image = pygame.image.load("image1.jpg")
# Mise à jour des dimensions de l'image d'arrière plan par rapport à la taille de la fenêtre de graph
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialisation du modèle de graph
graph = Graph()

# Initialisation de la vue de graph
graph_view = GraphView(screen, background_image)

# Initialisation du controller de graph
graph_controller = GraphController(graph, graph_view)
edges_matrix, nodes_list = graph.compute_matrix()

# Initialisation du controller de CSV
csv_controller = CSVController()

running = True
is_saved = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # On vérifie les événements de l'utilisateur dès qu'une action est réalisée tout au long du programme (pour le moment, voué à être modifié)
        graph_controller.handle_event(event)
    
    # Une fois l'événement géré, on met à jour la vue à l'aide du controller
    graph_controller.update()
    
    # TODO : Créer des boutons appropriés pour save le graphe
    keys = pygame.key.get_pressed()
    # Si la touche S est enfoncée, on vérifie si ça a déjà été save
    if keys[pygame.K_s] and not is_saved:
        # S'il n'a pas encore été save, on sauvegarde le nouveau graphe
        graph_controller.save_graph()
        # On indique qu'il a été sauvegardé
        is_saved = True

    # Si la touche L est enfoncée, on charge un graphe déjà existant
    if keys[pygame.K_l]:
        graph_controller.load_graph(1)

    pygame.display.flip()

pygame.quit()
