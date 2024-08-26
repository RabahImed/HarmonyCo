# HarmonyCo

**HarmonyCo** est une bibliothèque Python dédiée au calcul de la médiane de permutations à l'aide de divers algorithmes exacts et heuristiques. Ce projet est conçu pour fournir des solutions performantes et flexibles aux problèmes de permutations complexes, avec une attention particulière à l'efficacité et à la simplicité d'utilisation.

## Table des matières

- [Description du Projet](#description-du-projet)
- [Algorithmes Inclus](#algorithmes-inclus)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Exemples](#exemples)
- [Contributions](#contributions)
- [Licence](#licence)

## Description du Projet

HarmonyCo est conçu pour unifier plusieurs méthodes de calcul de la médiane de permutations dans une seule bibliothèque Python. L'objectif principal est de fournir des outils robustes pour le calcul de la médiane en utilisant une variété d'approches, y compris des algorithmes exacts comme Branch and Bound, et des heuristiques comme Simulated Annealing et Borda Count.

Le projet inclut également des outils pour l'analyse comparative des performances des différents algorithmes en fonction de la taille des données et des configurations spécifiques.

### Objectifs

- **Unification des Algorithmes** : Intégrer divers algorithmes pour le calcul de la médiane de permutations.
- **Efficacité** : Optimiser les performances pour les calculs complexes en utilisant des structures de données avancées comme l'arbre de Fenwick pour le calcul de la distance de Kendall-Tau.
- **Extensibilité** : Faciliter l'ajout de nouveaux algorithmes et méthodes au fur et à mesure que le projet évolue.

## Algorithmes Inclus

HarmonyCo inclut les algorithmes suivants pour le calcul de la médiane de permutations :

### 1. **BestOfA**
Un algorithme heuristique qui sélectionne la meilleure permutation parmi un ensemble donné en minimisant la distance de Kendall-Tau.

### 2. **Borda Count**
Un algorithme de comptage simple mais efficace qui attribue des points aux éléments en fonction de leur position dans les permutations et sélectionne la permutation avec le score le plus élevé.

### 3. **Branch and Bound**
Un algorithme exact qui explore l'espace des permutations de manière récursive pour trouver la permutation qui minimise la distance de Kendall-Tau.

### 4. **Copeland**
Un algorithme qui utilise la méthode de Copeland pour déterminer la permutation médiane en fonction des préférences majoritaires.

### 5. **CPLEX**
Un algorithme basé sur le solveur d'optimisation CPLEX d'IBM pour résoudre le problème de la médiane de permutations en formulant un problème de programmation linéaire mixte en nombres entiers (MILP).

### 6. **Simulated Annealing**
Une heuristique d'optimisation inspirée du processus de recuit métallurgique, qui explore l'espace des permutations de manière stochastique pour converger vers une solution proche de l'optimum.

### 7. **Parcons**
Une autre approche heuristique qui utilise les notions de consensus parmi les permutations pour trouver la médiane.

### 8. **Pickaperm**
Un algorithme heuristique basé sur une sélection aléatoire de permutations, combiné à une évaluation par un critère de distance.

### 9. **PLNE**
Un algorithme utilisant la programmation linéaire pour estimer la médiane de permutations en minimisant une fonction d'objectif linéaire.

## Installation

### Prérequis

Avant de commencer à utiliser HarmonyCo, assurez-vous d'avoir installé les dépendances suivantes :

- Python 3.7 ou supérieur
- `numpy` : Bibliothèque pour les calculs numériques
- `cplex` : Interface Python du solveur d'optimisation IBM CPLEX
- `scipy` : Pour des outils supplémentaires d'optimisation et de traitement scientifique
- `PuLP` : est une bibliothèque Python permettant de modéliser et résoudre des problèmes d'optimisation linéaire (PL) et linéaire en nombres entiers (PLNE). 

- Vous pouvez installer ces dépendances via pip :

```bash
pip install numpy cplex scipy PuLP
```

# Installation de HarmonyCo

Clonez le dépôt HarmonyCo à partir de GitHub :

```bash
git clone https://github.com/votreutilisateur/harmonyco.git
cd harmonyco
```

# Utilisation

HarmonyCo est conçu pour être simple à utiliser. Le fichier main.py permet de sélectionner l'algorithme souhaité et de l'exécuter sur un ensemble de permutations donné.
Exemple de Commande

```bash
python main.py -a BestOfA -f data/permutations.txt -o results/output.txt
```
Cette commande exécute l'algorithme BestOfA sur les permutations contenues dans le fichier permutations.txt et enregistre le résultat dans output.txt.

# Exemples
Calcul de la Médiane avec Branch and Bound

```python
from harmonyco.algorithms.branchandbound import branch_and_bound

permutations = [
    [1, 3, 2, 4],
    [4, 2, 3, 1],
    [2, 1, 4, 3]
]

result = branch_and_bound(permutations)
print(f"La permutation médiane est : {result}")
```

# Contributions

Les contributions au projet HarmonyCo sont les bienvenues. Veuillez suivre les étapes suivantes pour contribuer :

- Forkez le dépôt. 
- Créez une branche pour votre fonctionnalité (git checkout -b feature/AmazingFeature). 
- Commitez vos changements (git commit -m 'Add some AmazingFeature'). 
- Poussez la branche (git push origin feature/AmazingFeature). 
- Ouvrez une Pull Request.

# Exemple d'execution 

```less
*** Bienvenue ***

Vos permutations sont :
1: [1, 3, 2, 4]
2: [4, 2, 3, 1]
3: [2, 1, 4, 3]

Voici les algorithmes que vous pouvez utiliser pour résoudre le problème :
1 - Best Of A
2 - Borda
3 - Branch and Bound
4 - Copeland
5 - CPLEX
6 - Parcons
7 - Pickaperm
8 - PLNE
9 - Simulated Annealing

Veuillez choisir un algorithme (1-9) : _

```