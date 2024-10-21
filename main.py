from data.datacleaner2 import nettoyer_fichier  # Importer la fonction de nettoyage
from lot3 import import_hbase  # Importer le module pour l'import dans HBase

def main():
    """Fonction principale pour exécuter les différentes étapes du TP."""

    # Nettoyage des données
    nettoyer_fichier("data/dataw_fro03.csv", "data/dataw_fro03_cleaned.csv")
    nettoyer_fichier("data/dataw_fro03_mini_1000.csv", "data/dataw_fro03_mini_1000_cleaned.csv")

    # Import des données dans HBase
    import_hbase.importer_donnees()

    # Lot 1 :
    # Exécuter le job MapReduce pour le lot 1 (à adapter à votre environnement Hadoop)
    # ...

    # Lot 2 :
    # Exécuter le job MapReduce pour le lot 2 (à adapter à votre environnement Hadoop)
    # ...

    # Lot 3 :
    # Exécuter les requêtes HBase (le code se trouve dans lot3/hbase_queries.py)
    # ...

    # Lot 4 :
    # Lancer Logstash et Kibana (à adapter à votre environnement ELK)
    # ...

if __name__ == "__main__":
    main()