from constants.Config import GRAPH_WINDOW_WIDTH

from views.ScrollingListView import ScrollingListView

from models.ScrollingList import ScrollingList

from models.algorithms.Algorithm import Algorithm
from models.algorithms.NaiveAlgorithm import NaiveAlgorithm
from models.algorithms.EvolutionalAlgorithm import EvolutionalAlgorithm
from models.algorithms.AntColonyAlgorithm import AntColonyAlgorithm

import pygame

class ScrollingListController:
    def __init__(self, parameters_view) -> None:
        self.parameters_view = parameters_view
        self.scrolling_list = ScrollingList(
            [NaiveAlgorithm(), EvolutionalAlgorithm(), AntColonyAlgorithm()]
        )
        self.scrolling_list_view = ScrollingListView(parameters_view.screen, 10, 110, 290, 40)

    def draw_scrolling_list(self):
        '''
        Cette méthode dessine la liste déroulante.
        '''
        algorithms = self.scrolling_list.get_algorithms()
        selected_algorithm = self.scrolling_list.get_selected_algorithm()

        self.scrolling_list_view.draw(algorithms, selected_algorithm, self.scrolling_list.has_an_algorithm_selected())

    def is_scrolling_list_header_hovered(self, event):
        '''
        Cette méthode vérifie si la souris est située dans les limites de la liste déroulante.

        Args:
            event: L'événement Pygame contenant des informations sur les coordonnées de la souris.
        '''
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        if self.scrolling_list_view.scrolling_list_rect:
            return self.scrolling_list_view.scrolling_list_rect.collidepoint(mouse_pos)
        return False

    def handle_event(self, event) -> bool:
        '''
        Cette méthode gère les interactions de l'utilisateur avec la souris, permettant de contrôler 
        le comportement de la liste déroulante (ouverture, sélection, etc.).
 
        Args:
            event: L'événement Pygame contenant des informations sur les coordonnées de la souris.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si l'élément est survolé, c'est que l'utilisateur a cliqué sur le header de la liste déroulante
            if self.is_scrolling_list_header_hovered(event):
                return self.handle_header_clicked(event)

            # Sinon, c'est qu'il essaie soit de cliquer sur les options de la liste déroulante, soit en dehors
            elif self.scrolling_list_view.is_active:
                return self.handle_scrolling_list_options(event)
        
        # Si l'utilisateur essaie de hover le header de la liste déroulante
        if event.type == pygame.MOUSEMOTION:
            return self.handle_header_hovered(event)
        return False

    def handle_header_clicked(self, event) -> bool:
        # Si la liste déroulante est déjà déroulée:
        if self.scrolling_list_view.is_active:
            # On la replie
            self.scrolling_list_view.set_active(False)
            return False
        # Sinon, on la déplie pour faire apparaitre les options d'algorithmes
        self.scrolling_list_view.set_active(True)
    
    def handle_header_hovered(self, event) -> bool:
        if not self.scrolling_list_view.is_active:
            if self.is_scrolling_list_header_hovered(event):
                self.scrolling_list_view.set_hovered()
            else:
                self.scrolling_list_view.set_normal()

    def handle_scrolling_list_options(self, event) -> bool:
        self.scrolling_list_view.set_active(False)
        # Récupération des options disponibles depuis le modèle et vérification que l'élément cliqué
        # est un algorithme disponible dans la liste
        selected_option = self.scrolling_list_view.is_option_clicked(event, self.scrolling_list.get_algorithms())
        # S'il s'agit d'une option d'algorithme qui a été sélectionnée:
        if selected_option:
            self.scrolling_list.set_selected_algorithm(selected_option)
            self.scrolling_list_view.set_active(False)
            return True
        
        # Sinon, c'est que l'utilisateur a cliqué en dehors de la liste d'options, on ferme la liste déroulante
        self.scrolling_list_view.set_active(False)
        return False

    def get_selected_algorithm(self) -> Algorithm:
        return self.scrolling_list.get_selected_algorithm()