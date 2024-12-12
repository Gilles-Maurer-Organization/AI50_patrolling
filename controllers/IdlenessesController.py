from controllers.text_boxes.BaseTextBoxController import BaseTextBoxController
from models.Node import Node
from models.IdlenessData import IdlenessData
from views.SimulationDataView import SimulationDataView
from views.IdlenessView import IdlenessView

class IdlenessController(BaseTextBoxController):
        

    """
    initialiser IdlenessData avec la liste des nodes du Graph


    Faire une fct "update" qui:
        - appelle IdlenessView.update_idleness()
        - get la max
        - get la moyenne
        - l'envoie à la vue ? 

    """
    def __init__(self, nodes_list : list[Node], simulation_view: SimulationDataView)-> None:
        super().__init__(simulation_view)
        self.idleness = IdlenessData(nodes_list)
    

    #def handle_idleness(self):
        
        #update idleness values
    #    self.idleness.update_idleness()

    def draw_idlenesses(self):

        self._text_boxes.clear()
        offset_y = 0
        for label, value in self.idleness.get_idleness_data().items():

            text_box_view = IdlenessView(
                self._parameters_view._screen,
                10,
                100,
                190,
                40,
                label_text = label,
                label_value = value
            )
            self.add_text_box(value, text_box_view)
            offset_y += 77
            
        pass
   

