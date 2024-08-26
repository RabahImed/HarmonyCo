import math
import random
import numpy as np
import math
import os

def heuristic_sa(instance, verbose_detail=False, verbose_result=False, sa_mode=3):
    """
    Implémentation de l'algorithme de recuit simulé (Simulated Annealing) en Python.

    Parameters:
    - instance: Objet contenant les données de l'instance (par exemple, les permutations et les distances tabulées).
    - verbose_detail (bool): Si True, affiche des détails de l'exécution du SA.
    - verbose_result (bool): Si True, affiche les résultats du SA.
    - sa_mode (int): Mode de recuit simulé pour ajuster les paramètres (0 à 5).

    Returns:
    - None: Met à jour l'objet instance avec les résultats de l'algorithme SA.
    """
    sa_set = set()
    pi = None
    next_pi = None
    energy = 0
    delta_energy = 0
    num_runs = 0
    num_moves = 0
    ini_temperature = 0.0
    temperature = 0.0
    rand = 0.0
    alpha = 0.0

    p_min = None
    e_min = float('inf')
    global_e_min = float('inf')

    r1, r2 = 0, 0
    n = instance.n
    temp = 0
    set_size = instance.m
    a = [0] * n

    # Paramétrage du SA en fonction de m et n
    ini_temperature = (0.25 * set_size + 4.0) * n

    if set_size in [3, 4]:
        alpha = 0.99
    elif n <= 10:
        alpha = 0.95
    elif 11 <= n <= 16:
        alpha = 0.99
    elif 17 <= n <= 20:
        alpha = 0.999
    elif 21 <= n <= 24:
        alpha = 0.9995
    else:
        alpha = 0.9998

    if set_size == 3:
        num_moves = int(0.6 * math.pow(n, 3.0) - 11.0 * math.pow(n, 2.0) + 127.0 * n)
    elif set_size == 4:
        num_moves = int(0.9 * math.pow(n, 3.0) - 29.0 * math.pow(n, 2.0) + 435.0 * n - 1623)
    elif n <= 7:
        num_moves = 250
    elif 8 <= n <= 24:
        num_moves = int(90.0 * math.pow(n, 2.0) - 1540.0 * n + 7000)
    elif 25 <= n <= 38:
        num_moves = int(35.0 * math.pow(n, 2.0) - 660.0 * n + 31000)
    else:
        num_moves = int(80.0 * math.pow(n, 2.0) - 2300.0 * n + 27000)

    if set_size in [3, 4]:
        num_runs = math.ceil(0.05 * n + 2.0)
    elif n % 2 == 0:
        num_runs = math.ceil(0.007 * n * set_size + 3.0)
    else:
        num_runs = math.ceil(0.002 * n * set_size + 3.0)

    # Ajustement selon le mode SA
    if sa_mode == 0:
        ini_temperature = 0.0
        num_moves *= 0.33
        num_runs = 1
    elif sa_mode == 1:
        ini_temperature *= 0.5
        alpha *= 0.995
        num_moves *= 0.666
        num_runs = 1
    elif sa_mode == 2:
        ini_temperature *= 0.9
        num_moves *= 0.866
        num_runs = int(round(0.5 * num_runs) + 1)
    elif sa_mode == 3:
        pass  # paramètres par défaut
    elif sa_mode == 4:
        num_moves *= 1.1
        num_runs *= 2
    elif sa_mode == 5:
        ini_temperature *= 1.2
        num_moves *= 2
        num_runs *= 10
    else:
        print("SA error: SAmode not specified")

    # Initialisation avec une permutation aléatoire
    pi = create_random_permutation(n)
    if verbose_detail:
        print("SA Details:")

    for j in range(num_runs):
        if verbose_detail:
            print(f"Electron {j}")
            print("i \ttemp \tenergie")

        temperature = ini_temperature
        energy = pi.distance_to_set_matrix(instance.tabD)
        e_min = float('inf')

        for i in range(num_moves):
            # Sélection des indices r1 et r2
            r1 = random.randint(0, n - 1)
            r2 = random.randint(0, n - 1)

            # Calcul de delta_energy
            if r1 != r2:
                if r2 > r1:
                    temp = sum(instance.tabD[pi.get_tab()[r2] - 1][pi.get_tab()[u] - 1] for u in range(r1, r2))
                    delta_energy = -set_size * (r2 - r1) + 2 * temp
                else:
                    temp = sum(instance.tabD[pi.get_tab()[r2] - 1][pi.get_tab()[u] - 1] for u in range(r2 + 1, r1 + 1))
                    delta_energy = set_size * (r1 - r2) - 2 * temp
            else:
                delta_energy = 0

            # Décision d'acceptation du mouvement
            if delta_energy <= 0:
                # Création de la nouvelle permutation
                a = pi.get_tab().copy()
                if r1 != r2:
                    if r2 > r1:
                        temp = a[r2]
                        for u in range(r2, r1, -1):
                            a[u] = a[u - 1]
                        a[r1] = temp
                    else:
                        temp = a[r2]
                        for u in range(r2, r1):
                            a[u] = a[u + 1]
                        a[r1] = temp
                next_pi = Permutation(a)
                pi = next_pi
                energy += delta_energy
                if verbose_detail:
                    print(f"{i}\t{temperature:.2f}\t{energy}")
                if energy < e_min:
                    e_min = energy
                    p_min = pi
                    if e_min < global_e_min:
                        global_e_min = e_min
                        sa_set.clear()
            else:
                rand = random.random()
                if rand < math.exp(-delta_energy / temperature):
                    a = pi.get_tab().copy()
                    if r1 != r2:
                        if r2 > r1:
                            temp = a[r2]
                            for u in range(r2, r1, -1):
                                a[u] = a[u - 1]
                            a[r1] = temp
                        else:
                            temp = a[r2]
                            for u in range(r2, r1):
                                a[u] = a[u + 1]
                            a[r1] = temp
                    next_pi = Permutation(a)
                    pi = next_pi
                    energy += delta_energy
                    if verbose_detail:
                        print(f"{i}\t{temperature:.2f}\t{energy}")
            temperature *= alpha

        if energy > e_min:
            pi = p_min
            energy = e_min
        if energy == global_e_min:
            sa_set.add(pi)

    instance.add_solver_permutations(sa_set)
    instance.set_upper_bound(global_e_min)
    instance.sa_upper_bound = global_e_min

    if verbose_result:
        print(f"Simulated Annealing: ({global_e_min}) {pi}")
        print(
            f"SA heuristic parameters: {ini_temperature} initial temp, {alpha} cooling, {num_moves} moves, {num_runs} runs")


