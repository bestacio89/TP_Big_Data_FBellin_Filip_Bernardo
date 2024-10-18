import sys
import random

current_city = None
quantity_list = []

# Itération sur chaque ligne de l'entrée standard (la sortie du mapper)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la tabulation comme séparateur
    city, quantity = line.split("\t")

    # Convertir la quantité en nombre
    try:
        quantity = int(quantity)
    except ValueError:
        continue  # Ignorer les lignes qui ne contiennent pas de quantité valide

    # Si la ville est la même que la ville courante
    if city == current_city:
        # Ajouter la quantité à la liste des quantités pour cette ville
        quantity_list.append(quantity)
    else:
        # Sinon, traiter les données de la ville courante
        if current_city:
            # Calculer la moyenne des quantités pour un échantillon de 5% des commandes
            sample_size = int(len(quantity_list) * 0.05)
            if sample_size > 0:
                sample = random.sample(quantity_list, sample_size)
                average_quantity = sum(sample) / len(sample)
                print(f"{current_city}\t{average_quantity:.2f}")  # Afficher la ville et la moyenne

        # Mettre à jour la ville courante et réinitialiser la liste des quantités
        current_city = city
        quantity_list = [quantity]

# Traiter les données de la dernière ville
if current_city:
    # Calculer la moyenne des quantités pour un échantillon de 5% des commandes
    sample_size = int(len(quantity_list) * 0.05)
    if sample_size > 0:
        sample = random.sample(quantity_list, sample_size)
        average_quantity = sum(sample) / len(sample)
        print(f"{current_city}\t{average_quantity:.2f}")  # Afficher la ville et la moyenne