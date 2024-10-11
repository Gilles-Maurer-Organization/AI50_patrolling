def algo_dfs(matrix, node, visited):
    '''
    Parcours en profondeur (DFS) pour marquer tous les sommets atteignables comme visités.

    args:
        matrix (Matrix): matrice d'adjacence (via compute_matrix())
        node (Int): le nœud de départ
        visited (List): liste marquant l'état de visite de chaque nœud
    '''

    # noeud actuel considéré comme "visité"
    visited[node] = True

    for neighbor, connected in enumerate(matrix[node]):
        # si une connexion existe et que le voisin n'a pas encore été visité
        if connected != 0 and not visited[neighbor]:
            # appel récursif pour explorer le voisin
            algo_dfs(matrix, neighbor, visited)


def is_graph_eulerian(graph):
    '''
    Vérifie si le graphe est eulérien ou semi-eulérien.

    args:
        graph (Matrix): matrice d'adjacence (via compute_matrix())

    returns:
        - "eulérien" si le graphe est un cycle eulérien
        - "semi-eulérien" si le graphe est un chemin eulérien
        - "pas eulérien" sinon
    '''
    edges_matrix = graph[0]  # matrice d'adjacence

    odd_degree_nodes = 0  # compteur de nœuds de degré impair

    # on vérifie le degré de chaque sommet
    for node, row in enumerate(edges_matrix):
        degree = sum(1 for weight in row if weight != 0) # calcul du degré

        if degree == 0:
            continue  # on ignore les sommets isolés

        if degree % 2 != 0:
            odd_degree_nodes += 1

        if odd_degree_nodes > 2:
            return "non eulérien"  # plus de deux nœuds de degré impair => pas eulérien

    # on cherche un noeud de départ pour le DFS
    start_node = next((i for i, row in enumerate(edges_matrix) if any(row)), None)
    if start_node is None:
        return "eulérien"  # trivialement eulérien car aucun noeud n'est connecté

    # DFS pour vérifier la connexité (condition pour être eulérien ou semi-eulérien)
    visited = [False] * len(edges_matrix) # répertorie les noeuds visités
    algo_dfs(edges_matrix, start_node, visited)

    # on vérifie que chaque sommet ayant au moins une arête a été visité
    for node, row in enumerate(edges_matrix):
        if any(row) and not visited[node]:  # Si le sommet est connecté mais pas visité
            return "non eulérien"  # Le graphe n'est pas connexe, donc pas eulérien

    # on détermine si le graphe est eulérien ou semi-eulérien
    if odd_degree_nodes == 0:
        return "eulérien" # revient au point de départ (= circuit eulérien)
    elif odd_degree_nodes == 2:
        return "semi-eulérien" # ne revient pas au point de départ (=chemin eulérien)
    else:
        return "non eulérien"

