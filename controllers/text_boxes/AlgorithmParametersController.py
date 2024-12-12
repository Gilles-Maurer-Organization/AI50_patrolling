from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.algorithms.IAlgorithmModel import IAlgorithmModel
from views.ParametersView import ParametersView
from views.text_boxes.AlgorithmParametersView import AlgorithmParametersView

class AlgorithmParametersController(BaseTextBoxController):
    """
    This class is managing interactions with text boxes that hold
    algorithm parameters in the parameters view.

    This class extends the BaseTextBoxController and is responsible for
    handling the algorithm selection and updating the text boxes
    associated with the parameters of the selected algorithm.

    Attributes:
        _parameters_view: The parameters view associated with this
            controller.
        _text_boxes: A dictionary that maps TextBox models to their
            corresponding TextBoxView instances.
    """
    def __init__(self, parameters_view: ParametersView):
        super().__init__(parameters_view)

    def handle_selected_algorithm(self, algorithm: IAlgorithmModel):
        """
        Updates the parameters view with text boxes for the selected
        algorithm's parameters.

        This method clears the existing text boxes, iterates over the
        parameters of the selected algorithm, and creates new text
        boxes for each parameter, associating them with their
        corresponding views.

        Args:
            algorithm (AlgorithmModel): The selected algorithm whose
                parameters need to be displayed and edited.
        """
        self._text_boxes.clear()
        offset_y = 0
        for label, parameter in algorithm.parameters.items():
            text_box_view = AlgorithmParametersView(
                self._parameters_view.screen,
                10,
                290 + offset_y,
                190,
                40,
                label_text = label
            )
            
            self.add_text_box(parameter, text_box_view)
            offset_y += 77