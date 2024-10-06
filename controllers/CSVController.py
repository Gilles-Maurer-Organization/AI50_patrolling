import os
from pathlib import Path

class CSVController: 

    folder_path = os.path.join(Path(__file__).resolve().parent.parent, "csv_files")

    def __init__(self):
        pass

    def count_files(self):
        return len(os.listdir(self.folder_path))

    def save(self, edges_matrix, nodes_list):
        
        file_path = os.path.join(self.folder_path, f"graph_{self.count_files() + 1}.csv")
        
        with open(file_path, "w") as f:
            f.write("Nodes,")
            for node in nodes_list:
                f.write(str(node) + ",")
            f.write("\n")

            for i, row in enumerate(edges_matrix):
                for cell in row:
                    f.write(str(cell) + ",")
                f.write("\n")

    def load(self, num_file):
        
        file_path = os.path.join(self.folder_path, f"graph_{num_file}.csv")

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

        print(edges_matrix)
        print(nodes_list)

        return edges_matrix, nodes_list