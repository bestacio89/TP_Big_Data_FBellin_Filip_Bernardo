#!/usr/bin/env python
import sys
from collections import defaultdict
import random

# Dictionnaire pour stocker les résultats par ville et code de commande (codcde)
city_results = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # {city: {codcde: [quantity_sum, order_count]}}

# Itération sur chaque ligne de l'entrée standard (le fichier "part-00000")
for line in sys.stdin:
    line = line.strip()
    try:
        department, city, codcde, quantity, timbrecde = line.split("\t")
    except ValueError:
        continue

    # Conversion de quantity et timbrecde
    try:
        quantity = int(quantity)
        timbrecde = float(timbrecde)
    except ValueError:
        continue

    # Ignorer si timbrecde est à 0 (indiquant timbrecli absent ou non renseigné)
    if timbrecde == 0:
        continue

    # Accumuler la somme des quantités et le nombre de commandes (pour la moyenne)
    city_results[city][codcde][0] += quantity  # Total quantity for codcde
    city_results[city][codcde][1] += 1  # Number of orders for codcde

# Collecter les commandes avec la somme des quantités et la moyenne des commandes
top_orders = []
for city, codcde_totals in city_results.items():
    for codcde, totals in codcde_totals.items():
        quantity_sum, order_count = totals
        avg_quantity = quantity_sum / order_count  # Calcul de la moyenne
        top_orders.append((city, codcde, quantity_sum, avg_quantity))

# Trier les commandes par la somme des quantités, puis par la quantité moyenne
top_orders.sort(key=lambda x: (-x[2], -x[3]))

# Sélectionner les 100 meilleures commandes
top_orders = top_orders[:100]

# Sélectionner aléatoirement 5% des meilleures commandes
num_to_select = max(1, int(len(top_orders) * 0.05))  # Minimum de 1 sélectionné
selected_orders = random.sample(top_orders, num_to_select)

# Afficher les résultats pour traitement ultérieur ou impression
for city, codcde, quantity_sum, avg_quantity in selected_orders:
    print("{}\t{}\t{}".format(city, quantity_sum, avg_quantity))
