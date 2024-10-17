from models.Button import Button
from views.ButtonView import ButtonView
import pygame

class ButtonController:
    def __init__(self, parameters_view, graph_controller) -> None:
        self.parameters_view = parameters_view
        self.graph_controller = graph_controller

        # Création des modèles de boutons, 1 de chaque type (save, import, clear)
        self.buttons = [
            Button("Save", self.save_action),
            Button("Import", self.import_action),
            Button("Clear", self.clear_action)
        ]
        
        # Création des vues de chaque bouton
        self.button_views = [
            ButtonView(parameters_view.screen, button.text, button.action, 10 + i * 130, 10, 120, 40)
            for i, button in enumerate(self.buttons)
        ]

    def draw_buttons(self) -> None:
        '''
        Cette méthode dessine l'intégralité des boutons sur la vue.
        '''
        for button_view in self.button_views:
            button_view.draw()

    def handle_click(self, event) -> None:
        '''
        Gère l'événement de clic sur les boutons.

        Cette méthode vérifie si l'événement reçu correspond à un clic gauche de souris. 
        Si tel est le cas, elle déclenche l'action associée au bouton sur lequel l'utilisateur a cliqué.

        Args:
            event: L'événement Pygame contenant des informations sur le clic de souris.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - 960, event.pos[1])
            for button, button_view in zip(self.buttons, self.button_views):
                if button_view.is_clicked(mouse_pos):
                    button.action()

    def save_action(self) -> None:
        '''
        Cette méthode sauvegarde un graphe sur l'ordinateur lorsque le bouton Save est cliqué.
        '''
        self.graph_controller.save_graph()
        print("Save action triggered")

    def import_action(self) -> None:
        '''
        Cette méthode importe un graphe depuis l'ordinateur lorsque le bouton Import est cliqué.
        '''
        self.graph_controller.load_graph(1)
        print("Import action triggered")

    def clear_action(self) -> None:
        '''
        Cette méthode nettoie l'intégralité de la vue du graphe lorsque le bouton Clear est cliqué.
        '''
        print("Clear action triggered")
