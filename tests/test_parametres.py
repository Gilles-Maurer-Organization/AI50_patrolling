import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import product

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.TextBox import TextBox
from services.algorithms.AntColonyAlgorithm import AntColonyAlgorithm

class AntColonyExperiment:
    def __init__(self, cost_matrix, evaporation_rates, alpha_parameters, beta_parameters, nb_agents, nb_colony, nb_iterations, Q):
        self.cost_matrix = cost_matrix
        self.evaporation_rates = evaporation_rates
        self.alpha_parameters = alpha_parameters
        self.beta_parameters = beta_parameters
        self.nb_agents = nb_agents
        self.nb_colony = nb_colony
        self.nb_iterations = nb_iterations
        self.Q = Q
        self.results = []

    def run_experiment(self):
        i = 0
        for evaporation_rate, alpha, beta in product(self.evaporation_rates, self.alpha_parameters, self.beta_parameters):
            print(f"Running experiment with evaporation_rate={evaporation_rate}, alpha={alpha}, beta={beta}")
            performances = []

            for _ in range(5):
                i += 1
                print(f"Iteration {i}")

                parameters = {
                    "Alpha": TextBox(str(alpha)),
                    "Beta": TextBox(str(beta)),
                    "Pheromone quantity": TextBox(str(self.Q)),
                    "Nb colony" : TextBox(str(self.nb_colony)),
                    "Nb iterations": TextBox(str(self.nb_iterations)),
                    "Evaporation rate": TextBox(str(evaporation_rate))
                }

                fourmis = AntColonyAlgorithm(parameters, self.nb_agents, cost_matrix)
                final_path = fourmis.launch()

                performances.append(final_path)

            if performances:
                self.results.append({
                    "evaporation_rate": evaporation_rate,
                    "alpha": alpha,
                    "beta": beta,
                    "nb_agents": self.nb_agents,
                    "nb_colonies": self.nb_colony,
                    "performance_mean": np.mean(performances),
                    "performance_min": np.min(performances),
                    "performance_max": np.max(performances)
                })


    def plot_results(self):
        results_df = pd.DataFrame(self.results)
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # 1. Performance moyenne vs Taux d'évaporation
        for alpha in self.alpha_parameters:
            for beta in self.beta_parameters:
                subset = results_df[(results_df["alpha"] == alpha) & (results_df["beta"] == beta)]
                label = f"α={alpha}, β={beta}"
                axes[0].plot(subset["evaporation_rate"], subset["performance_mean"], 'o-', label=label)
        axes[0].set_title("Performance moyenne vs Taux d'évaporation")
        axes[0].set_xlabel("Taux d'évaporation")
        axes[0].set_ylabel("Performance moyenne")
        axes[0].legend(fontsize=8)

        # 2. Performance moyenne vs Alpha
        for evaporation_rate in self.evaporation_rates:
            for beta in self.beta_parameters:
                subset = results_df[(results_df["evaporation_rate"] == evaporation_rate) & (results_df["beta"] == beta)]
                label = f"Evap={evaporation_rate:.1f}, β={beta}"
                axes[1].plot(subset["alpha"], subset["performance_mean"], 'o-', label=label)
        axes[1].set_title("Performance moyenne vs Alpha")
        axes[1].set_xlabel("Alpha")
        axes[1].set_ylabel("Performance moyenne")
        axes[1].legend(fontsize=8)

        # 3. Performance moyenne vs Beta
        for evaporation_rate in self.evaporation_rates:
            for alpha in self.alpha_parameters:
                subset = results_df[(results_df["evaporation_rate"] == evaporation_rate) & (results_df["alpha"] == alpha)]
                label = f"Evap={evaporation_rate:.1f}, α={alpha}"
                axes[2].plot(subset["beta"], subset["performance_mean"], 'o-', label=label)
        axes[2].set_title("Performance moyenne vs Beta")
        axes[2].set_xlabel("Beta")
        axes[2].set_ylabel("Performance moyenne")
        axes[2].legend(fontsize=8)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    cost_matrix = np.array([
        [  0.        , 134.00373129,  90.13878189, 182.82231811, 225.17992806,
         342.24828416, 322.26236725, 457.4104342 , 370.8775284 , 389.96053959,
         506.60151302, 261.25545034],
        [134.00373129,   0.        , 224.14251318, 206.0218435 , 347.32007515,
         230.25171905, 444.40251434, 396.45942043, 236.87379711, 255.9568083 ,
         372.59778173, 127.25171905],
        [ 90.13878189, 224.14251318,   0.        , 213.32838536, 315.31870994,
         432.38706604, 412.40114914, 547.54921609, 461.01631029, 480.09932148,
         596.74029491, 351.39423222],
        [182.82231811, 206.0218435 , 213.32838536,   0.        , 408.00224617,
         436.27356255, 505.08468536, 602.48126393, 442.89564062, 461.9786518 ,
         578.61962523, 333.27356255],
        [225.17992806, 347.32007515, 315.31870994, 408.00224617,   0.        ,
         117.0683561 ,  97.08243919, 232.23050614, 329.69043417, 348.77344535,
         465.41441878, 220.0683561 ],
        [342.24828416, 230.25171905, 432.38706604, 436.27356255, 117.0683561 ,
           0.        , 214.15079529, 166.20770139, 212.62207807, 231.70508925,
         348.34606268, 103.        ],
        [322.26236725, 444.40251434, 412.40114914, 505.08468536,  97.08243919,
         214.15079529,   0.        , 135.14806695, 426.77287336, 445.85588455,
         562.49685798, 317.15079529],
        [457.4104342 , 396.45942043, 547.54921609, 602.48126393, 232.23050614,
         166.20770139, 135.14806695,   0.        , 378.82977945, 397.91279064,
         514.55376407, 269.20770139],
        [370.8775284 , 236.87379711, 461.01631029, 442.89564062, 329.69043417,
         212.62207807, 426.77287336, 378.82977945,   0.        , 182.09887424,
         135.72398462, 109.62207807],
        [389.96053959, 255.9568083 , 480.09932148, 461.9786518 , 348.77344535,
         231.70508925, 445.85588455, 397.91279064, 182.09887424,   0.        ,
         146.7548977 , 128.70508925],
        [506.60151302, 372.59778173, 596.74029491, 578.61962523, 465.41441878,
         348.34606268, 562.49685798, 514.55376407, 135.72398462, 146.7548977 ,
           0.        , 245.34606268],
        [261.25545034, 127.25171905, 351.39423222, 333.27356255, 220.0683561 ,
         103.        , 317.15079529, 269.20770139, 109.62207807, 128.70508925,
         245.34606268,   0.        ]
    ])
    evaporation_rates = [0.5]
    alpha_parameters = [4]
    beta_parameters = [1]

    nb_agents = 3
    nb_colony = 5
    nb_iterations = 500
    Q = 10

    experiment = AntColonyExperiment(cost_matrix, evaporation_rates, alpha_parameters, beta_parameters, nb_agents, nb_colony, nb_iterations, Q)
    experiment.run_experiment()
    experiment.plot_results()


