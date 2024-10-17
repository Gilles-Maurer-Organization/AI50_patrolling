from models.Button import Button
from views.ButtonView import ButtonView

class ParametersController:
    def __init__(self, screen):
        self.screen = screen

        button_save_model = Button("save", self.save_action)
        button_import_model = Button("import", self.import_action)
        button_clear_model = Button("clear", self.clear_action)

        button_save_view = ButtonView(self.screen, "save", 10, 10, 110, 40)
        button_import_view = ButtonView(self.screen, "import", 130, 10, 120, 40)
        button_clear_view = ButtonView(self.screen, "clear", 260, 10, 120, 40)

        self.button_controllers = [
            ButtonController(button_save_model, button_save_view),
            ButtonController(button_import_model, button_import_view),
            ButtonController(button_clear_model, button_clear_view)
        ]

    def handle_events(self, event):
        self.parameters_view.handle_events(event)

    def save_action(self):
        print("Save action triggered")

    def import_action(self):
        print("Import action triggered")

    def clear_action(self):
        print("Clear action triggered")

    def draw(self):
        self.parameters_view.draw_parameters()