import pygame
from controllers.ViewController import ViewController
from services.CSVService import CSVService
from services.ImageService import ImageService

pygame.init()
pygame.display.set_caption("AI50 patrolling problem")
clock = pygame.time.Clock()

csv_service = CSVService()
image_service = ImageService()
view_controller = ViewController(csv_service, image_service)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            csv_service.stop_timer()

        view_controller.handle_actions(event)

    view_controller.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()