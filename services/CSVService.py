import csv
import os
import ast
import time
from pathlib import Path
import re
from threading import Timer
from typing import Union

from models.GraphData import GraphData
from models.GraphDataComplements import GraphDataComplements
from services.ICSVService import ICSVService


class CSVService(ICSVService):
    """
    Service for managing CSV operations, including saving and loading 
    graph data, managing references, and initializing directories.

    Attributes:
        _csv_folder_path (str): Path to the directory where CSV files
            are stored.
        _references_file_path (str): Path to the file where image and
            CSV references are stored.
    """

    def __init__(self) -> None:
        self._csv_folder_path = os.path.join(
            Path(__file__).resolve().parent.parent,
            "csv_files"
        )
        self._references_file_path = os.path.join(
            Path(__file__).resolve().parent.parent,
            "references",
            "references.csv"
        )

    def _initialize_directories(self):
        """
        Creates directories and reference file if they do not exist.
        """
        if not os.path.exists(self._csv_folder_path):
            os.makedirs(self._csv_folder_path)
        if not os.path.exists(os.path.dirname(self._references_file_path)):
            os.makedirs(os.path.dirname(self._references_file_path))
        if not os.path.exists(self._references_file_path):
            open(self._references_file_path, "w").close()

    def _count_files(self) -> int:
        """
        Counts the number of CSV files in the CSV directory.

        Returns:
            int: The number of CSV files in the directory.
        """
        if not os.path.exists(self._csv_folder_path):
            return 0
        return len(os.listdir(self._csv_folder_path))

    def save(self, edges_matrix, nodes_list, image_name) -> None:
        """
        Saves graph data and reference of the image and data onto
        different CSV files.

        Args:
            edges_matrix (List[List[float]]): The adjacency matrix
                representing the graph.
            nodes_list (Dict[int, Tuple[int, int]]): The nodes in the
                graph, represented as a dictionary of node ids and
                their (x, y) coordinates.
            image_name (str): The name of the image associated with the
                graph.
        """
        csv_path = self.find_csv_reference(image_name)
        if csv_path is None:
            new_csv_path = f'graph_{self._count_files() + 1}.csv'
            self._write_csv_information(
                edges_matrix,
                nodes_list,
                image_name,
                new_csv_path
            )
            self._save_csv_reference(
                new_csv_path,
                image_name
            )
        else:
            self._write_csv_information(
                edges_matrix,
                nodes_list, 
                image_name,
                csv_path
            )

    def save_complements(
        self,
        graph_data_complements: GraphDataComplements,
        image_name: str
    ) -> None:
        """
        Appends complete graph and shortest paths to the relevant CSV
        file.

        Args:
            graph_data_complements (GraphDataComplements): The
                complements of the Graph such as the complete
                adjacency matrix and the shortest paths
            image_name (str): The name of the image associated with the
                graph.
        """
        csv_path = self.find_csv_reference(image_name)

        if csv_path is None:
            raise FileNotFoundError("No CSV file associated to this image")
        
        file_path = os.path.join(self._csv_folder_path, csv_path)
        
        complete_graph_lines = [
            ",".join(map(str, row)) + "\n"
            for row in graph_data_complements.complete_adjacency_matrix
        ]
        shortest_paths_lines = [
            ",".join(map(str, (start, end, path))) +"\n"
            for (start, end), path in graph_data_complements.shortest_paths.items()
        ]

        with open(file_path, mode='a', newline='') as f:
            f.write("Complete Graph,\n")
            f.writelines(complete_graph_lines)
            f.write("Shortest paths,\n")
            f.writelines(shortest_paths_lines)
    
    def are_complements_saved(self, image_name: str) -> bool:
        """
        Checks if complete graph and shortest paths are saved for an
        image.

        Args:
            image_name (str): The name of the image to check for
                associated data.
        
        Returns:
            bool: True if complements are saved, False otherwise.
        """
        csv_path = self.find_csv_reference(image_name)

        if csv_path is None:
            raise FileNotFoundError("No CSV file associated to this image")
        
        file_path = os.path.join(self._csv_folder_path, csv_path)

        try:
            with open(file_path, mode='r') as f:
                for line in f:
                    if "Complete Graph" in line:
                        return True
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file {csv_path} not found at {file_path}")
        
        return False
    
    def _save_csv_reference(self, csv_path: str, image_name: str) -> None:
        """
        Saves a reference of a CSV file associated with an image.

        Args:
            csv_path (str): The path to the CSV file.
            image_name (str): The name of the image associated with the
                CSV file.
        """
        with open(self._references_file_path, "a") as f:
            f.write(f'{image_name},{csv_path}\n')

    def find_csv_reference(self, image_name: str) -> Union[None, str]:
        """
        Finds the CSV file associated with an image, if it exists.

        Args:
            image_name (str): The name of the image for which to find
                the associated CSV.
        
        Returns:
            Union[None, str]: The path to the CSV file if found, None
                otherwise.
        """
        # check if the reference file exists, if not, create it
        self._initialize_directories()

        # search for the csv reference by image name
        with open(self._references_file_path, "r") as f:
            for line in f:
                img_path, csv_path = line.strip().split(",")
                if img_path == image_name:
                    return csv_path
        return None

    def _write_csv_information(
        self,
        edges_matrix: list[list[float]],
        nodes_list: dict[int, tuple[int, int]],
        image_name: str,
        csv_path: str
    ) -> None:
        """
        Writes nodes and edges matrix data to a specified CSV file.

        Args:
            edges_matrix (List[List[float]]): The adjacency matrix
                representing distances between nodes in the graph.
            nodes_list (Dict[int, Tuple[int, int]]): The nodes in the
                graph.
            image_name (str): The name of the image associated with the
                graph.
            csv_path (str): The path to the CSV file where the data
                will be saved.
        """
        # write nodes and edges matrix to a csv file
        file_path = os.path.join(self._csv_folder_path, csv_path)

        with open(file_path, "w") as f:
            f.write("Nodes,")
            for node in nodes_list.values():
                f.write(f'{node},')
            f.write("\n")
            
            f.write("Simple Graph,\n")
            # write edges matrix
            for row in edges_matrix:
                f.write(",".join(str(cell) for cell in row) + "\n")
            f.write(f'Image_ref,{image_name}\n')

    def _parse_csv_file(
        self,
        file_path: str
    ) -> GraphData:
        """
        Parses a CSV file to extract nodes, adjacency matrix, and
        complement data such as complete adjacency matrix and shortest
        paths.

        Args:
            file_path (str): Path to the CSV file.
        
        Returns:
            GraphData: Containing:
                - List of adjacency matrix rows
                - List of node positions (x, y)
                - List of complete graph adjacency matrix
                - Dictionary of shortest paths between node pairs
        """
        if not os.path.exists(file_path):
            print("File does not exist")
            return None, None

        edges_matrix: list[list[float]] = []
        nodes_list: list[tuple[int, int]] = []
        complete_adjacency_matrix: list[list[float]] = []
        shortest_paths: dict[tuple[int, int], list[int]] = {}


        with open(file_path, "r") as f:
            lines = f.readlines()
        
        # first line with nodes data
        nodes_line = lines[0]
        # extract all (x, y) pairs
        matches = re.findall(r"\((\d+),\s*(\d+)\)", nodes_line) 
        nodes_list = [(int(x), int(y)) for x, y in matches]
        
        section = None
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            if "Simple Graph" in line:
                section = "Simple Graph"
                continue
            elif "Complete Graph" in line:
                section = "Complete Graph"
                continue
            elif "Shortest paths" in line:
                section = "Shortest paths"
                continue
            elif "Image_ref" in line:
                section = None
                continue
            
            if section == "Simple Graph":
                edges_matrix.append(
                    [
                        float(cell.strip()) if cell.strip() else 0.0
                        for cell in line.split(",")
                    ]
                )
            
            elif section == "Complete Graph":
                complete_adjacency_matrix.append(
                    [
                        float(cell.strip()) if cell.strip() else 0.0
                        for cell in line.split(",")
                    ]
                )
            
            elif section == "Shortest paths":
                parts = line.split(",", maxsplit=2)
                if len(parts) == 3:
                    start = int(parts[0])
                    end = int(parts[1])
                    path = ast.literal_eval(parts[2])
                    shortest_paths[(start, end)] = path

        return GraphData(
            shortest_paths = shortest_paths,
            nodes_list=nodes_list,
            adjacency_matrix=edges_matrix,
            complete_adjacency_matrix=complete_adjacency_matrix
        )
            

    def load_from_num_file(
        self,
        num_file: int
    ) -> GraphData:
        """
        Loads graph data from a CSV file identified by its number.

        Args:
            num_file (int): The number associated with the CSV file to
                load.
        
        Returns:
            GraphData: Containing:
                - List of adjacency matrix rows
                - List of node positions (x, y)
                - List of complete graph adjacency matrix
                - Dictionary of shortest paths between node pairs
        """
        file_path = os.path.join(
            self._csv_folder_path,
            f"graph_{num_file}.csv"
        )
        return self._parse_csv_file(file_path)

    def load(
        self,
        file_path: str
    ) -> GraphData:
        """
        Loads graph data from a specified CSV file path.

        Args:
            file_path (str): Path to the CSV file.

            
        Returns:
            GraphData: Containing:
                - List of adjacency matrix rows
                - List of node positions (x, y)
                - List of complete graph adjacency matrix
                - Dictionary of shortest paths between node pairs
        """
        return self._parse_csv_file(file_path)

    def get_image_name(self, file_path: str) -> str:
        """
        Gives the image associated with the csv file.

        Args:
            file_path (str): Path to the CSV file.
        
        Returns:
            Union[str, None]: Image name if found, None otherwise.
        """
        with open(file_path, "r") as f:
            for line in f:
                if "Image_ref" in line:
                    return line.split(",")[1]
        return None

def export_idleness_data(graph_number: int, idleness_data_provider, interval: int = 10):
    """
    Exports idleness data (average, max, all-time max) to a CSV file every `interval` seconds.

    Args:
        graph_number (int): The graph number used to name the file.
        idleness_data_provider (callable): A function that provides the idleness data as (average, max, all-time max).
        interval (int): The interval (in seconds) at which the data will be exported.
    """
    csv_filename = f'graph_{graph_number}_results.csv'
    csv_folder_path = os.path.join(Path(__file__).resolve().parent.parent, "csv_files")
    csv_path = os.path.join(csv_folder_path, csv_filename)

    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)

    with open(csv_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Average idleness", "Max idleness", "All-time max idleness"])

    def write_data():
        # retrieve idleness data
        average, max_idleness, all_time_max = idleness_data_provider()

        with open(csv_path, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, average, max_idleness, all_time_max])

        # schedule the next write
        Timer(interval, write_data).start()

    write_data()
