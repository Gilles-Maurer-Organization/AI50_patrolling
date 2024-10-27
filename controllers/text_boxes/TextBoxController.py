from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.TextBox import TextBox
from views.TextBoxView import TextBoxView

class TextBoxController(BaseTextBoxController):
    def __init__(self, parameters_view):
        super().__init__(parameters_view)
        
        text_box = TextBox(default_text="Number of Agents")
        text_box_view = TextBoxView(parameters_view.screen, 10, 60, 190, 40, icon_path='assets/number_agents.png')
        self.add_text_box(text_box, text_box_view)