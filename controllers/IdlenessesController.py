from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.Node import Node
from models.IdlenessData import IdlenessData
from views.SimulationDataView import SimulationDataView
from views.IdlenessView import IdlenessView

class IdlenessController:
    """
    This class manages everything related to the Idleness of the simulation.

    Attributes:
        _simulation_data_view: the Simulation section of the View
        _idleness: the Idleness Model
        _idleness_view : the Idleness-data visualization


    """
    def __init__(self, nodes_list : list[Node], simulation_data_view: SimulationDataView)-> None:
        self._simulation_data_view = simulation_data_view
        print("nb nodes" ,len(nodes_list))
        self._idleness = IdlenessData(nodes_list)
        self._idleness_view = IdlenessView(
                self._simulation_data_view.screen,
                10,
                10,
                100,
                40,
                label_average_idleness_value = 0,
                label_max_idleness_value = 0,
                label_ath_idleness_value = 0
            )
    
    def draw_idlenesses(self):

        self._idleness.update_idleness()

        # Get the updated idleness values
        idleness_data = self._idleness.get_idleness_data()

        # Update the view with the new values
        self._idleness_view.update_values(idleness_data[0], idleness_data[1], idleness_data[2])
        #update l'idleness
        self._idleness_view.draw_text()
   

