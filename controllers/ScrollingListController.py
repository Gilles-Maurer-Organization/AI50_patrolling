import pygame

from models.ScrollingList import ScrollingList
from models.algorithms.KMeans import KMeans
from models.algorithms.IAlgorithmModel import IAlgorithmModel
from models.algorithms.AntColony import AntColony
from models.algorithms.Evolutional import Evolutional
from models.algorithms.Naive import Naive
from models.algorithms.NaiveRuntime import NaiveRuntime
from views.ParametersView import ParametersView
from views.ScrollingListView import ScrollingListView
from services.algorithms.IAlgorithm import IAlgorithm

class ScrollingListController:
    """
    The ScrollingListController handles the logic and interaction of
    the scrolling list for selecting algorithms in the ParametersView.

    Attributes:
        _scrolling_list (ScrollingList): The model containing the list
            of algorithms and their states.
        _scrolling_list_view (ScrollingListView): The view responsible
            for rendering the scrolling list.
    """
    def __init__(self, parameters_view: ParametersView) -> None:
        self._scrolling_list = ScrollingList(
            [Naive(), Evolutional(), AntColony(), KMeans(), NaiveRuntime()]
        )
        self._scrolling_list_view = ScrollingListView(
            parameters_view.screen,
            10,
            110,
            290,
            40
        )

    def draw_scrolling_list(self) -> None:
        """
        Draws the scrolling list with available algorithms.
        """
        algorithms = self._scrolling_list.algorithms
        selected_algorithm = self._scrolling_list.selected_algorithm

        self._scrolling_list_view.draw(
            algorithms,
            selected_algorithm,
            self._scrolling_list.has_an_algorithm_selected()
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Checks if the mouse is hovering over the scrolling list header.

        Args:
            event: The Pygame event containing information about mouse
                position.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the header is hovered, it means the user clicked on the
            # scrolling list header
            if self._is_scrolling_list_header_hovered(event):
                return self._handle_header_clicked()

            # Otherwise, check if the user clicked on the scrolling list
            # options or outside of it
            elif self._scrolling_list_view.is_active:
                return self._handle_scrolling_list_options(event)
        
         # If the user is trying to hover over the scrolling list header
        if event.type == pygame.MOUSEMOTION:
            return self._handle_header_hovered(event)
        return False
    
    def _is_scrolling_list_header_hovered(
        self,
        event: pygame.event.Event
    ) -> None:
        """
        This method checks if the mouse is within the bounds of the
        scrolling list.

        Args:
            event: The Pygame event containing information about the
                mouse's coordinates.
        """
        return self._scrolling_list_view.is_hovered(event)

    def _handle_header_clicked(self) -> bool:
        """
        Toggles the scrolling list between active (expanded) and
        inactive (collapsed) states.
        """
        # if the scrolling list is already expanded:
        if self._scrolling_list_view.is_active:
            # Collapse it
            self._scrolling_list_view.set_active(False)
            return False
        # Otherwise, expand the scrolling list to show algorithm options
        self._scrolling_list_view.set_active(True)
    
    def _handle_header_hovered(self, event: pygame.event.Event) -> bool:
        """
        Changes the appearance of the scrolling list header when
        hovered by the mouse.

        Args:
            event: The Pygame event containing information about mouse
                position.
        """
        if not self._scrolling_list_view.is_active:
            if self._is_scrolling_list_header_hovered(event):
                self._scrolling_list_view.set_hovered()
            else:
                self._scrolling_list_view.set_normal()

    def _handle_scrolling_list_options(
        self,
        event: pygame.event.Event
    ) -> bool:
        """
        Handles the selection of an algorithm from the scrolling list.

        Args:
            event: The Pygame event containing information about mouse
                actions.
        """
        self._scrolling_list_view.set_active(False)
        # Get available options from the model and check if a valid option was clicked
        selected_option = self._scrolling_list_view.is_option_clicked(event, self._scrolling_list.algorithms)
        # If a valid algorithm option was selected
        if selected_option:
            self._scrolling_list.selected_algorithm = selected_option
            self._scrolling_list_view.set_active(False)
            return True
        
        # Otherwise, close the scrolling list if the user clicked outside
        self._scrolling_list_view.set_active(False)
        return False

    def get_selected_algorithm(self) -> IAlgorithmModel:
        """
        Returns the currently selected algorithm from the scrolling
        list.
        """
        return self._scrolling_list.selected_algorithm