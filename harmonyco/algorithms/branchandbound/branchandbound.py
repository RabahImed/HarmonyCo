def branch_and_bound(instance, verbose=False):
    """
    Implémentation de l'algorithme Branch and Bound en Python pour calculer la médiane des permutations.

    Parameters:
    - instance: Objet contenant les données de l'instance (par exemple, les permutations et les distances tabulées).
    - verbose (bool): Si True, affiche des informations détaillées.

    Returns:
    - None: Met à jour l'objet instance avec les résultats de l'algorithme Branch and Bound.
    """
    # Initialisation
    n = instance.n
    response = 0
    resolution_mot = 0
    instance.nb_explored_nodes_bnb = 0
    instance.nb_max_nodes_bnb = 500000000
    memory_limit = 100000

    instance.nb_reject_gd = 0.0
    instance.nb_reject_triplets = 0.0
    instance.nb_reject_mot = 0.0
    instance.nb_reject_mot4 = 0.0
    instance.nb_reject_semi_dist_bi = 0.0
    instance.nb_reject_top_scores = 0.0
    instance.nb_reject_sub_scores = 0.0
    instance.nb_reject_spatial = 0.0
    instance.nb_reject = 0.0

    min_sub_scores_size = 4
    max_sub_scores_size = 6

    instance.top_scores = {}
    instance.sub_scores = {}

    if verbose:
        print("\n ***EXACT B&B SOLVER***\n")

    # Calcul des contraintes MOT
    for i in range(n):
        for j in range(n):
            if instance.tabC[i][j]:
                resolution_mot += 1

    resolution_exacte = 100.0 * (resolution_mot) / (n * (n - 1) / 2)
    if verbose:
        print(f"Resolution contraintes par contraintes: {resolution_mot}/{n * (n - 1) / 2} ({resolution_exacte:.2f}%)")
    instance.resolu_mot = f"{resolution_exacte:.2f}%"

    # Préparation des nombres et permutations pour le BnB
    nombres = []
    if len(instance.medians) == 0:
        nombres = list(range(1, n + 1))
    else:
        pi = instance.pick_a_random_median()
        nombres = [pi.get_tab()[i] for i in range(pi.get_size())]

    borne_inf = instance.simple_lower_bound
    borne_inf_add = instance.add3cyles_lower_bound
    if verbose:
        print(f"Gap = {instance.get_gap()} ({instance.get_relative_gap():.2f}%)")

    # Début de l'algorithme Branch and Bound
    vecteur_bit = BitVector(n)
    vecteur_bit.set_value(0)
    permu_en_cours = []

    if verbose:
        print("Starting the BnB...")

    response = branch_and_bound_recursive(instance, permu_en_cours, instance.apport, borne_inf_add, nombres, n, 0,
                                          borne_inf, vecteur_bit, False, 0)

    if instance.nb_explored_nodes_bnb >= instance.nb_max_nodes_bnb:
        if verbose:
            print("Node limit exceeded: BnB didn't finish optimizing")
            print(f"Gap = {instance.get_gap()} ({instance.get_relative_gap():.2f}%)")
    else:
        if verbose:
            print("BnB terminated correctly")
        instance.declare_is_optimal()
        if verbose:
            print(f"Kemeny Optimal Score: {instance.best_lower_bound}")

    # Compilation des résultats
    instance.nb_reject = (
            instance.nb_reject_gd + instance.nb_reject_triplets + instance.nb_reject_mot +
            instance.nb_reject_mot4 + instance.nb_reject_semi_dist_bi +
            instance.nb_reject_top_scores + instance.nb_reject_sub_scores + instance.nb_reject_spatial
    )

    if verbose:
        print(
            "Profil des rejets - " +
            f"GD : {instance.nb_reject_gd:.2f}%, triplets : {instance.nb_reject_triplets:.2f}%, MOT3e+LUBC : {instance.nb_reject_mot:.2f}%, " +
            f"SemiDistBI : {instance.nb_reject_semi_dist_bi:.2f}%, TopScs : {instance.nb_reject_top_scores:.2f}%, " +
            f"SubScs : {instance.nb_reject_sub_scores:.2f}%, Spatial : {instance.nb_reject_spatial:.2f}%, total : {instance.nb_reject:.2f}%"
        )
        print(
            f"Size of topScores = {len(instance.top_scores)}, size of subScores({min_sub_scores_size}-{max_sub_scores_size}) = {len(instance.sub_scores)}")
        print(f"Nb de noeuds explorés: {instance.nb_explored_nodes_bnb}\n")


