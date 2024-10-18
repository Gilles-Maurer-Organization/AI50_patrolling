from views.ScrollingListView import ScrollingListView

from models.ScrollingList import ScrollingList

import pygame

class ScrollingListController:
    def __init__(self, parameters_view) -> None:
        self.parameters_view = parameters_view
        self.scrolling_list = ScrollingList('algorithm', ['naive algorithm', 'ant colony algorithm', 'evolutional algorithm'])
        self.scrolling_list_view = ScrollingListView(parameters_view.screen, 10, 110, 290, 40)

    def draw_scrolling_list(self) -> None:
        self.scrolling_list_view.draw(self.scrolling_list.algorithms)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_scrolling_list_hovered(event):
                self.scrolling_list_view.set_active(True)
            elif self.scrolling_list_view.is_active:
                selected_option = self.scrolling_list_view.is_option_clicked(event.pos)
                if selected_option:
                    self.scrolling_list_view.set_selected_option(selected_option)
                    print(f"Algorithme sélectionné : {selected_option}")
                else:
                    self.scrolling_list_view.set_active(False)

        if event.type == pygame.MOUSEMOTION:
            if self.scrolling_list_view.scrolling_list_rect.collidepoint(event.pos):
                self.scrolling_list_view.set_hovered()
            else:
                self.scrolling_list_view.set_normal()