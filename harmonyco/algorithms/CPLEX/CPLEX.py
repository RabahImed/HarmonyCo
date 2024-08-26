# Il ne faut pas oublier d'installer pip install cplex

import cplex
from cplex.exceptions import CplexError


def solve_median_permutation_cplex(permutations):
    """
    Utilise CPLEX pour calculer la médiane des permutations.

    Parameters:
    - permutations (list of lists): Liste des permutations à analyser.

    Returns:
    - list: La permutation médiane trouvée par CPLEX.
    """
    n = len(permutations[0])  # Taille des permutations
    m = len(permutations)  # Nombre de permutations

    # Créer un modèle CPLEX
    try:
        model = cplex.Cplex()
        model.set_problem_type(cplex.Cplex.problem_type.LP)
        model.set_results_stream(None)  # Désactiver les logs pour une exécution plus propre
        model.set_warning_stream(None)

        # Définir les variables de décision
        # x[i][j] est 1 si l'élément i est placé avant l'élément j dans la médiane, sinon 0
        variable_names = []
        for i in range(n):
            for j in range(i + 1, n):
                variable_names.append(f"x_{i}_{j}")

        # Ajout des variables binaires au modèle
        model.variables.add(names=variable_names, types=["B"] * len(variable_names))

        # Fonction objectif : Minimiser la somme des distances de Kendall-Tau
        objective = []
        for i in range(n):
            for j in range(i + 1, n):
                objective.append(0)  # Les coefficients seront mis à jour dans les contraintes
        model.objective.set_linear(list(zip(variable_names, objective)))
        model.objective.set_sense(model.objective.sense.minimize)

        # Contraintes pour chaque permutation
        constraints = []
        for k in range(m):
            for i in range(n):
                for j in range(i + 1, n):
                    if permutations[k][i] < permutations[k][j]:
                        # Ajouter contrainte x[i][j] = 1 si i précède j
                        constraints.append((f"x_{i}_{j}", 1))
                    else:
                        # Ajouter contrainte x[i][j] = 0 si j précède i
                        constraints.append((f"x_{i}_{j}", -1))

        # Ajout des contraintes au modèle
        model.linear_constraints.add(lin_expr=constraints, senses=["E"] * len(constraints))

        # Résolution du problème
        model.solve()

        # Récupération des résultats
        solution = model.solution.get_values()
        median_permutation = []
        for i in range(n):
            for j in range(i + 1, n):
                if solution[variable_names.index(f"x_{i}_{j}")] > 0.5:
                    median_permutation.append(i + 1)
                else:
                    median_permutation.append(j + 1)

        return median_permutation

    except CplexError as exc:
        print(exc)
        return None


# Exemple d'utilisation
if __name__ == "__main__":
    permutations = [
        [1, 3, 2, 4],
        [1, 2, 3, 4],
        [4, 2, 3, 1]
    ]
    median = solve_median_permutation_cplex(permutations)
    print(f"La permutation médiane trouvée est : {median}")
