# algorithm_choice.py
import argparse

from .BestOfA.BestOfA import heuristic_best_of_a
from .borda.borda import heuristic_borda_count
from .branchandbound.branchandbound import branch_and_bound_recursive
from .copeland.copeland import heuristic_copeland
from .CPLEX.CPLEX import solve_median_permutation_cplex
from .Parcons.Parcons import parcons_algorithm
from .Pickaperm.Pickaperm import pickaperm_algorithm
from .PLNE.PLNE import plne_algorithm
from .SimulatedAnnealing.SimulatedAnnealing import heuristic_sa


def list_available_algorithms():
    """
    Retourne la liste des algorithmes disponibles dans HarmonyCo.
    """
    return [
        'BestOfA',
        'borda',
        'branchandbound',
        'copeland',
        'CPLEX',
        'Parcons',
        'Pickaperm',
        'PLNE',
        'SimulatedAnnealing'
    ]


def get_algorithm(algorithm_name):
    """
    Récupère l'algorithme correspondant au nom fourni.

    Parameters:
    - algorithm_name (str): Nom de l'algorithme choisi.

    Returns:
    - function: La fonction correspondant à l'algorithme choisi.
    """
    algorithms = {
        'BestOfA': heuristic_best_of_a,
        'borda': heuristic_borda_count,
        'branchandbound': branch_and_bound_recursive,
        'copeland': heuristic_copeland,
        'CPLEX': solve_median_permutation_cplex,
        'Parcons': parcons_algorithm,
        'Pickaperm': pickaperm_algorithm,
        'PLNE': plne_algorithm,
        'SimulatedAnnealing': heuristic_sa,
    }

    return algorithms.get(algorithm_name, None)


def main():
    # Créer un parseur d'arguments pour le fichier d'entrée
    parser = argparse.ArgumentParser(
        description="Interface pour choisir un algorithme de résolution de la médiane de permutations.")
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="Chemin vers le fichier contenant les permutations.")
    args = parser.parse_args()

    # Lire les permutations à partir du fichier fourni
    permutations = read_permutations_from_file(args.file)

    # Afficher le message de bienvenue et les permutations
    print("\n*** Bienvenue ***\n")
    print("Vos permutations sont :")
    for i, perm in enumerate(permutations, 1):
        print(f"{i}: {perm}")

    # Afficher les algorithmes disponibles
    print("\nVoici les algorithmes que vous pouvez utiliser pour résoudre le problème :")
    algorithms = {
        '1': ('Best Of A', heuristic_best_of_a),
        '2': ('Borda', heuristic_borda_count),
        '3': ('Branch and Bound', branch_and_bound_recursive),
        '4': ('Copeland', heuristic_copeland),
        '5': ('CPLEX', solve_median_permutation_cplex),
        '6': ('Parcons', parcons_algorithm),
        '7': ('Pickaperm', pickaperm_algorithm),
        '8': ('PLNE', plne_algorithm),
        '9': ('Simulated Annealing', heuristic_sa)
    }
    for key, (name, _) in algorithms.items():
        print(f"{key} - {name}")

    # Demander à l'utilisateur de choisir un algorithme
    choice = input("\nVeuillez choisir un algorithme (1-9) : ")

    # Vérifier que le choix est valide
    if choice in algorithms:
        algorithm_name, algorithm_function = algorithms[choice]
        print(f"\nVous avez choisi : {algorithm_name}\n")
        result = algorithm_function(permutations)
        print(f"Le résultat de la permutation médiane est : {result}")
    else:
        print("\nChoix invalide. Veuillez réessayer en exécutant à nouveau le programme.")


def read_permutations_from_file(file_path):
    """
    Lit les permutations à partir d'un fichier texte.

    :param file_path: Chemin vers le fichier texte contenant les permutations.
    :return: Une liste de permutations.
    """
    permutations = []
    with open(file_path, 'r') as f:
        for line in f:
            permutations.append(list(map(int, line.strip().split())))
    return permutations
