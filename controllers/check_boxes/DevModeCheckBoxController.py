from constants.Colors import Colors
from controllers.GraphController import GraphController
from controllers.check_boxes.CheckBoxController import CheckBoxController
from views.CheckBoxView import CheckBoxView
from views.ParametersView import ParametersView

class DevModeCheckBoxController(CheckBoxController):
    """
    This class manages the developer checkbox, inheriting from
    CheckBoxController.

    Attributes:
        _graph_controller (GraphController): The controller managing the graph
            logic.
        _parameters_view (ParametersView): The view containing UI elements.
        _check_box (CheckBox): The model representing the checkbox state.
        _check_box_view (CheckBoxView): The view for rendering the checkbox.
    """
    def __init__(
        self,
        parameters_view: ParametersView,
        graph_controller: GraphController
    ) -> None:
        super().__init__(parameters_view, graph_controller)

    def create_view(self) -> CheckBoxView:
        """
        Creates the checkbox view.
        
        Returns:
            CheckBoxView: An instance of the checkbox view.
        """
        return CheckBoxView(
            self._parameters_view.screen,
            10,
            160,
            40,
            40,
            Colors.BUTTON_GREEN,
            "Developer mode"
        )

    def on_state_change(self) -> None:
        """
        Called when the state of the checkbox changes.
        """
        if self._check_box.enabled:
            self._graph_controller.raise_info("Developer mode enabled")
        else:
            self._graph_controller.raise_info("Developer mode disabled")
        
        self._graph_controller.enable_dev_mode(self._check_box.enabled)