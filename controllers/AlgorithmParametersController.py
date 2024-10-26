from controllers.BaseTextBoxController import BaseTextBoxController
from models.Algorithm import Algorithm
from views.TextBoxView import TextBoxView

class AlgorithmParametersController(BaseTextBoxController):
    def __init__(self, parameters_view):
        super().__init__(parameters_view)
        self.algorithm = None

    def handle_selected_algorithm(self, algorithm: Algorithm):
        '''
        Cette méthode met à jour les paramètres de l'algorithme sélectionné et initialise les zones de texte correspondantes.
        '''
        self.algorithm = algorithm
        self.text_boxes.clear()
        offset_y = 0
        for parameter in algorithm.parameters:
            text_box_view = TextBoxView(self.parameters_view.screen, 10, 160 + offset_y, 190, 40)
            self.add_text_box(parameter, text_box_view)
            offset_y += 50