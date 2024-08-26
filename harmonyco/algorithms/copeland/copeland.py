def heuristic_copeland(instance, verbose=False):
    """
    Implémentation de l'heuristique Copeland en Python pour calculer la médiane des permutations.

    Parameters:
    - instance: Objet contenant les données de l'instance (par exemple, les distances tabulées).
    - verbose (bool): Si True, affiche des informations détaillées.

    Returns:
    - None: Met à jour l'objet instance avec les résultats de l'algorithme Copeland.
    """
    inf_score = float('inf')
    num_elements = instance.n
    copeland_scores = [0] * num_elements
    elements = list(range(1, num_elements + 1))

    # Calcul des scores de Copeland pour chaque élément
    for i in range(num_elements):
        for j in range(num_elements):
            if instance.tabD[i][j] > instance.tabD[j][i]:
                copeland_scores[i] += 1  # L'élément i perd contre l'élément j -> +1 défaite

    # Tri des éléments en fonction des scores de Copeland
    elements_sorted, copeland_scores_sorted = zip(
        *sorted(zip(elements, copeland_scores), key=lambda x: x[1], reverse=True))

    # Conversion de la liste triée en une permutation
    copeland_permutation = list(elements_sorted)

    # Calcul de la distance à l'ensemble des matrices et mise à jour du score
    copeland_best_score = instance.distance_to_set_matrix(copeland_permutation)
    instance.Copeland_upper_bound = copeland_best_score
    instance.add_solver_permutation(copeland_permutation)
    instance.set_upper_bound(copeland_best_score)

    if verbose:
        print(f"Copeland ({copeland_best_score}) {copeland_permutation}")

