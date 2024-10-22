#!/usr/bin/env python
import sys

# Dictionnaire pour stocker les résultats catégorisés
results = {}

# Itération sur chaque ligne de l'entrée standard (le fichier CSV nettoyé)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la virgule comme séparateur
    words = line.split(",")

    # Vérification du nombre de colonnes (au moins 16)
    if len(words) < 16:
        continue

    # Extraire l'année de la colonne 'datcde' (8ème colonne, index 7)
    try:
        year = int(words[7].split("-")[0])
    except (IndexError, ValueError):
        continue

    # Extraire le département de la colonne 'cpcli' (5ème colonne, index 4)
    department = words[4][:2]

    # Extraire la quantité de la colonne 'qte' (15ème colonne, index 14)
    try:
        quantity = int(words[14])
    except ValueError:
        continue

    # Extraire 'timbrecde' de la 11ème colonne (index 10)
    try:
        timbrecde = float(words[10])
    except ValueError:
        continue

    # Extraire le code de commande 'codcde' de la 1ère colonne (index 0)
    codcde = words[0]

    # Vérifier si l'année est entre 2006 et 2010 et si le département est 53, 61 ou 28
    if 2006 <= year <= 2010 and department in ["53", "61", "28"]:
        city = words[5]  # Ville (7ème colonne, index 6)

        # Créer une clé pour le dictionnaire avec le département et la ville
        key = (department, city)

        # Ajouter la quantité, 'timbrecde' et 'codcde' (code de commande) à la catégorie correspondante
        if key not in results:
            results[key] = []

        results[key].append((quantity, timbrecde, codcde))

# Afficher les résultats catégorisés après avoir traité toutes les lignes
for (department, city), sales in results.items():
    for quantity, timbrecde, codcde in sales:
        print("{}\t{}\t{}\t{}\t{}".format(department, city, codcde, quantity, timbrecde))
