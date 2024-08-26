
from typing import List, Dict
from itertools import permutations

class Permutation:
    def __init__(self, elements: List[int]):
        self.elements = elements

    def distance_to(self, other: 'Permutation') -> int:
        """
        Calcule la distance de Kendall-Tau entre cette permutation et une autre.
        :param other: Une autre permutation.
        :return: La distance de Kendall-Tau.
        """
        return KemenyScoreCalculator.count_inversions([self.elements.index(x) for x in other.elements])

    def __repr__(self):
        return f"Permutation({self.elements})"


class KemenyScoreCalculator:
    @staticmethod
    def count_inversions(arr: List[int]) -> int:
        return KemenyScoreCalculator._merge_sort_and_count(arr, 0, len(arr) - 1)

    @staticmethod
    def _merge_sort_and_count(arr: List[int], left: int, right: int) -> int:
        if left >= right:
            return 0

        mid = (left + right) // 2
        inv_count = KemenyScoreCalculator._merge_sort_and_count(arr, left, mid)
        inv_count += KemenyScoreCalculator._merge_sort_and_count(arr, mid + 1, right)
        inv_count += KemenyScoreCalculator._merge_and_count(arr, left, mid, right)

        return inv_count

    @staticmethod
    def _merge_and_count(arr: List[int], left: int, mid: int, right: int) -> int:
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


class parcons_algorithm:
    """
    Implémentation de l'algorithme Parcons pour calculer la médiane de permutations.
    """

    def __init__(self, permutations: List[Permutation]):
        self.permutations = permutations

    def calculate_median(self) -> Permutation:
        """
        Calcule la permutation médiane en minimisant la somme des distances Kendall-Tau à toutes les permutations données.
        :return: La permutation médiane.
        """
        all_elements = list(range(1, len(self.permutations[0].elements) + 1))
        best_permutation = None
        best_distance = float('inf')

        for perm in permutations(all_elements):
            current_perm = Permutation(list(perm))
            total_distance = sum(current_perm.distance_to(p) for p in self.permutations)

            if total_distance < best_distance:
                best_distance = total_distance
                best_permutation = current_perm

        return best_permutation


# Exemple d'utilisation
if __name__ == "__main__":
    # Ensemble de permutations
    perms = [
        Permutation([1, 2, 3, 4]),
        Permutation([4, 3, 2, 1]),
        Permutation([2, 1, 4, 3]),
        Permutation([3, 4, 1, 2])
    ]

    parcons = Parcons(perms)
    median_perm = parcons.calculate_median()
    print(f"Permutation médiane calculée : {median_perm.elements}")
