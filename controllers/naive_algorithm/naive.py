

class Naive:
    def __init__(self,parameters_view, graph_controller):
        self.graph = graph_controller.graph
        super().__init__(parameters_view, graph_controller)

    def calc_path():
        print(self.graph.computematrix())




if __name__ == "__main__":
    # Exemple of path :
    naif = Naive(parameters_view, graph_controller)
    path=   [    
                [0, 1, 2, 3, 4],  # Agent 1 fait le tour du pentagone
                [4, 3, 2, 1, 0],  # Agent 2 fait le tour inverse
                [0, 2, 4],        # Agent 3 suit un chemin en étoile
                [1, 3, 0],        # Agent 4 suit un autre chemin en étoile
                [2, 0, 3, 4, 1]   # Agent 5 suit un chemin en zigzag
            ]
    
    print(graph.computematrix())