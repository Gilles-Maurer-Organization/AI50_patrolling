import pygame

from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.TextBox import TextBox
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
    
        padding_x = 10
        padding_y = 40
        
        text_box_width = 290 // 2 - padding_x // 2
        text_box_height = 40

        start_x = 10
        start_y = 190

        col_gap = text_box_width + padding_x
        row_gap = text_box_height + padding_y

        for i, (label, parameter) in enumerate(algorithm.parameters.items()):
            col = i % 2
            row = i // 2

            x = start_x + col * col_gap
            y = start_y + row * row_gap

            text_box_view = AlgorithmParametersView(
                self._parameters_view.screen,
                x,
                y,
                text_box_width,
                text_box_height,
                label_text=label
            )
            
            self.add_text_box(parameter, text_box_view)

    def handle_keyboard(self, event: pygame.event.Event, model: TextBox):
        """
        Handles keyboard input when the text box is active for
        algorithm parameters.

        This override allows handling of decimal points.
        """
        # If it is the first time the text box is being written to and
        # the pressed key is valid (a digit), reset the default text
        if model.first_input and event.unicode.isdigit():
            model.reset()

        # If the backspace key is pressed
        if event.key == pygame.K_BACKSPACE:
            model.handle_backspace()
        # Otherwise, handle digits and allow points
        elif event.unicode.isdigit() or event.unicode == '.':
            model.add_character(event.unicode)