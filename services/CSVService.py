import os
from pathlib import Path

from services.ICSVService import ICSVService

class CSVService(ICSVService): 
    def __init__(self) -> None:
        self.csv_folder_path = os.path.join(Path(__file__).resolve().parent.parent, "csv_files")
        self.references_file_path = os.path.join(Path(__file__).resolve().parent.parent, "references", "references.csv")

    def initialize_directories(self):
        if not os.path.exists(self.csv_folder_path):
            os.makedirs(self.csv_folder_path)
        if not os.path.exists(os.path.dirname(self.references_file_path)):
            os.makedirs(os.path.dirname(self.references_file_path))
        if not os.path.exists(self.references_file_path):
            open(self.references_file_path, "w").close()

    def count_files(self) -> int:
        if not os.path.exists(self.csv_folder_path):
            return 0
        return len(os.listdir(self.csv_folder_path))

    def save(self, edges_matrix, nodes_list, image_path) -> None:
        self.initialize_directories()
        csv_path = self.find_csv_reference(image_path)
        if csv_path is None:
            new_csv_path = f'graph_{self.count_files() + 1}.csv'
            self.write_csv_information(edges_matrix, nodes_list, image_path, new_csv_path)
            self.save_csv_reference(new_csv_path, image_path)
        else:
            self.write_csv_information(edges_matrix, nodes_list, image_path, csv_path)

    def save_csv_reference(self, csv_path, image_path):
        with open(self.references_file_path, "w") as f:
            f.write(f'{image_path},{csv_path}')

    def find_csv_reference(self, image_path):
        with open(self.references_file_path, "r") as f:
            for line in f:
                img_path, csv_path = line.strip().split(",")
                if img_path == image_path:
                    return csv_path
        return None

    def write_csv_information(self, edges_matrix, nodes_list, image_path, csv_path):
        file_path = os.path.join(self.csv_folder_path, csv_path)

        with open(file_path, "w") as f:
            f.write("Nodes,")
            for node in nodes_list:
                f.write(f'{node},')
            f.write("\n")

            for row in edges_matrix:
                f.write(",".join(str(cell) for cell in row) + "\n")
            f.write(f'Image_ref,{image_path}')

    
    # TODO : Fix la fonction (charge des coordonnées en string avec des () en trop)
    def load(self, num_file) -> tuple[list, list[str]]:
        
        file_path = os.path.join(self.csv_folder_path, f"graph_{num_file}.csv")

        if (not os.path.exists(file_path)):
            print("File does not exist")
            return None, None

        edges_matrix = []
        nodes_list = []

        with open(file_path, "r") as f:
            lines = f.readlines()

            nodes_list = lines[0].split(",")[1:-1]

            for line in lines[1:]:
                row = line.split(",")[1:-1]
                edges_matrix.append([float(cell) for cell in row])

        return edges_matrix, nodes_list