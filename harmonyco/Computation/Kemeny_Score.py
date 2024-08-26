from typing import List, Dict
import numpy as np

class KemenyScoreCalculator:
    """
    Module pour le calcul des scores de Kemeny. L'algorithme de calcul du score est de complexité m * n * log(n) où n est le nombre
    d'éléments et m le nombre de classements. L'algorithme est basé sur le comptage du nombre d'inversions.
    """

    def __init__(self):
        """
        Initialise le calculateur de score de Kemeny.
        """
        pass

    @staticmethod
    def calculate_kemeny_score(rankings: List[List[int]]) -> int:
        """
        Calcule le score de Kemeny pour une liste de classements.

        :param rankings: Une liste de classements, où chaque classement est une permutation.
        :return: Le score de Kemeny, qui est le nombre total d'inversions.
        """
        n = len(rankings[0])
        m = len(rankings)
        # Créer une matrice de préférence où préférence[i][j] est le nombre de fois que i est préféré à j
        preference_matrix = np.zeros((n, n), dtype=int)

        for ranking in rankings:
            for i in range(n):
                for j in range(i + 1, n):
                    preference_matrix[ranking[i] - 1][ranking[j] - 1] += 1

        # Calculer le score de Kemeny en comptant les inversions
        kemeny_score = 0

        for i in range(n):
            for j in range(i + 1, n):
                if preference_matrix[i][j] < preference_matrix[j][i]:
                    kemeny_score += preference_matrix[i][j]
                else:
                    kemeny_score += preference_matrix[j][i]

        return kemeny_score

    @staticmethod
    def count_inversions(ranking: List[int]) -> int:
        """
        Compte le nombre d'inversions dans un classement donné.

        :param ranking: Une permutation.
        :return: Le nombre d'inversions dans le classement.
        """
        return KemenyScoreCalculator._merge_sort_and_count(ranking, 0, len(ranking) - 1)

    @staticmethod
    def _merge_sort_and_count(arr: List[int], left: int, right: int) -> int:
        """
        Utilise l'algorithme de tri fusion pour compter le nombre d'inversions dans un tableau.

        :param arr: Le tableau à trier et à compter les inversions.
        :param left: L'indice de gauche du sous-tableau.
        :param right: L'indice de droite du sous-tableau.
        :return: Le nombre d'inversions dans le sous-tableau.
        """
        if left >= right:
            return 0

        mid = (left + right) // 2
        inv_count = KemenyScoreCalculator._merge_sort_and_count(arr, left, mid)
        inv_count += KemenyScoreCalculator._merge_sort_and_count(arr, mid + 1, right)
        inv_count += KemenyScoreCalculator._merge_and_count(arr, left, mid, right)

        return inv_count

    @staticmethod
    def _merge_and_count(arr: List[int], left: int, mid: int, right: int) -> int:
        """
        Fusionne deux sous-tableaux triés et compte le nombre d'inversions.

        :param arr: Le tableau à fusionner.
        :param left: L'indice de gauche du sous-tableau gauche.
        :param mid: Le point milieu du tableau.
        :param right: L'indice de droite du sous-tableau droit.
        :return: Le nombre d'inversions lors de la fusion.
        """
        left_subarray = arr[left:mid + 1]
        right_subarray = arr[mid + 1:right + 1]

        i = j = 0
        k = left
        inversions = 0

        while i < len(left_subarray) and j < len(right_subarray):
            if left_subarray[i] <= right_subarray[j]:
                arr[k] = left_subarray[i]
                i += 1
            else:
                arr[k] = right_subarray[j]
                inversions += (mid - i + 1 - left)
                j += 1
            k += 1

        while i < len(left_subarray):
            arr[k] = left_subarray[i]
            i += 1
            k += 1

        while j < len(right_subarray):
            arr[k] = right_subarray[j]
            j += 1
            k += 1

        return inversions


# Exemple d'utilisation
if __name__ == "__main__":
    rankings = [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 1, 4, 3]
    ]

    calculator = KemenyScoreCalculator()

    # Calculer le score de Kemeny pour les classements
    score = calculator.calculate_kemeny_score(rankings)
    print(f"Score de Kemeny : {score}")

    # Compter les inversions dans un classement donné
    inversions = calculator.count_inversions([4, 3, 2, 1])
    print(f"Nombre d'inversions : {inversions}")
