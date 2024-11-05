import os
from pathlib import Path
import re

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

    def save(self, edges_matrix, nodes_list, image_name) -> None:
        self.initialize_directories()
        csv_path = self.find_csv_reference(image_name)
        if csv_path is None:
            new_csv_path = f'graph_{self.count_files() + 1}.csv'
            self.write_csv_information(edges_matrix, nodes_list, image_name, new_csv_path)
            self.save_csv_reference(new_csv_path, image_name)
        else:
            self.write_csv_information(edges_matrix, nodes_list, image_name, csv_path)

    def save_csv_reference(self, csv_path, image_name):
        with open(self.references_file_path, "a") as f:
            f.write(f'{image_name},{csv_path}\n')

    def find_csv_reference(self, image_name):
        with open(self.references_file_path, "r") as f:
            for line in f:
                img_path, csv_path = line.strip().split(",")
                if img_path == image_name:
                    return csv_path
        return None

    def write_csv_information(self, edges_matrix, nodes_list, image_name, csv_path):
        file_path = os.path.join(self.csv_folder_path, csv_path)

        with open(file_path, "w") as f:
            f.write("Nodes,")
            for node in nodes_list:
                f.write(f'{node},')
            f.write("\n")

            for row in edges_matrix:
                f.write(",".join(str(cell) for cell in row) + "\n")
            f.write(f'Image_ref,{image_name}')

    def load(self, num_file) -> tuple[list[list[float]], list[tuple[int, int]]]:
        file_path = os.path.join(self.csv_folder_path, f"graph_{num_file}.csv")

        if not os.path.exists(file_path):
            print("File does not exist")
            return None, None

        edges_matrix = []
        nodes_list = []

        with open(file_path, "r") as f:
            lines = f.readlines()

            # Extraction des noeuds en tant que tuples (x, y)
            nodes_line = lines[0]  # Première ligne complète
            matches = re.findall(r"\((\d+),\s*(\d+)\)", nodes_line)  # Extraire toutes les paires (x, y)
            for match in matches:
                x, y = map(int, match)
                nodes_list.append((x, y))

            # Extraction de la matrice des arêtes
            for line in lines[1:]:
                if "Image_ref" in line:  # Ignorer la ligne avec l'image de référence
                    continue
                row = line.split(",")[1:]  # Ignore la première colonne
                cleaned_row = [float(cell.strip()) if cell.strip() else 0.0 for cell in row]
                edges_matrix.append(cleaned_row)

        return edges_matrix, nodes_list