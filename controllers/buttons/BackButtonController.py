from constants.Colors import Colors
from constants.Config import PARAMETERS_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH
from controllers.GraphController import GraphController
from controllers.SimulationController import SimulationController
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from views.ButtonView import ButtonView
from views.SimulationDataView import SimulationDataView


class BackButtonController(BaseButtonController):
    def __init__(
        self,
        simulation_data_view: SimulationDataView,
        simulation_controller: SimulationController
    ) -> None:
        super().__init__()
        self._simulation_data_view = simulation_data_view
        self._simulation_controller = simulation_controller

        self._back_button = Button(
            "Back to configuration",
            self.back_action,
            enabled=True
        )

        self._button_map = {
            self._back_button: ButtonView(
                self._simulation_data_view.screen,
                self._back_button.text,
                PARAMETERS_WINDOW_WIDTH - 180 - 10,
                PARAMETERS_WINDOW_HEIGHT - 40 - 10,
                180,
                40,
                color=Colors.ORANGE,
                hover_color=Colors.DARK_ORANGE
            )
        }

    def back_action(self) -> None:
        self._simulation_controller.set_simulation_started(False)