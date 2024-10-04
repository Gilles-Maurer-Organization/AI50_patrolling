
import tkinter as tk
from PIL import Image, ImageTk
import os
from pathlib import Path
import math

class GraphCreation:

    image = None
    image_size = None
    root = None
    canvas = None
    node_size = 7
    nodes_coordinates_dict = {}

    edge_list = {}

    selected_node = None

    def __init__(self, width, height):
        self.image_size = (width, height)

    def load_image(self, image_path):
        self.image = Image.open(image_path)
        self.image = self.image.resize(self.image_size)

    def display_image(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.image_size[0], height=self.image_size[1])
        self.canvas.pack()
        photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        self.root.mainloop()


    def left_click(self, event):
        x, y = event.x, event.y
        r = self.node_size

        for node, coordinates in self.nodes_coordinates_dict.items():
            if coordinates[0] - r < x < coordinates[0] + r and coordinates[1] - r < y < coordinates[1] + r:

                lines_to_remove = []

                for line, nodes in self.edge_list.items():
                    node1, node2 = nodes
                    if node == node1 or node == node2:
                        lines_to_remove.append(line)

                for line in lines_to_remove:
                    self.remove_edge(line)


                print("Node already exists at these coordinates")
                self.remove_node(node)
                return
            
        self.add_node(x, y)

        print(f"Node added at coordinates: ({x}, {y})")
        print("dict: ", self.nodes_coordinates_dict)


    def add_node(self, x, y):
        r = self.node_size
        new_node = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="red")
        self.nodes_coordinates_dict[new_node] = (x, y)


    def remove_node(self, node):

        del self.nodes_coordinates_dict[node]
        self.canvas.delete(node)


    def right_click(self, event):
        x, y = event.x, event.y
        r = self.node_size

        clicked_node = None

        for node, coordinates in self.nodes_coordinates_dict.items():
            if coordinates[0] - r < x < coordinates[0] + r and coordinates[1] - r < y < coordinates[1] + r:
                clicked_node = node
                break
            
        if clicked_node is not None:

            if self.selected_node is not None:
                
                if self.selected_node == clicked_node:
                    self.canvas.itemconfig(self.selected_node, fill="red")
                    self.selected_node = None


                else:

                    self.add_edge(self.selected_node, clicked_node)

                    self.canvas.itemconfig(self.selected_node , fill="red")                    
                    self.selected_node = None


            else:
                self.selected_node = clicked_node
                self.canvas.itemconfig(clicked_node, fill="green")

        else : 
            lines_to_remove = []
            for line, nodes in self.edge_list.items():
                node1, node2 = nodes
                node1 = self.nodes_coordinates_dict[node1]
                node2 = self.nodes_coordinates_dict[node2]
                if self.is_point_near_line(x, y, node1[0], node1[1], node2[0], node2[1], 3):
                    lines_to_remove.append(line)

            for line in lines_to_remove:
                self.remove_edge(line)
                
        
        return


    def add_edge(self, node1, node2):

        x1, y1 = self.nodes_coordinates_dict[node1]
        x2, y2 = self.nodes_coordinates_dict[node2]

        line = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
        self.edge_list[line] = (node1, node2)

    
    def remove_edge(self, line):
        self.canvas.delete(line)
        del self.edge_list[line]


    def is_point_near_line(self, x0, y0, x1, y1, x2, y2, tolerance):

        # Calcul de la distance du point (x0, y0) à la ligne (x1, y1) -> (x2, y2)
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distance = numerator / denominator

        # Retourne True si la distance est inférieure à la tolérance
        return distance <= tolerance
    
    def compute_matrix(self):

        edges_matrix = [[0 for i in range(len(self.nodes_coordinates_dict))] for j in range(len(self.nodes_coordinates_dict))]
        nodes_list = list(self.nodes_coordinates_dict.keys())

        for _, nodes in self.edge_list.items():
            node1, node2 = nodes
            index1 = nodes_list.index(node1)
            index2 = nodes_list.index(node2)

            edges_matrix[index1][index2] = self.distance(node1, node2)
            edges_matrix[index2][index1] = self.distance(node1, node2)

        return edges_matrix, list(self.nodes_coordinates_dict.values())

        

    def distance(self, node1, node2):
        x1, y1 = self.nodes_coordinates_dict[node1]
        x2, y2 = self.nodes_coordinates_dict[node2]

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) 


class CSV_Controller: 

    folder_path = os.path.join(Path(__file__).resolve().parent, "csv_files")

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
                # f.write(str(nodes_list[i]) + ",")
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

        return edges_matrix, nodes_list


# main function
if __name__ == "__main__":

    gc = GraphCreation(1000, 600)
    gc.load_image(os.path.join(Path(__file__).resolve().parent, "image1.jpg"))
    gc.display_image()

    edges_matrix, nodes_list = gc.compute_matrix()

    csvController = CSV_Controller()

    csvController.save(edges_matrix, nodes_list)

    edges_matrix, nodes_list = csvController.load(5)

    print(edges_matrix)
    print(nodes_list)


