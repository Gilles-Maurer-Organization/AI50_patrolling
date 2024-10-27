import pygame

from controllers.ViewController import ViewController

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("AI50 patrolling problem")

# TODO : déplacer la référence background_image, elle n'a pas de l ien direct avec la vue générale mais seulement avec la GraphView
view_controller = ViewController()

running = True
is_saved = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # On vérifie les événements de l'utilisateur dès qu'une action est réalisée tout au long du programme
        # (pour le moment, voué à être modifié, il ne faut pas les vérifier tout au long de la vie du programme)
        view_controller.handle_actions(event)
    
    # Une fois l'événement géré, on met à jour la vue
    view_controller.draw()

    pygame.display.flip()
    
pygame.quit()
