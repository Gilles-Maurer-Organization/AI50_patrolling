import unittest
import pygame

from unittest.mock import MagicMock, patch
from controllers.text_boxes.AlgorithmParametersController import AlgorithmParametersController
from models.algorithms.AntColony import AntColony

class TestAlgorithmParametersController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We initialize pygame once for all the tests
        pygame.init()

    def test_default_parameters(self):
        algorithm = AntColony()
        
        # We check if the value of the parameters are indeed
        # the one by default with the empty constructor 
        self.assertEqual(algorithm.parameters["Alpha"]._text_content, "1")
        self.assertEqual(algorithm.parameters["Beta"]._text_content, "4")
        self.assertEqual(algorithm.parameters["Evaporation rate"]._text_content, "0.1")
        self.assertEqual(algorithm.parameters["Pheromone quantity"]._text_content, "100")
        self.assertEqual(algorithm.parameters["Nb colony"]._text_content, "5")
        self.assertEqual(algorithm.parameters["Nb iterations"]._text_content, "100")


    def test_custom_parameters(self):
        algorithm = AntColony(alpha=0.5, beta=0.7, evaporation=0.3, q=15, nb_colony=5, nb_iterations=200)
        
        # We check if the parameters passed in the constructor are indeed
        # modified in the instantiation of the text boxes
        self.assertEqual(algorithm._parameters["Alpha"]._text_content, "0.5")
        self.assertEqual(algorithm._parameters["Beta"]._text_content, "0.7")
        self.assertEqual(algorithm._parameters["Evaporation rate"]._text_content, "0.3")
        self.assertEqual(algorithm._parameters["Pheromone quantity"]._text_content, "15")
        self.assertEqual(algorithm._parameters["Nb colony"]._text_content, "5")
        self.assertEqual(algorithm._parameters["Nb iterations"]._text_content, "200")

    @patch('controllers.text_boxes.AlgorithmParametersController.AlgorithmParametersView')
    def test_handle_selected_algorithm(self, mockAlgorithmParametersView):
        # We initialize a mocked view
        mock_parameters_view = MagicMock()
        
        # We create our controller thanks to the mocked view
        controller = AlgorithmParametersController(parameters_view=mock_parameters_view)
        
        # We create an instantiation of the ant colony algorithm class
        algorithm = AntColony()
        
        # We call the method that we want to test
        controller.handle_selected_algorithm(algorithm)
        # We check if the number of text boxes is equal to 6 (for the ant colony algorithm)
        self.assertEqual(len(controller._text_boxes), 6)

        # We verify that the self.text_boxes.clear() method was called:
        controller.handle_selected_algorithm(algorithm)
        # In fact, if we call the handle_selected_algorithm() method again, the number of
        # text boxes must stay the same as before, and not duplicating
        self.assertEqual(len(controller._text_boxes), 6)
        
        # We verify that the AntColony class has been instantiated with the correct parameters
        expected_calls = [
            unittest.mock.call(
            mock_parameters_view.screen,
            10,
            190,
            140,
            40,
            label_text="Alpha"
            ),
            unittest.mock.call(
            mock_parameters_view.screen,
            160,
            190,
            140,
            40,
            label_text="Beta"
            ),
            unittest.mock.call(
            mock_parameters_view.screen,
            10,
            270,
            140,
            40,
            label_text="Evaporation rate"
            ),
            unittest.mock.call(
            mock_parameters_view.screen,
            160,
            270,
            140,
            40,
            label_text="Pheromone quantity"
            ),
            unittest.mock.call(
            mock_parameters_view.screen,
            10,
            350,
            140,
            40,
            label_text="Nb colony"
            ),
            unittest.mock.call(
            mock_parameters_view.screen,
            160,
            350,
            140,
            40,
            label_text="Nb iterations"
            )
        ]

        # We assert that the parameters instantiated are the same as expected
        mockAlgorithmParametersView.assert_has_calls(expected_calls, any_order=False)