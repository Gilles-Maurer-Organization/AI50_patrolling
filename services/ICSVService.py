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