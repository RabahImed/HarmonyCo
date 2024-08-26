from typing import List, Tuple


class PermutationPreprocessor:
    """
    Classe pour effectuer le prétraitement des permutations. Elle inclut des méthodes pour vérifier la validité,
    normaliser et convertir des permutations entre différents formats.
    """

    def __init__(self):
        """
        Initialise l'objet PermutationPreprocessor.
        """
        pass

    @staticmethod
    def is_valid_permutation(perm: List[int]) -> bool:
        """
        Vérifie si une liste donnée est une permutation valide.

        :param perm: La liste des éléments à vérifier.
        :return: True si la liste est une permutation valide, sinon False.
        """
        n = len(perm)
        return sorted(perm) == list(range(1, n + 1))

    @staticmethod
    def normalize_permutation(perm: List[int]) -> List[int]:
        """
        Normalise une permutation en ajustant les indices pour qu'ils commencent à 1.

        :param perm: La permutation à normaliser.
        :return: La permutation normalisée.
        """
        rank = {v: i + 1 for i, v in enumerate(sorted(perm))}
        return [rank[v] for v in perm]

    @staticmethod
    def convert_to_cycle_notation(perm: List[int]) -> List[Tuple[int]]:
        """
        Convertit une permutation en notation cyclique.

        :param perm: La permutation à convertir.
        :return: Une liste de tuples représentant la permutation en notation cyclique.
        """
        visited = [False] * len(perm)
        cycles = []

        for i in range(len(perm)):
            if not visited[i]:
                cycle = []
                x = i
                while not visited[x]:
                    visited[x] = True
                    cycle.append(x + 1)
                    x = perm[x] - 1
                if len(cycle) > 1:
                    cycles.append(tuple(cycle))

        return cycles

    @staticmethod
    def convert_from_cycle_notation(cycles: List[Tuple[int]], n: int) -> List[int]:
        """
        Convertit une permutation de la notation cyclique à la notation standard.

        :param cycles: Une liste de tuples représentant la permutation en notation cyclique.
        :param n: Le nombre total d'éléments dans la permutation.
        :return: Une permutation en notation standard.
        """
        perm = list(range(1, n + 1))
        for cycle in cycles:
            if len(cycle) > 1:
                for i in range(len(cycle) - 1):
                    perm[cycle[i] - 1], perm[cycle[i + 1] - 1] = perm[cycle[i + 1] - 1], perm[cycle[i] - 1]
        return perm

    @staticmethod
    def preprocess_permutations(permutations: List[List[int]]) -> List[List[int]]:
        """
        Effectue le prétraitement d'une liste de permutations en vérifiant leur validité et en les normalisant.

        :param permutations: La liste des permutations à prétraiter.
        :return: La liste des permutations prétraitées.
        """
        processed_perms = []
        for perm in permutations:
            if PermutationPreprocessor.is_valid_permutation(perm):
                normalized_perm = PermutationPreprocessor.normalize_permutation(perm)
                processed_perms.append(normalized_perm)
            else:
                raise ValueError(f"La permutation {perm} n'est pas valide.")
        return processed_perms


# Exemple d'utilisation
if __name__ == "__main__":
    preprocessor = PermutationPreprocessor()

    # Exemple de permutations
    permutations = [
        [4, 3, 1, 2],
        [3, 4, 2, 1],
        [1, 2, 3, 4]
    ]

    # Vérification et normalisation des permutations
    try:
        processed_perms = preprocessor.preprocess_permutations(permutations)
        print("Permutations prétraitées :", processed_perms)
    except ValueError as e:
        print(e)

    # Conversion en notation cyclique
    cycle_notation = preprocessor.convert_to_cycle_notation([4, 3, 1, 2])
    print("Notation cyclique :", cycle_notation)

    # Conversion de la notation cyclique à la notation standard
    standard_notation = preprocessor.convert_from_cycle_notation(cycle_notation, 4)
    print("Notation standard à partir de la notation cyclique :", standard_notation)
