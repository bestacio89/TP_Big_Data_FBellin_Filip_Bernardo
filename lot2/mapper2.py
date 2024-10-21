#!/usr/bin/env python
import sys
import random

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

    # Extraire la quantité de la colonne 'qte' (17ème colonne, index 16)
    try:
        quantity = int(words[16])
    except ValueError:
        continue

    # Vérifier si l'année est entre 2011 et 2016 et si le département est 22, 49 ou 53
    if 2011 <= year <= 2016 and department in ["22", "49", "53"]:
        # Afficher la ville (7ème colonne, index 6) et la quantité séparés par une tabulation
        print(words[6] + "\t" + str(quantity))