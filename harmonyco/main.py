# main.py

# Importation des bibliothèques standards
import sys
import argparse

# Importation des modules spécifiques au projet

from algorithms.Algorithm_choice import get_algorithm, list_available_algorithms
#from . import load_permutations, calculate_median



# Importation des autres modules nécessaires (si nécessaire)
# import other_module

def main():
    """
    Point d'entrée principal du programme HarmonyCo.
    Gère l'interface utilisateur, la sélection des algorithmes,
    et l'exécution du calcul de la médiane des permutations.
    """

    # Analyse des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Calcul de la médiane des permutations avec HarmonyCo")
    parser.add_argument('-a', '--algorithm', type=str, choices=list_available_algorithms(),
                        help="Choisissez l'algorithme à utiliser pour calculer la médiane")
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="Chemin vers le fichier contenant les permutations")
    parser.add_argument('-o', '--output', type=str, required=False,
                        help="Chemin vers le fichier de sortie pour enregistrer les résultats")

    args = parser.parse_args()

    # Chargement des permutations depuis le fichier fourni
    permutations = load_permutations(args.file)

    if permutations is None:
        print("Erreur : Le fichier des permutations n'a pas pu être chargé.")
        sys.exit(1)

    # Sélection de l'algorithme choisi par l'utilisateur
    algorithm = get_algorithm(args.algorithm)

    if algorithm is None:
        print(f"Erreur : L'algorithme '{args.algorithm}' n'est pas disponible.")
        sys.exit(1)

    # Calcul de la médiane des permutations
    print(f"Calcul de la médiane en utilisant l'algorithme : {args.algorithm}")
    median_permutation = calculate_median(permutations, algorithm)

    # Affichage ou enregistrement du résultat
    if args.output:
        with open(args.output, 'w') as f:
            f.write(f"Median Permutation: {median_permutation}\n")
        print(f"Résultats enregistrés dans : {args.output}")
    else:
        print(f"Median Permutation: {median_permutation}")


if __name__ == "__main__":
    main()
