# BestOfA.py

def kendall_tau_distance(perm1, perm2):
    """
    Calcule la distance de Kendall-Tau entre deux permutations.

    Parameters:
    - perm1 (list): La première permutation.
    - perm2 (list): La seconde permutation.

    Returns:
    - int: La distance de Kendall-Tau entre les deux permutations.
    """
    n = len(perm1)
    pairs = [(perm1[i], perm1[j]) for i in range(n) for j in range(i + 1, n)]
    return sum((perm2.index(x) > perm2.index(y)) for x, y in pairs)


def heuristic_best_of_a(instance, verbose=False):
    """
    Implémentation de l'heuristique Best of A en Python pour calculer la médiane des permutations.

    Parameters:
    - instance: Objet contenant les données de l'instance (par exemple, les permutations et les distances tabulées).
    - verbose (bool): Si True, affiche des informations détaillées.

    Returns:
    - None: Met à jour l'objet instance avec les résultats de l'algorithme Best of A.
    """
    best_score = float('inf')
    dist_to_a = 0
    best_permutation = None

    # Parcours de chaque permutation dans l'ensemble A
    for permutation in instance.A:
        dist_to_a = permutation.distance_to_set_matrix(instance.tabD)
        if dist_to_a < best_score:
            best_score = dist_to_a
            best_permutation = permutation

    # Mise à jour des résultats dans l'instance
    instance.BestOfA_upper_bound = best_score
    instance.add_solver_permutation(best_permutation)
    instance.set_upper_bound(best_score)

    if verbose:
        print(f"BestOfA ({best_score}) {best_permutation}")


if __name__ == "__main__":
    # Exemple de permutations
    permutations = [
        [1, 2, 3],
        [3, 1, 2],
        [2, 3, 1]
    ]

    # Calcul de la médiane
    median = heuristic_best_of_a(permutations)
    print("Médiane trouvée:", median)
