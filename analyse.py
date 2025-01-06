import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from utils.utils import get_data_path

# Data pre-processing
def preprocess(folder: str) -> pd.DataFrame:
    """
    Retrieves data from each instance's csv and merges it into a dataframe

    Args:
        folder (str): Path to the folder containing data files

    Returns:
        pd.DataFrame: A single DataFrame for each instance
    """
    data_list = []
    try:
        for idx, file in enumerate(os.listdir(folder), start=1):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and file.endswith('.csv'):
                df = pd.read_csv(file_path)
                df['instance_num'] = idx
                data_list.append(df)
        final_data = pd.concat(data_list, ignore_index=True)
        final_data = final_data.groupby(['Algorithm', 'Test Number', 'instance_num']).agg(
            all_time_max_idleness=('All-time Max Idleness', 'last'),
            avg_idleness=('Average Idleness', 'mean')
        ).reset_index()
        return final_data
    except FileNotFoundError:
        print("Erreur : Le dossier spécifié est introuvable.")
        return pd.DataFrame()


def test_normality(group):
    stat, p_value = stats.shapiro(group)
    return p_value


def test_variance_equality(groups):
    stat, p_value = stats.levene(*groups)
    return p_value


def statistical_test(df):
    results_normality_avg = {}
    results_normality_max = {}
    results_variance_avg = {}
    results_variance_max = {}
    paired_ttest_results = {}
    instances = df['instance_num'].unique()

    for instance in instances:
        subset = df[df['instance_num'] == instance]
        normality_p_values_avg = {}
        normality_p_values_max = {}

        for alg in subset['Algorithm'].unique():
            avg_idleness_data = subset[subset['Algorithm'] == alg]['avg_idleness']
            max_idleness_data = subset[subset['Algorithm'] == alg]['all_time_max_idleness']
            
            normality_p_values_avg[alg] = test_normality(avg_idleness_data)
            normality_p_values_max[alg] = test_normality(max_idleness_data)
        
        results_normality_avg[instance] = normality_p_values_avg
        results_normality_max[instance] = normality_p_values_max

        groups_avg = [subset[subset['Algorithm'] == alg]['avg_idleness'] for alg in subset['Algorithm'].unique()]
        groups_max = [subset[subset['Algorithm'] == alg]['all_time_max_idleness'] for alg in subset['Algorithm'].unique()]

        results_variance_avg[instance] = test_variance_equality(groups_avg)
        results_variance_max[instance] = test_variance_equality(groups_max)

    print("\n=== Résultats des tests de normalité et d'égalité des variances ===")
    for instance in instances:
        normality_avg_ok = all(p > 0.05 for p in results_normality_avg[instance].values())
        normality_max_ok = all(p > 0.05 for p in results_normality_max[instance].values())
        variance_avg_ok = results_variance_avg[instance] > 0.05
        variance_max_ok = results_variance_max[instance] > 0.05

        print(f"\nInstance {instance}:")
        print(f"  Normalité pour Average Idleness: {'Vérifiée' if normality_avg_ok else 'Non vérifiée'}")
        print(f"  Normalité pour All-time Max Idleness: {'Vérifiée' if normality_max_ok else 'Non vérifiée'}")
        print(f"  Égalité des variances pour Average Idleness: {'Vérifiée' if variance_avg_ok else 'Non vérifiée'}")
        print(f"  Égalité des variances pour All-time Max Idleness: {'Vérifiée' if variance_max_ok else 'Non vérifiée'}")

        if normality_avg_ok and variance_avg_ok:
            subset = df[df['instance_num'] == instance]
            algorithms = subset['Algorithm'].unique()
            paired_ttest_results[instance] = {}
            for i in range(len(algorithms)):
                for j in range(i + 1, len(algorithms)):
                    alg_a = algorithms[i]
                    alg_b = algorithms[j]
                    data_a = subset[subset['Algorithm'] == alg_a]['avg_idleness']
                    data_b = subset[subset['Algorithm'] == alg_b]['avg_idleness']
                    t_stat, p_value = stats.ttest_rel(data_a, data_b)
                    paired_ttest_results[instance][(alg_a, alg_b)] = (t_stat, p_value)

    print("\n=== Résultats des tests t appariés ===")
    for instance, comparisons in paired_ttest_results.items():
        print(f"\nInstance {instance}:")
        for (alg_a, alg_b), (t_stat, p_value) in comparisons.items():
            print(f"  Comparaison {alg_a} vs {alg_b}: t-stat = {t_stat:.4f}, p-value = {p_value:.4f}")


def box_plots(df: pd.DataFrame):
    instances = df['instance_num'].unique()
    for instance in instances:
        df_instance = df[df['instance_num'] == instance]
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_instance, x='Algorithm', y='all_time_max_idleness')
        plt.title(f'Boxplot for instance {instance} - All-time Max Idleness')
        plt.show()
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df_instance, x='Algorithm', y='avg_idleness')
        plt.title(f'Boxplot for instance {instance} - Average Idleness')
        plt.show()


def evolution(folder: str):
    try:
        for file in os.listdir(folder):
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(folder, file))
                df = df[df['Test Number'] == 1]
                algorithms = df['Algorithm'].unique()

                plt.figure(figsize=(10, 6))
                for algo in algorithms:
                    algo_data = df[df['Algorithm'] == algo]
                    plt.plot(algo_data['Simulation Time (s)'], algo_data['All-time Max Idleness'], label=f'{algo}')
                plt.title(f'All-time Max Idleness Evolution - {file}')
                plt.xlabel('Simulation Time (s)')
                plt.ylabel('All-time Max Idleness')
                plt.legend()
                plt.grid()
                plt.show()

                plt.figure(figsize=(10, 6))
                for algo in algorithms:
                    algo_data = df[df['Algorithm'] == algo]
                    plt.plot(algo_data['Simulation Time (s)'], algo_data['Average Idleness'], label=f'{algo}')
                plt.title(f'Average Idleness Evolution - {file}')
                plt.xlabel('Simulation Time (s)')
                plt.ylabel('Average Idleness')
                plt.legend()
                plt.grid()
                plt.show()
    except FileNotFoundError:
        print("Erreur : Le dossier spécifié est introuvable.")


def main():
    folder = get_data_path("results")
    print(folder)
    df = preprocess(folder)
    if df.empty:
        print("Aucune instance chargée.")
        return
    
    try:
        statistical_test(df)
    except ValueError as e:
        print(f"Erreur dans les données pour effectuer le test statistique : {e}")
    
    box_plots(df)
    evolution(folder)


if __name__ == "__main__":
    main()
