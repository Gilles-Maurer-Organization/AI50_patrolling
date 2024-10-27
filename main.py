import pygame

from controllers.ViewController import ViewController
from services.CSVService import CSVService

from services.CSVService import CSVService

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("AI50 patrolling problem")

clock = pygame.time.Clock()

csv_service = CSVService()
view_controller = ViewController(csv_service)

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

    # On limite le coût en CPU en ajoutant une limite de 30 fps pour notre programme,
    # largement suffisant pour le programme réalisé.
    clock.tick(30)

pygame.quit()
