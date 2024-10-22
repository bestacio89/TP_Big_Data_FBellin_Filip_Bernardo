#!/usr/bin/env python
import sys
from collections import defaultdict

# Dictionnaire pour stocker les résultats par ville et code de commande (codcde)
city_results = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # {city: {codcde: [quantity_sum, timbrecde_sum]}}

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

    # Accumuler les totaux pour chaque ville et chaque codcde
    city_results[city][codcde][0] += quantity  # Somme des quantités
    city_results[city][codcde][1] += timbrecde  # Somme des timbrecde

# Pour chaque ville, créer une liste de résultats
top_orders = []

for city, codcde_totals in city_results.items():
    for codcde, totals in codcde_totals.items():
        quantity_sum, timbrecde_sum = totals
        top_orders.append((city, codcde, quantity_sum, timbrecde_sum))

# Trier les résultats par somme des quantités, puis par somme des timbrecde
top_orders.sort(key=lambda x: (-x[2], -x[3]))  # x[2] est quantity_sum, x[3] est timbrecde_sum

# Afficher les 100 meilleures commandes
for i, (city, codcde, quantity_sum, timbrecde_sum) in enumerate(top_orders[:100], start=1):
    print("{}. {}\t{}\t{}\t{}".format(i, city, codcde, quantity_sum, timbrecde_sum))
