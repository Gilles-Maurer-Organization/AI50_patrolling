import pygame

from constants.Config import GRAPH_WINDOW_WIDTH
from models.TextBox import TextBox
from views.ParametersView import ParametersView
from views.text_boxes.TextBoxView import TextBoxView

class BaseTextBoxController:
    """
    This class is managing and handling multiple text boxes.
    
    This class handles user interactions with text boxes, including
    mouse events, keyboard input, and visual updates. It manages a
    collection of text boxes and their associated views, ensuring that
    user interactions are reflected in the model and the view.

    Attributes:
        _parameters_view: The parameters view associated with this
            controller.
        _text_boxes: A dictionary mapping TextBox models to their
            corresponding TextBoxView instances.
    """
    def __init__(self, parameters_view: ParametersView):
        self._parameters_view = parameters_view
        self._text_boxes : dict[TextBox, TextBoxView] = {}

    def add_text_box(
        self,
        model: TextBox,
        text_box_view: TextBoxView
    ) -> None:
        """
        Associates a TextBox model with its corresponding view
        (TextBoxView).
        """
        self._text_boxes[model] = text_box_view

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events for all registered text boxes.

        Handles mouse clicks, mouse hover, and keyboard inputs for
        active text boxes.
        """
        for model, view in self._text_boxes.items():
            # Handle mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event, model, view)

            # Handle mouse hover event
            if event.type == pygame.MOUSEMOTION and not model.active:
                self.handle_hover(event, view)

            # Handle keyboard input if the text box is active
            if event.type == pygame.KEYDOWN and model.active:
                self.handle_keyboard(event, model)

            # Update the view with the text content and state of the text box
            view.change_text(model.text_content)
            # Update if the text box is completed (to change text color)
            view.set_text_completed(self.is_text_box_text_completed(model))

    def handle_click(
        self,
        event: pygame.event.Event,
        model: TextBox,
        view: TextBoxView
    ) -> None:
        """
        Handles a click event on a text box.

        Activates the text box if clicked, otherwise deactivates it.
        """
        if self.is_text_box_hovered(event, view):
            model.active = True
            view.set_clicked()
        else:
            model.active = False
            view.set_normal()

    def handle_hover(self, event: pygame.event.Event, view: TextBoxView):
        """
        Handles mouse hover event on a text box.

        Changes the appearance of the text box based on whether it's
        hovered.
        """
        if self.is_text_box_hovered(event, view):
            view.set_hovered()
        else:
            view.set_normal()

    def handle_keyboard(self, event: pygame.event.Event, model: TextBox):
        """
        Handles keyboard input when the text box is active.

        Processes backspace and digit input, updates the text box model
        accordingly.
        """
        # If it is the first time the text box is being written to and
        # the pressed key is valid (a digit), reset the default text
        if model.first_input and event.unicode.isdigit():
            model.reset()

        # If the backspace key is pressed
        if event.key == pygame.K_BACKSPACE:
            model.handle_backspace()
        # If it's not the backspace key, it must be a digit key
        elif event.unicode.isdigit():
            model.add_character(event.unicode)

    def is_text_box_text_completed(self, model: TextBox) -> bool:
        """
        Checks if the text box content is different from its default
        text.

        Returns:
            bool: True if completed, False otherwise.
        """
        return model.default_text != model.text_content or not model.first_input

    def is_text_box_hovered(self, event, text_box_view) -> bool:
        """
        Checks if the mouse is hovered over the text box based on the
        mouse position.

        Returns:
            bool: True if the mouse is within the text box bounds,
                False otherwise.
        """
        mouse_pos = (event.pos[0] - GRAPH_WINDOW_WIDTH, event.pos[1])
        return text_box_view.is_hovered(mouse_pos)

    def draw_text_boxes(self):
        """
        Draws all the registered text boxes on the screen.
        """
        for text_box in self._text_boxes.values():
            text_box.draw()

    def is_everything_filled(self) -> bool:
        """
        Checks if all text boxes are filled (i.e., not using default
        text).

        Returns:
            bool: True if all text boxes are filled, False otherwise.
        """
        for model, _ in self._text_boxes.items():
            if not model.filled:
                return False
        return True
