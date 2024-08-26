class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, value):
        """
        Met à jour l'arbre de Fenwick en ajoutant 'value' à l'indice 'index'.
        """
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def query(self, index):
        """
        Retourne la somme cumulative des éléments de 1 à 'index' dans l'arbre de Fenwick.
        """
        sum = 0
        while index > 0:
            sum += self.tree[index]
            index -= index & -index
        return sum


def kendall_tau_distance_with_fenwick(permutation1, permutation2):
    """
    Calcule la distance de Kendall-Tau entre deux permutations en utilisant un arbre de Fenwick.

    Parameters:
    - permutation1 (list): La première permutation.
    - permutation2 (list): La seconde permutation.

    Returns:
    - int: La distance de Kendall-Tau entre les deux permutations.
    """
    n = len(permutation1)

    # Inverser permutation2 pour obtenir l'ordre des indices dans permutation1
    position_in_permutation2 = [0] * (n + 1)
    for i, value in enumerate(permutation2):
        position_in_permutation2[value] = i + 1

    # Représenter permutation1 en termes de positions dans permutation2
    mapped_permutation = [position_in_permutation2[value] for value in permutation1]

    # Calcul de la distance de Kendall-Tau en utilisant un arbre de Fenwick
    fenwick_tree = FenwickTree(n)
    kendall_tau_distance = 0

    for i in range(n):
        # Ajouter le nombre d'inversions jusqu'à l'indice actuel
        kendall_tau_distance += i - fenwick_tree.query(mapped_permutation[i])

        # Mettre à jour l'arbre de Fenwick avec la position actuelle
        fenwick_tree.update(mapped_permutation[i], 1)

    return kendall_tau_distance


# Exemple d'utilisation
if __name__ == "__main__":
    perm1 = [10, 6, 7 , 8 , 9,5 , 1, 3, 2, 4]
    perm2 = [1, 4,5 ,10 , 9, 8, 7 , 6, 3, 2]
    distance = kendall_tau_distance_with_fenwick(perm1, perm2)
    print(f"La distance de Kendall-Tau entre les permutations est : {distance}")
