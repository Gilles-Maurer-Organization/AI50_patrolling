def algo_dfs(graph, node, visited, visit_count):
    '''
         Vérifie si le graphe est connexe
         
        args:
            graph (Graph): matrice d'adjacence (via compute_matrix())
            node (Int): le noeud de départ (le 1er de la matrice d'adjacence)
            visited (List) : l'état de chaqe noeud du graphe (visité ou non)
            visited_count (List): nombre de fois que chaque noeud a été visité
    '''

    # matrice d'adjacence
    edges_matrix = graph[0]
    # compte chaque visite sur le nœud
    visit_count[node] += 1
    # marque le nœud comme visité
    visited[node] = True

    for neighbor, connected in enumerate(edges_matrix[node]):

        # si une connexion existe
        if connected != 0:
            # si le voisin n'a pas encore été visité dans ce chemin
            if not visited[neighbor]:
                #appel récursif
                algo_dfs(graph, neighbor, visited,visit_count)
            else:
                # incrémente le nombre de visite pour le noeud
                visit_count[neighbor] += 1

def is_graph_eulerian(graph):

    '''
        Vérifie si le graphe donné en paramètre est eulérien ou non

        args:
            graph (Graph): matrice d'adjacence (via compute_matrix())

        returns:
            - True s'il est eulérien
            - False sinon
    '''

    #matriced'adjacence
    edges_matrix = graph[0]

    #vérification de la conformité du graphe, si non conforme, il n'est pas eulérien
    for node, row in enumerate(edges_matrix):

        #on calcule le degré pour chaque noeud
        degree = sum(1 for weight in row if weight != 0)

        #vérifie le cas "noeud isolé" (= non relié)
        if degree == 0:
           # print(f"le noeud {node} n'est pas connecté au graphe")
            return node

        # vérifie le cas "noeud cul de sac"
        if degree < 2:
           # print(f"Le nœud {node} est un cul de sac et va poser porblème s'il n'est pas relié à un autre noeud")
            return node

    #Recherche d'un nœud de départ ayant au moins une connexion pour lancer le DFS
    start_node = next((i for i, row in enumerate(edges_matrix) if any(row)), None)

    #Dictionnaire pour compter le nombre de visites pour chaque nœud
    visit_count = {i: 0 for i in range(len(edges_matrix))}

    #Initialisation de la liste des nœuds visités et lancement du DFS
    visited = [False] * len(edges_matrix)
    algo_dfs(graph,start_node, visited, visit_count)

    if False in visited:
        return False

    #réajuster le nombre de visites de chaque noeud (il est doublé ??)
    for node, count in visit_count.items():
        visit_count[node]//= 2

    '''
    - on vérifie si le noeud a été visité + de 1 fois, s'il a été visité + de 1 fois, il n'est pas eulérien
    - tout en excluant le noeud initial car, selon comment le graphe a été construit,il se peut que le DFS "visite" 
    le noeud initial plusieurs fois même si le graphe est valide
    '''
    for node, count in visit_count.items():
        if count > 1 and node != 0:
            return node

    #si tout est bon, le grpahe est considéré comme eulérien
    return True
