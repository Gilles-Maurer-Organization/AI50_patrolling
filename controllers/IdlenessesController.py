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
    def __init__(self, simulation_data_view: SimulationDataView)-> None:
        self._simulation_data_view = simulation_data_view
        self._idleness_data = IdlenessData()
        self._idleness_view = IdlenessView(
            self._simulation_data_view.screen
        )

    @property
    def idleness(self) -> IdlenessData:
        """Getter for the idleness attribute."""
        return self._idleness_data

    @idleness.setter
    def idleness(self, value: IdlenessData) -> None:
        """Setter for the idleness attribute with validation."""
        if not isinstance(value, IdlenessData):
            raise ValueError("idleness must be an instance of IdlenessData")
        self._idleness_data = value
    
    def draw_idlenesses(self, nodes_list : list[Node])-> None:
        """
        Draws the idleness values in the View.
        """
        self.idleness.update_idleness(nodes_list)

        # Get the updated idleness values
        idleness_data = self._idleness_data.get_idleness_data()

        # Update the view with the new values
        self._idleness_view.update_values(
            idleness_data[0],
            idleness_data[1],
            idleness_data[2]
        )
        # Update the idleness display
        self._idleness_view.draw_text()

    def reset_idleness_data(self) -> None:
        self._idleness_data.reset()