import numpy as np


def sa_average_solution_stat(arg1):
    """
    Calcule les statistiques moyennes des solutions pour plusieurs exécutions du recuit simulé (Simulated Annealing).

    Parameters:
    - arg1 (int): Nombre de cas à simuler.

    Returns:
    - None: Affiche les statistiques moyennes.
    """
    nb_cas = 1000  # par défaut
    nb_cas = arg1
    m = 3  # par défaut
    n = 10  # par défaut
    nb_electrons = 1
    nb_mvts = 700
    temperature = 500
    temperature = (m * 0.25 + 4.0) * n
    refroidissement = 0.99

    tab_average = np.zeros(nb_mvts)

    print(f"n={n}, m={m}, cas={nb_cas}, ele={nb_electrons}, mvt={nb_mvts}, tmp={temperature}, lam={refroidissement}")

    for cas in range(nb_cas):
        my_instance = Instance(m, n)
        heuristique_creer_sa_for_parameters2(my_instance, False, False, nb_electrons, nb_mvts, temperature,
                                             refroidissement, tab_average)

    tab_average /= nb_cas

    for i in range(nb_mvts):
        print(f"{i} \t {tab_average[i]:.2f}")


def heuristique_creer_sa_for_parameters2(instance, verbose_detail, verbose_result, nb_electrons, nb_mvts, temperature,
                                         refroidissement, tab_average):
    """
    Fonction simulant le recuit simulé avec les paramètres donnés. Cette fonction met à jour le tableau `tab_average`.

    Parameters:
    - instance: Instance de l'objet à simuler.
    - verbose_detail (bool): Si True, affiche les détails.
    - verbose_result (bool): Si True, affiche les résultats.
    - nb_electrons (int): Nombre d'électrons (simulations).
    - nb_mvts (int): Nombre de mouvements.
    - temperature (float): Température initiale.
    - refroidissement (float): Facteur de refroidissement.
    - tab_average (np.array): Tableau pour accumuler les résultats.

    Returns:
    - None: Met à jour `tab_average`.
    """
    for electron in range(nb_electrons):
        energie = 0
        for i in range(nb_mvts):
            # Simulation d'un mouvement ici
            delta_energie = np.random.rand() - 0.5  # Exemple: changement d'énergie aléatoire
            energie += delta_energie
            temperature *= refroidissement
            tab_average[i] += energie


class Instance:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        # Initialisation des autres attributs nécessaires


# Exemple d'utilisation
if __name__ == "__main__":
    sa_average_solution_stat(100)




