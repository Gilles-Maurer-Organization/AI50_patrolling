from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.TextBox import TextBox
from views.text_boxes.TextBoxView import TextBoxView

class TextBoxController(BaseTextBoxController):
    """
    This class is managing interactions with a specific text box in the
    parameters view.
    
    This class is responsible for handling user interactions with a text
    box that asks for the number of agents. It extends the base
    functionality of the BaseTextBoxController and sets up a specific
    text box with its corresponding view.

    Attributes:
        _parameters_view: The parameters view associated with this
            controller.
        _text_boxes: A dictionary that maps TextBox models to their
            corresponding TextBoxView instances.
    """
    def __init__(self, parameters_view):
        super().__init__(parameters_view)

        self._text_box = TextBox(default_text="Number of Agents")
        text_box_view = TextBoxView(
            parameters_view.screen,
            10,
            60,
            190,
            40,
            icon_path='assets/widgets/number_agents.png'
        )
        self.add_text_box(self._text_box, text_box_view)

    @property
    def text_content(self) -> str:
        """
        Get the text content of the text box.

        Returns:
            str: The current text content of the text box.
        """
        return self._text_box.text_content