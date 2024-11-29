import os
from pathlib import Path
import re

from services.ICSVService import ICSVService

class CSVService(ICSVService): 
    def __init__(self) -> None:
        self.csv_folder_path = os.path.join(Path(__file__).resolve().parent.parent, "csv_files")
        self.references_file_path = os.path.join(Path(__file__).resolve().parent.parent, "references", "references.csv")

    def initialize_directories(self):
        # create csv directories if they do not exist
        if not os.path.exists(self.csv_folder_path):
            os.makedirs(self.csv_folder_path)
        if not os.path.exists(os.path.dirname(self.references_file_path)):
            os.makedirs(os.path.dirname(self.references_file_path))
        if not os.path.exists(self.references_file_path):
            open(self.references_file_path, "w").close()

    def count_files(self) -> int:
        # count the number of csv files in the directory
        if not os.path.exists(self.csv_folder_path):
            return 0
        return len(os.listdir(self.csv_folder_path))

    def save(self, edges_matrix, nodes_list, image_name) -> None:
        # save graph information and reference to the csv file
        csv_path = self.find_csv_reference(image_name)
        if csv_path is None:
            new_csv_path = f'graph_{self.count_files() + 1}.csv'
            self.write_csv_information(edges_matrix, nodes_list, image_name, new_csv_path)
            self.save_csv_reference(new_csv_path, image_name)
        else:
            self.write_csv_information(edges_matrix, nodes_list, image_name, csv_path)

    def save_complements(self, complete_graph, shortest_paths, image_name):
        """
        Ajoute les données du complete_graph et des shortest_paths à la suite du fichier CSV correspondant à image_name.
        """
        # Trouver le chemin du fichier CSV associé à l'image
        csv_path = self.find_csv_reference(image_name)

        if csv_path is None:
            raise FileNotFoundError("No CSV file associated to this image")
        
        file_path = os.path.join(self.csv_folder_path, csv_path)
        
        complete_graph_lines = [
            ",".join(map(str, row)) + "\n" for row in complete_graph
        ]
        shortest_paths_lines = [
            ",".join(map(str, (start, end, path))) + "\n" for (start, end), path in shortest_paths.items()
        ]

        with open(file_path, mode='a', newline='') as f:
            f.write("Complete Graph,\n")
            f.writelines(complete_graph_lines)
            f.write("Shortest paths,\n")
            f.writelines(shortest_paths_lines)
    
    def are_complements_saved(self, image_name):
        csv_path = self.find_csv_reference(image_name)

        if csv_path is None:
            raise FileNotFoundError("No CSV file associated to this image")
        
        file_path = os.path.join(self.csv_folder_path, csv_path)

        try:
            with open(file_path, mode='r') as f:
                for line in f:
                    if "Complete Graph" in line:
                        return True
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file {csv_path} not found at {file_path}")
        
        return False
    
    def save_csv_reference(self, csv_path, image_name):
        # add csv file reference and image to the reference file
        with open(self.references_file_path, "a") as f:
            f.write(f'{image_name},{csv_path}\n')

    def find_csv_reference(self, image_name):
        # check if the reference file exists, if not, create it
        self.initialize_directories()

        # search for the csv reference by image name
        with open(self.references_file_path, "r") as f:
            for line in f:
                img_path, csv_path = line.strip().split(",")
                if img_path == image_name:
                    return csv_path
        return None

    def write_csv_information(self, edges_matrix, nodes_list, image_name, csv_path):
        # write nodes and edges matrix to a csv file
        file_path = os.path.join(self.csv_folder_path, csv_path)

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

    def _parse_csv_file(self, file_path: str) -> tuple[list[list[float]], list[tuple[int, int]]]:
        """
        Private utility to parse a CSV file and extract node information and the edge matrix.
        """
        if not os.path.exists(file_path):
            print("File does not exist")
            return None, None

        edges_matrix = []
        nodes_list = []
        
        complete_adjacency_matrix = []
        shortest_paths = {}

        with open(file_path, "r") as f:
            lines = f.readlines()

        nodes_line = lines[0]  # first line with nodes data
        matches = re.findall(r"\((\d+),\s*(\d+)\)", nodes_line)  # extract all (x, y) pairs
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
                edges_matrix.append([float(cell.strip()) if cell.strip() else 0.0 for cell in line.split(",")])
            
            elif section == "Complete Graph":
                complete_adjacency_matrix.append([float(cell.strip()) if cell.strip() else 0.0 for cell in line.split(",")])
            
            elif section == "Shortest paths":
                parts = line.split(",", maxsplit=2)
                if len(parts) == 3:
                    start = int(parts[0])
                    end = int(parts[1])
                    path_info = eval(parts[2])
                    path, cost = path_info
                    shortest_paths[(start, end)] = {"path": path, "cost": cost}

        return edges_matrix, nodes_list, complete_adjacency_matrix, shortest_paths

    def load_from_num_file(self, num_file: int) -> tuple[list[list[float]], list[tuple[int, int]]]:
        """
        Load graph data from a CSV file identified by its number.
        """
        file_path = os.path.join(self.csv_folder_path, f"graph_{num_file}.csv")
        return self._parse_csv_file(file_path)

    def load(self, file_path: str) -> tuple[list[list[float]], list[tuple[int, int]]]:
        """
        Load graph data from a specified CSV file path.
        """
        return self._parse_csv_file(file_path)

    def get_image_name(self, file_path: str) -> str:
        """
        Give the image associated with the csv file.
        """
        with open(file_path, "r") as f:
            for line in f:
                if "Image_ref" in line:
                    return line.split(",")[1]
        return None

