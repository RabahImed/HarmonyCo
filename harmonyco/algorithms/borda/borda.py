def heuristic_borda_count(instance, verbose=False):
    """
    Implémentation de l'heuristique Borda Count en Python pour calculer la médiane des permutations.

    Parameters:
    - instance: Objet contenant les données de l'instance (par exemple, les distances tabulées).
    - verbose (bool): Si True, affiche des informations détaillées.

    Returns:
    - None: Met à jour l'objet instance avec les résultats de l'algorithme Borda Count.
    """
    best_score = float('inf')
    n = instance.n
    tab_values = [0] * n
    tab_elements = list(range(1, n + 1))

    # Calcul des valeurs Borda pour chaque élément
    for i in range(n):
        tab_values[i] = sum(instance.tabD[i][j] for j in range(n))

    # Tri des éléments en fonction des valeurs Borda (ordre croissant)
    tab_elements_sorted, tab_values_sorted = zip(*sorted(zip(tab_elements, tab_values), key=lambda x: x[1]))

    # Conversion de la liste triée en une permutation
    result = Permutation(list(tab_elements_sorted))

    # Calcul de la distance à l'ensemble des matrices et mise à jour du score
    best_score = result.distance_to_set_matrix(instance.tabD)
    instance.Borda_upper_bound = best_score
    instance.add_solver_permutation(result)
    instance.set_upper_bound(best_score)

    if verbose:
        print(f"BordaCount ({best_score}) {result}")
