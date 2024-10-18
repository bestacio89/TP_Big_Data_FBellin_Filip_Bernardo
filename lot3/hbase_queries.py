import happybase
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à HBase
connection = happybase.Connection('localhost')  # Remplacez 'localhost' par l'adresse de votre serveur HBase si nécessaire
table = connection.table('dataw_fro')  # Nom de la table HBase

# Question 1 : Meilleure commande de Nantes de l'année 2020
# Scanner la table HBase avec des filtres pour la date et la ville
rows = table.scan(filter=(
    "SingleColumnValueFilter('info', 'datcde', =, 'binary:2020') AND "
    "SingleColumnValueFilter('info', 'villecli', =, 'binary:Nantes')"
))

# Trouver la commande avec la plus grande quantité
best_order = max(rows, key=lambda row: int(row[1][b'info:qte'].decode()), default=None)
if best_order:
    print(f"Meilleure commande de Nantes en 2020 : {best_order}")
else:
    print("Aucune commande trouvée pour Nantes en 2020.")

# Question 2 : Nombre total de commandes entre 2010 et 2015, par année
results = {}
for year in range(2010, 2016):
    # Scanner la table HBase avec un filtre pour l'année
    rows = table.scan(filter=(
        f"SingleColumnValueFilter('info', 'datcde', >=, 'binary:{year}-01-01') AND "
        f"SingleColumnValueFilter('info', 'datcde', <=, 'binary:{year}-12-31')"
    ))
    results[year] = sum(1 for _ in rows)  # Compter le nombre de commandes pour chaque année

# Créer un barplot avec Matplotlib
plt.bar(results.keys(), results.values())
plt.xlabel("Année")
plt.ylabel("Nombre de commandes")
plt.title("Nombre total de commandes entre 2010 et 2015")
plt.show()  # Afficher le graphique

# Question 3 : Client avec le plus de frais de 'timbrecde'
# (Cette partie nécessite une requête plus complexe pour agréger les frais de 'timbrecde' par client)
# ...

# Fermer la connexion à HBase
connection.close()