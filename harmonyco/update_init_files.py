import os

def update_init_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"Checking directory: {dirpath}")  # Affiche chaque dossier parcouru
        init_file = os.path.join(dirpath, '__init__.py')

        if '__init__.py' not in filenames:
            print(f"Creating {init_file}")  # Affiche la création du fichier
            with open(init_file, 'w') as f:
                f.write("# This file allows Python to recognize this directory as a package.\n")
        else:
            print(f"Updating {init_file}")  # Affiche la mise à jour du fichier
            with open(init_file, 'r+') as f:
                content = f.read()
                if "# This file allows Python to recognize this directory as a package." not in content:
                    f.write("\n# This file allows Python to recognize this directory as a package.\n")
                else:
                    print(f"No changes needed for {init_file}")


# Exemple d'utilisation
if __name__ == "__main__":
    project_root = "C:/Users/Admin/PycharmProjets/HarmonyCo/harmonyco/algorithms"  # Change ce chemin en fonction de ton projet
    update_init_files(project_root)

