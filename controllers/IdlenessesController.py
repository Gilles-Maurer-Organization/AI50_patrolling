from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.Node import Node
from models.IdlenessData import IdlenessData
from views.SimulationDataView import SimulationDataView
from views.IdlenessView import IdlenessView

class IdlenessController:
    """
    initialiser IdlenessData avec la liste des nodes du Graph


    Faire une fct "update" qui:
        - appelle IdlenessView.update_idleness()
        - get la max
        - get la moyenne
        - l'envoie à la vue ? 

    """
    def __init__(self, nodes_list : list[Node], simulation_data_view: SimulationDataView)-> None:
        self._simulation_data_view = simulation_data_view
        self._idleness = IdlenessData(nodes_list)
        self._idleness_view = IdlenessView(
                self._simulation_data_view.screen,
                10,
                10,
                100,
                40,
                label_text = "Idleness"
            )
    
    def draw_idlenesses(self):
        self._idleness_view.draw_text()
   

