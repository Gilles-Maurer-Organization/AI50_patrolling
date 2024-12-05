from abc import ABC, abstractmethod
from typing import Union

class ICSVService(ABC):
    @abstractmethod
    def save(self, edges_matrix, nodes_list, filename):
        pass
    
    @abstractmethod
    def save_complements(
        self,
        complete_graph: list[list[float]],
        shortest_paths: dict[tuple[int, int], list[int]],
        image_name: str
    ) -> None:
        pass

    @abstractmethod
    def are_complements_saved(self, image_name: str) -> bool:
        pass

    def load_from_num_file(
        self,
        num_file: int
    ) -> tuple[
        list[list[float]],
        list[tuple[int, int]],
        list[list[float]],
        dict[tuple[int, int], list[int]]
    ]:
        pass

    @abstractmethod
    def load(
        self,
        file_path: str
    ) -> tuple[
        list[list[float]],
        list[tuple[int, int]],
        list[list[float]],
        dict[tuple[int, int], list[int]]
    ]:
        pass

    @abstractmethod
    def find_csv_reference(self, image_name: str) -> Union[None, str]:
        pass

    @abstractmethod
    def save_complements(
        self,
        complete_graph: list[list[float]],
        shortest_paths: dict[tuple[int, int], list[int]],
        image_name: str
    ) -> None:
        pass

    @abstractmethod
    def get_image_name(self, file_path: str) -> str:
        pass