#!/usr/bin/env python
import sys
from collections import defaultdict

# Dictionnaire pour stocker les résultats par ville et code de commande (codcde)
city_results = defaultdict(list)

# Itération sur chaque ligne de l'entrée standard (la sortie du mapper)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la tabulation comme séparateur
    try:
        department, city, codcde, quantity, timbrecde = line.split("\t")
    except ValueError:
        # Ignorer les lignes qui ne peuvent pas être divisées en 5 champs
        continue

    # Vérification que le département est dans ["53", "61", "28"]
    if department not in ["53", "61", "28"]:
        continue

    # Convertir la quantité et 'timbrecde' en nombres
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 0  # Si la conversion échoue, mettre la quantité à 0
    try:
        timbrecde = float(timbrecde)
    except ValueError:
        timbrecde = 0  # Si la conversion échoue, mettre 'timbrecde' à 0

    # Ajouter la vente avec 'codcde', 'quantity' et 'timbrecde'
    city_results[city].append((quantity, timbrecde, codcde))

# Pour chaque ville, trier les résultats et obtenir les 5 meilleures ventes
for city, sales in city_results.items():
    # Trier les ventes par quantité, puis par timbrecde
    sorted_sales = sorted(sales, key=lambda x: (-x[0], -x[1]))

    # Afficher les 5 meilleures ventes par ville
    for i, (quantity, timbrecde, codcde) in enumerate(sorted_sales[:5], start=1):
        print("{}. {}\t{}\t{}\t{}".format(i, city, codcde, quantity, timbrecde))
