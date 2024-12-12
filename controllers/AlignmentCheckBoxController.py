import pygame

from constants.Config import PARAMETERS_WINDOW_WIDTH
from controllers.GraphController import GraphController
from models.AlignmentCheckBox import AlignmentCheckBox
from views.AlignmentCheckBoxView import AlignmentCheckBoxView
from views.ParametersView import ParametersView

class AlignmentCheckBoxController:
    def __init__(
        self,
        parameters_view: ParametersView,
        graph_controller: GraphController
    ) -> None:
        self._graph_controller = graph_controller

        self._alignment_check_box = AlignmentCheckBox()
        self._alignment_check_box_view = AlignmentCheckBoxView(
            parameters_view.screen,
            PARAMETERS_WINDOW_WIDTH - 50,
            60,
            40,
            40
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events for the checkbox.

        Args:
            event (pygame.event.Event): The position of the mouse's click.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._alignment_check_box_view.is_clicked(event):
                self._alignment_check_box.toggle_alignment()
                self.draw_check_box()
                if self._alignment_check_box.alignment_enabled:
                    self._graph_controller.raise_info("Alignment enabled")
                elif not self._alignment_check_box.alignment_enabled:
                    self._graph_controller.raise_info("Alignment disabled")

                self._graph_controller.set_snapping_enabled(
                    self._alignment_check_box.alignment_enabled
                )

    def draw_check_box(self) -> None:
        """
        Draws the checkbox on the parameters' view.
        """
        self._alignment_check_box_view.draw(
            self._alignment_check_box.alignment_enabled
        )