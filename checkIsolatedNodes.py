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

def check_for_isolated_nodes(graph):
    '''
       Vérifie si le graphe contient des noeuds isolés (1 ou +).

       args:
           graph (Matrix): matrice d'adjacence (via compute_matrix())

       returns:
           - False si aucun noeud est isolé
           - True si au moins 1 noeud est isolé
       '''

    edges_matrix = graph[0]  # matrice d'adjacence

    for edge_list in edges_matrix:
        # si un noeud n'a pas de connexion vers un autre
        if not any(edge_list):
            return True

    #noeud de départ
    start_node = next((i for i, row in enumerate(edges_matrix) if any(row)), None)
    if start_node is None:
        return True # tous les noeuds sont isolés

    # DFS pour vérifier la connexité (s'il y a des noeuds isolés ou pas)
    visited = [False] * len(edges_matrix)  # répertorie les noeuds visités
    algo_dfs(edges_matrix, start_node, visited)

    # on vérifie que chaque sommet ayant au moins une arête ait été visitée
    for node, row in enumerate(edges_matrix):
        if any(row) and not visited[node]:  # Si le noeud possède une connexion mais n'est visité
            return True  # présence de noeud isolé

    return False
