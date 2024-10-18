import sys
import random

# Itération sur chaque ligne de l'entrée standard (le fichier CSV)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la virgule comme séparateur
    words = line.split(",")

    # Extraire l'année de la colonne 'datcde' (7ème colonne)
    try:
        year = int(words[7].split("-")[0])  # Convertir l'année en entier
    except (IndexError, ValueError):
        # Ignorer les lignes qui ne contiennent pas de date valide
        continue

    # Extraire le département de la colonne 'cpcli' (5ème colonne)
    department = words[4][:2]  # Prendre les 2 premiers chiffres du code postal

    # Extraire la quantité de la colonne 'qte' (16ème colonne)
    try:
        quantity = int(words[15])  # Convertir la quantité en entier
    except ValueError:
        # Ignorer les lignes qui ne contiennent pas de quantité valide
        continue

    # Vérifier si l'année est entre 2011 et 2016 et si le département est 22, 49 ou 53
    if 2011 <= year <= 2016 and department in ["22", "49", "53"]:
        # Afficher la ville (6ème colonne) et la quantité séparés par une tabulation
        print(f"{words[5]}\t{quantity}")