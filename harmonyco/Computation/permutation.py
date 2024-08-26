from typing import List


class Permutation:
    """
    Classe pour représenter une permutation. Une permutation est définie comme une liste ordonnée d'éléments uniques.
    """

    def __init__(self, elements: List[int]):
        """
        Initialise une permutation avec une liste d'éléments.

        :param elements: Une liste d'entiers représentant une permutation.
        """
        if len(elements) != len(set(elements)):
            raise ValueError("Tous les éléments doivent être uniques.")
        self.elements = elements

    def __repr__(self):
        """
        Représentation en chaîne de caractères de la permutation.
        :return: Une chaîne de caractères représentant la permutation.
        """
        return f"Permutation({self.elements})"

    def __len__(self):
        """
        Retourne la taille de la permutation.
        :return: La taille de la permutation.
        """
        return len(self.elements)

    def __getitem__(self, index: int) -> int:
        """
        Accès à un élément de la permutation par index.

        :param index: L'index de l'élément.
        :return: L'élément à l'index donné.
        """
        return self.elements[index]

    def invert(self) -> 'Permutation':
        """
        Inverse la permutation. L'inversion d'une permutation place chaque élément à l'indice de sa valeur d'origine.

        :return: Une nouvelle permutation qui est l'inverse de la permutation actuelle.
        """
        inverted = [0] * len(self.elements)
        for i, element in enumerate(self.elements):
            inverted[element - 1] = i + 1
        return Permutation(inverted)

    def distance(self, other: 'Permutation') -> int:
        """
        Calcule la distance de Kendall-Tau entre cette permutation et une autre.
        La distance de Kendall-Tau est le nombre de paires discordantes entre deux permutations.

        :param other: Une autre permutation.
        :return: La distance de Kendall-Tau entre les deux permutations.
        """
        if len(self.elements) != len(other):
            raise ValueError("Les deux permutations doivent avoir la même taille.")

        inversion_count = 0
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                if (self.elements[i] < self.elements[j]) != (other[i] < other[j]):
                    inversion_count += 1
        return inversion_count

    def is_identity(self) -> bool:
        """
        Vérifie si la permutation est l'identité (c'est-à-dire que les éléments sont dans l'ordre naturel).

        :return: True si la permutation est l'identité, sinon False.
        """
        return self.elements == list(range(1, len(self.elements) + 1))

    def apply(self, other: 'Permutation') -> 'Permutation':
        """
        Applique une autre permutation à cette permutation.

        :param other: La permutation à appliquer.
        :return: Une nouvelle permutation résultant de l'application de l'autre permutation à celle-ci.
        """
        if len(self.elements) != len(other):
            raise ValueError("Les deux permutations doivent avoir la même taille.")

        applied = [self.elements[other[i] - 1] for i in range(len(self.elements))]
        return Permutation(applied)

    def to_cycle_notation(self) -> str:
        """
        Représente la permutation en notation cyclique.

        :return: Une chaîne de caractères représentant la permutation en notation cyclique.
        """
        visited = [False] * len(self.elements)
        cycles = []

        for i in range(len(self.elements)):
            if not visited[i]:
                cycle = []
                x = i
                while not visited[x]:
                    visited[x] = True
                    cycle.append(x + 1)
                    x = self.elements[x] - 1
                if len(cycle) > 1:
                    cycles.append(cycle)

        cycle_str = ''.join(f"({' '.join(map(str, cycle))})" for cycle in cycles)
        return cycle_str or "()"


# Exemple d'utilisation
if __name__ == "__main__":
    p1 = Permutation([4, 3, 2, 1])
    p2 = Permutation([1, 2, 3, 4])

    print("Permutation p1 :", p1)
    print("Permutation p2 :", p2)
    print("Distance Kendall-Tau entre p1 et p2 :", p1.distance(p2))
    print("Inverse de p1 :", p1.invert())
    print("Permutation identité ?", p2.is_identity())
    print("Application de p2 à p1 :", p1.apply(p2))
    print("Notation cyclique de p1 :", p1.to_cycle_notation())
