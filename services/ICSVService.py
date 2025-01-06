from abc import ABC, abstractmethod
from typing import Union

from models.GraphData import GraphData
from models.GraphDataComplements import GraphDataComplements

class ICSVService(ABC):
    @abstractmethod
    def save(self, edges_matrix, nodes_list, filename):
        pass
    
    @abstractmethod
    def save_complements(
        self,
        graph_data_complements: GraphDataComplements,
        image_name: str
    ) -> None:
        pass

    @abstractmethod
    def are_complements_saved(self, image_name: str) -> bool:
        pass

    @abstractmethod
    def load_from_num_file(
        self,
        num_file: int
    ) -> GraphData:
        pass

    @abstractmethod
    def load(
        self,
        file_path: str
    ) -> GraphData:
        pass

    @abstractmethod
    def find_csv_reference(self, image_name: str) -> Union[None, str]:
        pass

    @abstractmethod
    def get_image_name(self, file_path: str) -> str:
        pass

    @property
    @abstractmethod
    def current_csv_number(self) -> int:
        """
        Abstract property for the current CSV number.
        """
        pass

    @current_csv_number.setter
    @abstractmethod
    def current_csv_number(self, value: int) -> None:
        pass

    @abstractmethod
    def get_next_test_number(self, algorithm: str, graph_number: int) -> int:
        pass

    @abstractmethod
    def export_idleness_data(
        self,
        idleness_data_provider,
        simulation_running_provider,
        algorithm: str,
        test_number: int,
        start_time: int,
        interval: int = 10
    ):
        pass