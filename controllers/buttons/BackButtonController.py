from constants.Colors import Colors
from constants.Config import PARAMETERS_WINDOW_HEIGHT, PARAMETERS_WINDOW_WIDTH
from controllers.IdlenessesController import IdlenessController
from controllers.SimulationController import SimulationController
from controllers.buttons.BaseButtonController import BaseButtonController
from models.Button import Button
from views.ButtonView import ButtonView
from views.SimulationDataView import SimulationDataView


class BackButtonController(BaseButtonController):
    """
    Controller for the "Back to configuration" button in the simulation
    view.

    This class handles the interaction logic for the "Back to configuration"
    button, which allows users to navigate back to the configuration screen
    from the simulation view.

    Attributes:
        _simulation_data_view (SimulationDataView): 
            The view where the simulation data is displayed.
        _simulation_controller (SimulationController): 
            The controller managing the simulation state.
        _idleness_controller (IdlenessController):
            The controller mananing the idlenesses.
        _back_button (Button): 
            The model for the "Back to configuration" button.
        _button_map (dict): 
            A mapping of button models to their corresponding views.
    """
    def __init__(
        self,
        simulation_data_view: SimulationDataView,
        simulation_controller: SimulationController,
        idleness_controller: IdlenessController
    ) -> None:
        super().__init__()
        self._simulation_data_view = simulation_data_view
        self._simulation_controller = simulation_controller
        self._idleness_controller = idleness_controller

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
        """
        Handles the action performed when the "Back to configuration" button is
        clicked.

        This method updates the simulation controller to indicate that the
        simulation is no longer running, allowing the user to return to the
        configuration screen.
        """
        self._simulation_controller.set_simulation_started(False)
        self._idleness_controller.reset_idleness_data()