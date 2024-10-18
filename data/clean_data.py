import pandas as pd

def nettoyer_fichier(fichier_entree, fichier_sortie):
    """Nettoie et prépare les données du fichier CSV spécifié.

    Args:
      fichier_entree: Le chemin d'accès au fichier CSV d'entrée.
      fichier_sortie: Le chemin d'accès au fichier CSV de sortie nettoyé.
    """
    # Charger le fichier CSV
    df = pd.read_csv(fichier_entree, delimiter=',', header=0)

    # Convertir la colonne `datcde` en type `datetime`
    df['datcde'] = pd.to_datetime(df['datcde'], errors='coerce')

    # Supprimer les accents des colonnes textuelles
    columns_to_clean = ['genrecli', 'nomcli', 'prenomcli', 'villecli', 'libobj', 'Tailleobj', 'libcondit']
    for column in columns_to_clean:
        df[column] = df[column].astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # Supprimer les lignes contenant des valeurs nulles dans les colonnes spécifiées
    df.dropna(subset=columns_to_clean, inplace=True)

    # Remplacer les valeurs manquantes de la colonne `timbrecli` par la moyenne
    df['timbrecli'].fillna(df['timbrecli'].mean(), inplace=True)

    # Enregistrer le dataframe nettoyé dans un nouveau fichier CSV
    df.to_csv(fichier_sortie, index=False)

# Nettoyer les deux fichiers CSV
# Utilisation de chemins relatifs pour accéder aux fichiers CSV
nettoyer_fichier("./dataw_fro03/dataw_fro03.csv", "dataw_fro03/dataw_fro03_cleaned.csv")
nettoyer_fichier("./dataw_fro03_mini_1000/dataw_fro03_mini_1000.csv", "dataw_fro03_mini_1000/dataw_fro03_mini_1000_cleaned.csv")
