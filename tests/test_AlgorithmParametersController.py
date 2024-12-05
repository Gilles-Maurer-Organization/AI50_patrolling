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
        self.assertEqual(algorithm.parameters["Alpha"]._text_content, "0.1")
        self.assertEqual(algorithm.parameters["Beta"]._text_content, "0.6")
        self.assertEqual(algorithm.parameters["Rho"]._text_content, "0.5")
        self.assertEqual(algorithm.parameters["Tau"]._text_content, "0.2")

    def test_custom_parameters(self):
        algorithm = AntColony(alpha=0.5, beta=0.7)
        
        # We check if the parameters passed in the constructor are indeed
        # modified in the instantiation of the text boxes
        self.assertEqual(algorithm.parameters["Alpha"]._text_content, "0.5")
        self.assertEqual(algorithm.parameters["Beta"]._text_content, "0.7")

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
        # We check if the number of text boxes is equal to 4 (for the ant colony algorithm)
        self.assertEqual(len(controller._text_boxes), 4)

        # We verify that the self.text_boxes.clear() method was called:
        controller.handle_selected_algorithm(algorithm)
        # In fact, if we call the handle_selected_algorithm() method again, the number of
        # text boxes must stay the same as before, and not duplicating
        self.assertEqual(len(controller._text_boxes), 4)
        
        # We verify that the AntColony class been instantiated with the good parameters
        expected_calls = [
            unittest.mock.call(
                mock_parameters_view.screen,
                10,
                190,
                190,
                40,
                label_text="Alpha"
            ),
            unittest.mock.call(
                mock_parameters_view.screen,
                10,
                267,
                190,
                40,
                label_text="Beta"
            ),
            unittest.mock.call(
                mock_parameters_view.screen,
                10,
                344,
                190,
                40,
                label_text="Rho"
            ),
            unittest.mock.call(
                mock_parameters_view.screen,
                10,
                421,
                190,
                40,
                label_text="Tau"
            )
        ]

        # We assert that the parameters instantiated are the same as expected
        mockAlgorithmParametersView.assert_has_calls(expected_calls, any_order=False)