def branch_and_bound_recursive(instance, current_permutation, contributions, lower_bound_add, numbers, left_to_set,
                               semi_dist, lower_bound, bit_vector, verbose_details, that_bnb_number):
    response = float('inf')
    candidate_response = float('inf')
    new_semi_dist = 0
    new_lower_bound = 0
    new_lower_bound_add = 0
    new_contributions = None
    last_element = 0
    before_last_element = 0
    element_to_put = 0

    permission_to_continue = True

    # Usage des contraintes
    use_gd = True
    use_triplets = True
    use_constraints = True
    use_semi_dist_bi_add = True
    use_top_scores = True

    numbers_after_first_cuts = []
    associated_lower_bounds = []
    associated_lower_bound = 0

    this_bnb_number = 0

    # Limite sur le nombre de noeuds explorés
    if instance.nb_explored_nodes_bnb >= instance.nb_max_nodes_bnb:
        return -1

    instance.nb_explored_nodes_bnb += 1

    # Pour l'affichage détaillé
    if verbose_details:
        print(f"{current_permutation}  sd: {semi_dist}   bi: {lower_bound}   add: {lower_bound_add}")

    # Feuille
    if left_to_set == 0:
        pi = Permutation(current_permutation)
        pi.set_dist(semi_dist)

        if semi_dist < instance.best_upper_bound:
            instance.set_upper_bound(semi_dist)
            instance.medians.clear()
            instance.add_solver_permutation(pi)
        elif semi_dist == instance.best_upper_bound:
            instance.add_solver_permutation(pi)

        response = semi_dist

    # Noeud
    else:
        if len(current_permutation) >= 1:
            last_element = current_permutation[-1]
        if len(current_permutation) >= 2:
            before_last_element = current_permutation[-2]

        for i in range(len(numbers)):
            element_to_put = numbers[i]
            permission_to_continue = True

            if use_gd:
                if len(current_permutation) >= 1:
                    permission_to_continue = instance.tab_contraintes_d[last_element - 1][element_to_put - 1]
                    if not permission_to_continue and verbose_details:
                        print(f"{current_permutation}({element_to_put})? nope: D/G")
                        instance.nb_reject_gd += 1

            if permission_to_continue and use_triplets and len(current_permutation) >= 2:
                if not instance.tab_triplets[before_last_element - 1][last_element - 1][element_to_put - 1]:
                    permission_to_continue = False
                    if verbose_details:
                        print(f"{current_permutation}({element_to_put})? nope: triplets")
                        instance.nb_reject_triplets += 1

            if permission_to_continue and use_constraints:
                for j in numbers:
                    if element_to_put != j and instance.tab_c[j - 1][element_to_put - 1]:
                        permission_to_continue = False
                        if verbose_details:
                            print(f"{current_permutation}({element_to_put})? nope: MOT3")
                            instance.nb_reject_mot += 1
                        break

            if permission_to_continue:
                new_permutation = current_permutation + [element_to_put]
                new_numbers = numbers[:]
                new_numbers.remove(element_to_put)

                new_lower_bound = lower_bound
                for k in new_numbers:
                    new_lower_bound -= min(instance.tab_d[element_to_put - 1][k - 1],
                                           instance.tab_d[k - 1][element_to_put - 1])

                new_semi_dist = semi_dist + sum(instance.tab_d[element_to_put - 1][j - 1] for j in new_numbers)

                if use_semi_dist_bi_add:
                    new_contributions = contributions[:]
                    new_lower_bound_add = lower_bound_add - contributions[element_to_put - 1]
                    if new_semi_dist + new_lower_bound + new_lower_bound_add >= instance.best_upper_bound:
                        if verbose_details:
                            print(
                                f"{current_permutation}({element_to_put})? nope: semiDist+borneInf+add ({new_semi_dist}+{new_lower_bound}+{new_lower_bound_add}={new_semi_dist + new_lower_bound + new_lower_bound_add} > {instance.best_upper_bound})")
                        permission_to_continue = False
                        instance.nb_reject_semi_dist_bi_add += 1

                if permission_to_continue:
                    associated_lower_bound = new_semi_dist + new_lower_bound + new_lower_bound_add
                    numbers_after_first_cuts.append(element_to_put)
                    associated_lower_bounds.append(associated_lower_bound)

        for i, element_to_put in enumerate(numbers_after_first_cuts):
            new_permutation = current_permutation + [element_to_put]
            new_numbers = numbers[:]
            new_numbers.remove(element_to_put)

            new_lower_bound = lower_bound
            for k in new_numbers:
                new_lower_bound -= min(instance.tab_d[element_to_put - 1][k - 1],
                                       instance.tab_d[k - 1][element_to_put - 1])

            new_semi_dist = semi_dist + sum(instance.tab_d[element_to_put - 1][j - 1] for j in new_numbers)

            new_contributions = contributions[:]
            new_lower_bound_add = lower_bound_add - contributions[element_to_put - 1]
            new_contributions[element_to_put - 1] = -1
            for j in new_numbers:
                for k in range(instance.tab_nb_triangle_associe[element_to_put - 1][j - 1]):
                    if instance.tab_triangle_associe[element_to_put - 1][j - 1][k] != 0:
                        if new_contributions[instance.tab_triangle_associe[element_to_put - 1][j - 1][k] - 1] != -1:
                            new_contributions[j - 1] -= instance.tab_triangle_add[element_to_put - 1][j - 1][
                                instance.tab_triangle_associe[element_to_put - 1][j - 1][k] - 1]

            new_bit_vector = bit_vector[:]
            new_bit_vector[element_to_put - 1] = True
            new_bit_vector.set_value(new_semi_dist)

            if use_top_scores:
                if instance.top_scores.get(new_bit_vector) is not None:
                    if instance.top_scores.get(new_bit_vector) < new_semi_dist:
                        if verbose_details:
                            print(
                                f"{current_permutation}({element_to_put})? nope: topScores before= {instance.top_scores.get(new_bit_vector)}  now= {new_semi_dist}")
                        permission_to_continue = False
                        instance.nb_reject_top_scores += 1
                    elif instance.top_scores.get(new_bit_vector) > new_semi_dist:
                        instance.top_scores[new_bit_vector] = new_semi_dist
                else:
                    if len(instance.top_scores) < instance.memory_limit:
                        instance.top_scores[new_bit_vector] = new_semi_dist
                    else:
                        instance.top_scores[new_bit_vector] = new_semi_dist

            if permission_to_continue:
                if verbose_details:
                    print(f"{current_permutation}({element_to_put})? ok")
                candidate_response = branch_and_bound_recursive(instance, new_permutation, new_contributions,
                                                                new_lower_bound_add, new_numbers, left_to_set - 1,
                                                                new_semi_dist, new_lower_bound, new_bit_vector,
                                                                verbose_details, this_bnb_number)

            if candidate_response != -1 and candidate_response < response:
                response = candidate_response

    return response
