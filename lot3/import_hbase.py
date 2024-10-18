import csv
import happybase

# Connexion à HBase
connection = happybase.Connection('localhost')  # Remplacez 'localhost' par l'adresse de votre serveur HBase si nécessaire

# Créer la table HBase si elle n'existe pas
try:
    connection.create_table(
        'dataw_fro',
        {'info': dict()}  # Définir une famille de colonnes nommée 'info'
    )
except Exception as e:
    # Ignorer l'erreur si la table existe déjà
    if "already exists" not in str(e):
        raise e

# Ouvrir le fichier CSV nettoyé
with open('data/dataw_fro03_cleaned.csv', 'r', encoding='utf-8') as csvfile:
    # Créer un lecteur CSV
    reader = csv.DictReader(csvfile)

    # Obtenir la table HBase
    table = connection.table('dataw_fro')

    # Parcourir les lignes du fichier CSV
    for row in reader:
        # Construire la clé rowkey en utilisant 'codcli' et 'codcde'
        rowkey = f"{row['codcli']}-{row['codcde']}"  

        # Créer un dictionnaire avec les données de la ligne
        data = {
            f'info:{key}': value.encode()  # Encoder les valeurs en octets
            for key, value in row.items()
        }

        # Insérer la ligne dans la table HBase
        table.put(rowkey, data)

# Fermer la connexion à HBase
connection.close()