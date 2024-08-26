# branchandbound.py
import random
from typing import List

class pickaperm_algorithm:
    """
    Implémentation de l'algorithme Pick-a-Perm pour sélectionner une permutation parmi un ensemble de permutations.
    """

    def __init__(self, permutations: List[List[int]]):
        """
        Initialise l'algorithme Pick-a-Perm avec un ensemble de permutations.

        :param permutations: Une liste de permutations (classements).
        """
        self.permutations = permutations

    def pick(self) -> List[int]:
        """
        Sélectionne une permutation parmi l'ensemble des permutations selon une stratégie donnée.

        :return: Une permutation sélectionnée.
        """
        # Implémentation simple : sélectionne une permutation au hasard parmi les permutations données
        return random.choice(self.permutations)

    def pick_best(self) -> List[int]:
        """
        Sélectionne la "meilleure" permutation parmi l'ensemble des permutations en fonction d'un critère simple,
        par exemple, la permutation qui a le plus de positions fixes (identiques à un classement de référence).

        :return: La permutation sélectionnée comme étant la "meilleure".
        """
        best_permutation = None
        best_score = -1

        for permutation in self.permutations:
            score = self._evaluate_permutation(permutation)
            if score > best_score:
                best_score = score
                best_permutation = permutation

        return best_permutation

    def _evaluate_permutation(self, permutation: List[int]) -> int:
        """
        Évalue une permutation selon un critère simple.

        :param permutation: La permutation à évaluer.
        :return: Un score basé sur le nombre de positions fixes dans la permutation.
        """
        # Exemple de critère : compte le nombre de positions fixes (où l'élément est à sa place d'origine)
        score = 0
        for i, element in enumerate(permutation):
            if element == i + 1:  # Suppose que les éléments sont de 1 à n
                score += 1
        return score


# Exemple d'utilisation
if __name__ == "__main__":
    # Ensemble de permutations
    permutations = [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 1, 4, 3],
        [3, 4, 1, 2]
    ]

    picker = PickAPerm(permutations)

    # Sélectionne une permutation au hasard
    chosen_permutation = picker.pick()
    print(f"Permutation choisie aléatoirement : {chosen_permutation}")

    # Sélectionne la "meilleure" permutation selon le critère dé
