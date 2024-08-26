from typing import List, Dict, Any
from permutation import Permutation
from preprocessing import PermutationPreprocessor


class Consensus:
    """
    Classe pour représenter et gérer un objet Consensus.
    Un Consensus est défini comme une liste de classements (classements de consensus).
    """

    def __init__(self, rankings: List[List[int]], additional_info: Dict[str, Any] = None):
        """
        Initialise un objet Consensus avec une liste de classements.

        :param rankings: Une liste de classements, où chaque classement est une permutation.
        :param additional_info: Un dictionnaire contenant des informations supplémentaires sur le consensus (facultatif).
        """
        preprocessor = PermutationPreprocessor()
        self.rankings = [Permutation(preprocessor.normalize_permutation(r)) for r in rankings]
        self.additional_info = additional_info if additional_info is not None else {}

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Consensus.
        :return: Une chaîne de caractères représentant l'objet Consensus.
        """
        return f"Consensus(rankings={self.rankings}, additional_info={self.additional_info})"

    def add_ranking(self, ranking: List[int]):
        """
        Ajoute un nouveau classement à l'objet Consensus.

        :param ranking: Un classement à ajouter (une permutation).
        """
        preprocessor = PermutationPreprocessor()
        normalized_ranking = preprocessor.normalize_permutation(ranking)
        self.rankings.append(Permutation(normalized_ranking))

    def remove_ranking(self, index: int):
        """
        Supprime un classement de l'objet Consensus par son index.

        :param index: L'index du classement à supprimer.
        """
        if index < 0 or index >= len(self.rankings):
            raise IndexError("Index hors limites.")
        self.rankings.pop(index)

    def get_ranking(self, index: int) -> Permutation:
        """
        Récupère un classement spécifique par son index.

        :param index: L'index du classement à récupérer.
        :return: Le classement à l'index spécifié sous forme d'objet Permutation.
        """
        if index < 0 or index >= len(self.rankings):
            raise IndexError("Index hors limites.")
        return self.rankings[index]

    def get_all_rankings(self) -> List[Permutation]:
        """
        Retourne tous les classements de l'objet Consensus.

        :return: Une liste de tous les classements sous forme d'objets Permutation.
        """
        return self.rankings

    def compute_consensus(self) -> Permutation:
        """
        Calcule un classement de consensus à partir des classements actuels.
        Cette méthode peut implémenter un algorithme spécifique pour générer le classement de consensus.

        :return: Un classement de consensus basé sur les classements actuels sous forme d'objet Permutation.
        """
        # Implémentation simplifiée : retourne la première permutation comme consensus.
        # Vous pouvez remplacer cela par un algorithme plus sophistiqué, comme la méthode de Kemeny-Young.
        return self.rankings[0]

    def add_additional_info(self, key: str, value: Any):
        """
        Ajoute des informations supplémentaires au consensus.

        :param key: La clé de l'information supplémentaire.
        :param value: La valeur associée à la clé.
        """
        self.additional_info[key] = value

    def get_additional_info(self, key: str) -> Any:
        """
        Récupère une information supplémentaire spécifique.

        :param key: La clé de l'information à récupérer.
        :return: La valeur associée à la clé, ou None si la clé n'existe pas.
        """
        return self.additional_info.get(key)

    def __len__(self):
        """
        Retourne le nombre de classements dans l'objet Consensus.

        :return: Le nombre de classements.
        """
        return len(self.rankings)

    def __iter__(self):
        """
        Retourne un itérateur sur les classements de l'objet Consensus.

        :return: Un itérateur sur les classements.
        """
        return iter(self.rankings)

    def __getitem__(self, index: int) -> Permutation:
        """
        Permet l'accès à un classement via l'indexation.

        :param index: L'index du classement.
        :return: Le classement à l'index spécifié sous forme d'objet Permutation.
        """
        return self.get_ranking(index)

    def describe(self) -> str:
        """
        Retourne une description complète du consensus, y compris les informations supplémentaires.

        :return: Une chaîne de caractères décrivant l'objet Consensus.
        """
        desc = f"Consensus avec {len(self.rankings)} classements.\n"
        desc += "Classements :\n"
        for i, ranking in enumerate(self.rankings):
            desc += f"  {i + 1}: {ranking.elements}\n"
        desc += "Informations supplémentaires :\n"
        for key, value in self.additional_info.items():
            desc += f"  {key}: {value}\n"
        return desc


# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'un objet Consensus avec deux classements
    consensus = Consensus(rankings=[[4, 2, 3, 1], [3, 2, 4, 1]])

    # Ajout d'un nouveau classement
    consensus.add_ranking([2, 4, 1, 3])

    # Affichage de tous les classements
    print("Tous les classements :", [r.elements for r in consensus.get_all_rankings()])

    # Calcul du consensus (implémentation simplifiée)
    print("Classement de consensus :", consensus.compute_consensus().elements)

    # Ajout d'informations supplémentaires
    consensus.add_additional_info("méthode", "Copeland")

    # Description complète de l'objet Consensus
    print(consensus.describe())
