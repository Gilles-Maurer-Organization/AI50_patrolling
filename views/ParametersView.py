class ParametersView:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = (200, 200, 200)

    def draw_parameters(self) -> None:
        self.screen.fill(self.background_color)
