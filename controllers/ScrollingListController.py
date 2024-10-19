from views.ScrollingListView import ScrollingListView

from models.ScrollingList import ScrollingList

import pygame

class ScrollingListController:
    def __init__(self, parameters_view) -> None:
        self.parameters_view = parameters_view
        self.scrolling_list = ScrollingList('algorithm', ['naive algorithm', 'ant colony algorithm', 'evolutional algorithm'])
        self.scrolling_list_view = ScrollingListView(parameters_view.screen, 10, 110, 290, 40)

    def draw_scrolling_list(self) -> None:
        self.scrolling_list_view.draw()

    def is_scrolling_list_hovered(self, event):
        '''
        Cette méthode vérifie si la souris est située dans les limites de la liste déroulante.

        Args:
            event: L'événement Pygame contenant des informations sur les coordonnées de la souris.
        '''
        # Ajout de l'offset 960 (largeur de la fenetre de graphe)
        # TODO: Modifier par une variable globale de largeur de la fenêtre
        mouse_pos = (event.pos[0] - 960, event.pos[1])
        if self.scrolling_list_view.scrolling_list_rect:
            return self.scrolling_list_view.scrolling_list_rect.collidepoint(mouse_pos)
        return False

    def handle_event(self, event) -> None:
        # Si un clic est réalisé
        if event.type == pygame.MOUSEBUTTONDOWN:
            # On vérifie si ce dernier est sur la zone de texte
            if self.is_scrolling_list_hovered(event):
                self.scrolling_list.active = True
                # On indique à la vue que la zone de texte a été cliquée
                self.scrolling_list_view.set_clicked()
            else:
                self.scrolling_list.active = False
                # On indique à la vue que la zone de texte n'est plus active
                self.scrolling_list_view.set_normal()

        if event.type == pygame.MOUSEMOTION:
            if self.scrolling_list.active == False:
                if self.is_scrolling_list_hovered(event):
                    # On indique à la vue que la zone de texte est survolée
                    self.scrolling_list_view.set_hovered()
                else:
                    # On indique à la vue que la zone de texte n'est pas survolée
                    # (réinitialisation en normal)
                    self.scrolling_list_view.set_normal()