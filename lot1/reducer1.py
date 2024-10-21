import sys

current_city = None
current_quantity_sum = 0
current_timbrecde_sum = 0

# Itération sur chaque ligne de l'entrée standard (la sortie du mapper)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la tabulation comme séparateur
    city, quantity, timbrecde = line.split("\t")

    # Convertir la quantité et 'timbrecde' en nombres
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 0  # Si la conversion échoue, mettre la quantité à 0
    try:
        timbrecde = float(timbrecde)
    except ValueError:
        timbrecde = 0  # Si la conversion échoue, mettre 'timbrecde' à 0

    # Si la ville est la même que la ville courante
    if city == current_city:
        # Additionner la quantité et 'timbrecde' aux sommes courantes
        current_quantity_sum += quantity
        current_timbrecde_sum += timbrecde
    else:
        # Sinon, afficher les résultats pour la ville courante
        if current_city:
            print("{}\t{}\t{}".format(current_city, current_quantity_sum, current_timbrecde_sum))

        # Mettre à jour la ville courante, la quantité et 'timbrecde'
        current_city = city
        current_quantity_sum = quantity
        current_timbrecde_sum = timbrecde

# Afficher les résultats pour la dernière ville
if current_city:
    print("{}\t{}\t{}".format(current_city, current_quantity_sum, current_timbrecde_sum))