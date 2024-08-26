from typing import List, Dict, Set
import numpy as np


class MOT3LUBC:
    """
    Classe pour gérer les contraintes MOT3 et LUBC dans le cadre du problème de la médiane de permutation.
    MOT3 (Majority of Three) est une méthode qui vérifie les triplets d'éléments pour des relations de majorité,
    tandis que LUBC (Linear Upper Bound Constraints) applique des contraintes linéaires pour améliorer l'élagage
    lors de la recherche de la solution optimale.
    """

    def __init__(self, n: int):
        """
        Initialise l'objet MOT3LUBC avec le nombre d'éléments à classer.

        :param n: Le nombre total d'éléments dans le problème de la médiane de permutation.
        """
        self.n = n
        self.tabMOT3 = np.zeros((n, n, n), dtype=bool)  # Tableau pour stocker les triplets MOT3
        self.tabLUBC = np.zeros((n, n), dtype=int)  # Tableau pour stocker les contraintes LUBC
        self._initialize_constraints()

    def _initialize_constraints(self):
        """
        Initialise les contraintes de base MOT3 et LUBC.
        """
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    for k in range(self.n):
                        if i != k and j != k:
                            self.tabMOT3[i][j][k] = self._compute_mot3_constraint(i, j, k)
                    self.tabLUBC[i][j] = self._compute_lubc_constraint(i, j)

    def _compute_mot3_constraint(self, i: int, j: int, k: int) -> bool:
        """
        Calcule la contrainte MOT3 pour un triplet d'éléments (i, j, k).

        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :param k: Indice du troisième élément.
        :return: Vrai si le triplet satisfait la contrainte MOT3, sinon Faux.
        """
        # Implémentation simplifiée pour démonstration ; la logique réelle dépend de l'application
        # MOT3 vérifie si l'ordre de préférence entre trois éléments respecte une règle de majorité
        return (i < j and j < k) or (k < j and j < i)

    def _compute_lubc_constraint(self, i: int, j: int) -> int:
        """
        Calcule la contrainte LUBC entre deux éléments (i, j).

        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :return: La valeur de la contrainte LUBC entre i et j.
        """
        # Implémentation simplifiée pour démonstration ; la logique réelle dépend de l'application
        # LUBC est souvent utilisé pour établir des bornes supérieures dans l'élagage d'un arbre de recherche
        return abs(i - j)

    def check_mot3(self, pi: List[int]) -> bool:
        """
        Vérifie si une permutation respecte toutes les contraintes MOT3.

        :param pi: La permutation à vérifier.
        :return: Vrai si la permutation respecte toutes les contraintes MOT3, sinon Faux.
        """
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    if self.tabMOT3[i][j][k] and not self._check_order(pi, i, j, k):
                        return False
        return True

    def _check_order(self, pi: List[int], i: int, j: int, k: int) -> bool:
        """
        Vérifie si l'ordre de la permutation respecte l'ordre attendu entre les éléments i, j, et k.

        :param pi: La permutation à vérifier.
        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :param k: Indice du troisième élément.
        :return: Vrai si l'ordre est respecté, sinon Faux.
        """
        pos_i = pi.index(i)
        pos_j = pi.index(j)
        pos_k = pi.index(k)
        return (pos_i < pos_j < pos_k) or (pos_k < pos_j < pos_i)

    def check_lubc(self, pi: List[int]) -> bool:
        """
        Vérifie si une permutation respecte toutes les contraintes LUBC.

        :param pi: La permutation à vérifier.
        :return: Vrai si la permutation respecte toutes les contraintes LUBC, sinon Faux.
        """
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.tabLUBC[i][j] > 0:
                    if not self._check_distance(pi, i, j):
                        return False
        return True

    def _check_distance(self, pi: List[int], i: int, j: int) -> bool:
        """
        Vérifie si la distance entre deux éléments dans la permutation respecte la contrainte LUBC.

        :param pi: La permutation à vérifier.
        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :return: Vrai si la distance est respectée, sinon Faux.
        """
        distance = abs(pi.index(i) - pi.index(j))
        return distance <= self.tabLUBC[i][j]

    def apply_constraints(self, permutations: List[List[int]]) -> List[List[int]]:
        """
        Applique les contraintes MOT3 et LUBC à une liste de permutations et retourne celles qui les respectent.

        :param permutations: La liste des permutations à filtrer.
        :return: La liste des permutations qui respectent toutes les contraintes.
        """
        valid_permutations = []
        for pi in permutations:
            if self.check_mot3(pi) and self.check_lubc(pi):
                valid_permutations.append(pi)
        return valid_permutations

    def add_custom_mot3_constraint(self, i: int, j: int, k: int, value: bool):
        """
        Ajoute ou modifie une contrainte MOT3 personnalisée pour un triplet d'éléments (i, j, k).

        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :param k: Indice du troisième élément.
        :param value: La valeur booléenne de la contrainte (True pour active, False pour désactive).
        """
        self.tabMOT3[i][j][k] = value

    def add_custom_lubc_constraint(self, i: int, j: int, value: int):
        """
        Ajoute ou modifie une contrainte LUBC personnalisée entre deux éléments (i, j).

        :param i: Indice du premier élément.
        :param j: Indice du deuxième élément.
        :param value: La valeur entière de la contrainte LUBC.
        """
        self.tabLUBC[i][j] = value