def find_sa_parameters(arg1, arg2, refroidissement):
    """
    Calcule les paramètres optimaux pour l'algorithme de recuit simulé en simulant plusieurs cas.

    Parameters:
    - arg1 (int): Valeur de m (nombre d'éléments dans la permutation).
    - arg2 (int): Valeur de n (taille de la permutation).
    - refroidissement (float): Facteur de refroidissement de l'algorithme SA.

    Returns:
    - None: Affiche les résultats et les écrit dans des fichiers.
    """
    nb_cas = 500  # 1000/2
    m = arg1
    n = arg2
    nb_electrons = 1000
    nb_mvts = 100000
    temperature = (m * 0.25 + 4.0) * n

    rendu = 0
    dernieres_iterations = {}
    cumulative = 0

    nb_found = 0.0
    nb_not_found = 0.0
    total = 0.0

    first_found = 0.0
    last_found = 0.0
    scale_plus = 0.0
    scale_mult = 0.0
    nb_of_divisions = 500.0
    tab_dernieres_iterations = np.zeros(int(nb_of_divisions))

    mvt90accumule = -1
    mvt95accumule = -1

    print(
        f"start\nn={n}, m={m}, cas={nb_cas}, ele={nb_electrons}, mvt={nb_mvts}, tmp={temperature}, lam={refroidissement}")

    for cas in range(nb_cas):
        my_instance = Instance(m, n)
        heuristics_pack(my_instance, False)
        constraints_pack(my_instance, False, True)
        branch_and_bound(my_instance, False)
        heuristique_creer_sa_for_parameters(my_instance, False, False, nb_electrons, nb_mvts, temperature,
                                            refroidissement, dernieres_iterations)

    while -1 in dernieres_iterations:
        nb_not_found += dernieres_iterations[-1]
        del dernieres_iterations[-1]

    write_all_final_good_iterations_in_file(dernieres_iterations,
                                            f"SA_param_data/finalGoodIterations_m_{m}_n_{n}_ref_{refroidissement}.txt")

    first_found = min(dernieres_iterations.keys())
    last_found = max(dernieres_iterations.keys())
    scale_plus = first_found * 0.95
    scale_mult = (last_found - first_found) / (nb_of_divisions * 0.95) + 1.0

    while dernieres_iterations:
        key = min(dernieres_iterations.keys())
        if key >= ((rendu + 1) * scale_mult + scale_plus):
            rendu += 1
        else:
            nb_found += dernieres_iterations[key]
            tab_dernieres_iterations[rendu] += dernieres_iterations[key]
            del dernieres_iterations[key]

    total = nb_found + nb_not_found
    nb_found_affichage = nb_found * 100.0 / total
    nb_found = nb_found / 100.0 * total

    cumulative = 0
    for i in range(int(nb_of_divisions)):
        cumulative += tab_dernieres_iterations[i]
        if mvt90accumule == -1 and cumulative >= 0.90 * nb_found:
            mvt90accumule = int((i + 1) * scale_mult + scale_plus - 1)
        if mvt95accumule == -1 and cumulative >= 0.95 * nb_found:
            mvt95accumule = int((i + 1) * scale_mult + scale_plus - 1)

    resultat_affiche = f"n={n}, m={m}, cas={nb_cas}, ele={nb_electrons}, mvt={nb_mvts}, tmp={temperature}, lam={refroidissement}\n"
    resultat_affiche += f"nbFound: {nb_found_affichage:.2f}%, nbNotFound: {nb_not_found:.2f}%\n"
    resultat_affiche += f"-\nmvt90accumule: {mvt90accumule}\nmvt95accumule: {mvt95accumule}\nsucces: {nb_found_affichage:.2f}%\n"

    print(resultat_affiche)
    print("stop")

    write_sa_params_in_file(resultat_affiche, f"SA_param_data/SA_params_m_{m}_n_{n}_ref_{refroidissement}.txt")
    write_final_good_iterations_cdf_in_file(tab_dernieres_iterations, nb_of_divisions,
                                            f"SA_param_data/CDF_m_{m}_n_{n}_ref_{refroidissement}.txt")
    write_final_good_iterations_pdf_in_file(tab_dernieres_iterations, nb_of_divisions,
                                            f"SA_param_data/PDF_m_{m}_n_{n}_ref_{refroidissement}.txt")
    write_final_good_iterations_scale_in_file(tab_dernieres_iterations, nb_of_divisions, scale_mult, scale_plus,
                                              f"SA_param_data/Scale_m_{m}_n_{n}_ref_{refroidissement}.txt")


# Fonctions placeholder à implémenter
def heuristics_pack(instance, verbose):
    pass


def constraints_pack(instance, use_gd, verbose):
    pass


def branch_and_bound(instance, verbose):
    pass


def heuristique_creer_sa_for_parameters(instance, verbose_detail, verbose_result, nb_electrons, nb_mvts, temperature,
                                        refroidissement, dernieres_iterations):
    pass


def write_all_final_good_iterations_in_file(data, filename):
    with open(filename, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")


def write_sa_params_in_file(resultat_affiche, filename):
    with open(filename, 'w') as file:
        file.write(resultat_affiche)


def write_final_good_iterations_cdf_in_file(data, nb_of_divisions, filename):
    with open(filename, 'w') as file:
        cumulative = 0
        for i in range(int(nb_of_divisions)):
            cumulative += data[i]
            file.write(f"{i}\t{cumulative}\n")


def write_final_good_iterations_pdf_in_file(data, nb_of_divisions, filename):
    with open(filename, 'w') as file:
        for i in range(int(nb_of_divisions)):
            file.write(f"{i}\t{data[i]}\n")


def write_final_good_iterations_scale_in_file(data, nb_of_divisions, scale_mult, scale_plus, filename):
    with open(filename, 'w') as file:
        for i in range(int(nb_of_divisions)):
            file.write(f"{i * scale_mult + scale_plus}\t{data[i]}\n")


class Instance:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        # Initialisation des autres attributs nécessaires


# Exemple d'utilisation
if __name__ == "__main__":
    find_sa_parameters(3, 20, 0.95)
