from constants.Config import PARAMETERS_WINDOW_WIDTH
from models.AlignmentCheckBox import AlignmentCheckBox
from views.AlignmentCheckBoxView import AlignmentCheckBoxView
from views.ParametersView import ParametersView


class AlignmentCheckBoxController:
    def __init__(self, parameters_view: ParametersView) -> None:
        self._alignment_check_box = AlignmentCheckBox()
        self._alignment_check_box_view = AlignmentCheckBoxView(
            parameters_view.screen,
            PARAMETERS_WINDOW_WIDTH - 60,
            140,
            50,
            40
        )

    def draw_check_box(self) -> None:
        self._alignment_check_box_view.draw()