import pygame

class ButtonController:
    def __init__(self, button_model: ButtonModel, button_view: ButtonView) -> None:
        self.model = button_model
        self.view = button_view

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and self.view.is_clicked(event.pos):
            self.model.action()  # Exécuter l'action du modèle associé