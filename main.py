import pygame
from controllers.ViewController import ViewController
from services.CSVService import CSVService

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("AI50 patrolling problem")
clock = pygame.time.Clock()

csv_service = CSVService()
view_controller = ViewController(csv_service)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        view_controller.handle_actions(event)

    # Redessine tous les éléments de l'interface et de la simulation
    view_controller.draw()  # Dessine les éléments statiques de l'interface
    view_controller.parameters_controller.update_and_draw_simulation()  # Met à jour et dessine les agents

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
