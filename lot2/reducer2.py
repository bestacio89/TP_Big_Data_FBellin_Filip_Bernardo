#!/usr/bin/env python
import sys
from collections import defaultdict
import random

# Dictionnaire pour stocker les résultats par ville et code de commande (codcde)
city_results = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # {city: {codcde: [quantity_sum, timbrecde_sum]}}

# Itération sur chaque ligne de l'entrée standard (la sortie du mapper)
for line in sys.stdin:
    line = line.strip()
    try:
        department, city, codcde, quantity, timbrecde = line.split("\t")
    except ValueError:
        continue

    if department not in ["22", "49", "53"]:
        continue

    try:
        quantity = int(quantity)
        timbrecde = float(timbrecde)
    except ValueError:
        continue

    city_results[city][codcde][0] += quantity
    city_results[city][codcde][1] += timbrecde

# Collecting top orders
top_orders = []
for city, codcde_totals in city_results.items():
    for codcde, totals in codcde_totals.items():
        quantity_sum, timbrecde_sum = totals
        top_orders.append((city, codcde, quantity_sum, timbrecde_sum))

# Sorting the top orders by quantity_sum and timbrecde_sum
top_orders.sort(key=lambda x: (-x[2], -x[3]))

# Selecting the top 100 orders
top_orders = top_orders[:100]

# Calculate the number of random entries to select (5% of 100)
num_to_select = max(1, int(len(top_orders) * 0.05))  # Ensure at least one order is selected

# Randomly select 5% of the top orders
selected_orders = random.sample(top_orders, num_to_select)

# Output the results for further processing
for city, codcde, quantity_sum, timbrecde_sum in selected_orders:
    print("{}\t{}\t{}".format(city, quantity_sum, timbrecde_sum))
