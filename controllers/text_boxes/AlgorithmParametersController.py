from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.algorithms.Algorithm import Algorithm
from views.text_boxes.AlgorithmParametersView import AlgorithmParametersView

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
        for label, parameter in algorithm.parameters.items():
            text_box_view = AlgorithmParametersView(
                self.parameters_view.screen,
                10,
                190 + offset_y,
                190,
                40,
                label_text = label
            )
            self.add_text_box(parameter, text_box_view)
            offset_y += 77