#  Big Data et BI projet chez Diginamic
**Groupe 1: Bernardo ESTACIO ABREU, Fabrice BELLIN, Filip DABROWSKI**

## Description du projet

Ce projet vise à traiter des données issues d'une fromagerie en utilisant l'écosystème Hadoop et des bibliothèques Python. Le projet est organisé en plusieurs lots, et les lots 0 et 1 ont déjà été réalisés. Le nettoyage des données a été effectué dans le lot 0, suivi de l'utilisation de MapReduce pour le lot 1, afin de filtrer et analyser les commandes.

### Technologies utilisées:

- Hadoop : HDFS, MapReduce, MapReduce Streaming
- Docker : Pour l'environnement Hadoop
- Python : Utilisation de bibliothèques telles que `pandas`, `matplotlib`, `happybase`
- ELK Stack : ElasticSearch, Logstash, Kibana pour la visualisation (à venir)

### Objectifs :

- Nettoyage des données brutes fournies par une fromagerie (**Lot 0**)
- Analyse des commandes et extraction de statistiques à l'aide de MapReduce (**Lot 1 et 2**)
- Import des données dans une base NoSQL (**HBase**) et interrogation avec des scripts Python (**Lot 3**)
- Visualisation des données avec ELK Stack (**Lot 4**, à venir)

## Environnement d'exécution:

Le projet est déployé dans un environnement Hadoop, lancé à l'intérieur d'une image Docker sur une machine virtuelle (VM) de Diginamic. Voici les étapes pour configurer et exécuter le projet :

1. Accès à la VM Diginamic : Vous devez vous connecter à la VM fournie par Diginamic.
2. Lancer Docker : À l'intérieur de cette VM, un conteneur Docker est utilisé pour héberger l'environnement Hadoop.
3. Exécution de Hadoop : Une fois le conteneur en cours d'exécution, le framework Hadoop est prêt à être utilisé pour traiter les données.

## Structure du projet:

### Lot 0 : Nettoyage des données

Le travail dans le Lot 0 consiste à nettoyer les données brutes fournies par le client pour les préparer à l'analyse. Le fichier `datacleaner.py` effectue les tâches suivantes :

1. Suppression des accents (pour assurer la normalisation des noms de villes).
2. Validation des dates et correction des dates corrompues.
3. Remplacement des valeurs manquantes par des valeurs par défaut.
4. Suppression des doublons pour éviter les biais dans l'analyse.

#### Fichiers principaux :

`datacleaner.py` : Script qui traite les données en supprimant les erreurs.

### Lot 1 : Analyse avec MapReduce

Dans le Lot 1, l'objectif est d'analyser les commandes effectuées entre 2006 et 2010, en filtrant pour les départements 53, 61, et 28. Le but est d'identifier les 100 meilleures commandes par ville, en fonction de la somme des quantités et des valeurs de "timbrecde". Les résultats sont exportés dans un fichier Excel.

Fonctionnement :

- Mapper (`mapper1.py`): Ce script traite chaque ligne de données et extrait les informations pertinentes (ville, quantité, valeur "timbrecde").
- Reducer (`reducer1.py`): Ce script agrège les données pour chaque ville et sélectionne les 100 meilleures commandes.

Commande MapReduce :
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-input /input/cleaneddata.csv \
-output /output/lot1 \
-mapper "python3 /big_data_tp/lot1/mapper1.py" \
-reducer "python3 /big_data_tp/lot1/reducer1.py"
```

**COMMENT FILIP: VERIFY ABOVE !!!!!!!!!!!!!!!!!**

### Lot 2 : Analyse avec MapReduce (Période 2011-2016)
Lot 2 s'appuie sur le Lot 1, mais pour une nouvelle période (2011-2016) et de nouveaux départements (22, 49, et 53). Cette fois-ci, l'objectif est de filtrer les commandes sans "timbrecli" et de calculer la moyenne des quantités de chaque commande. Un graphique en forme de camembert (pie chart) est généré pour illustrer la distribution des commandes par ville.

Fonctionnement :

- Mapper (`mapper2.py`): Ce script fonctionne de manière similaire au mapper du Lot 1 mais exclut les lignes avec un "timbrecli".
- Reducer (`reducer2.py`): Ce script agrège les données en calculant la somme et la moyenne des quantités par ville.

Commande MapReduce :
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-input /input/cleaneddata_lot2.csv \
-output /output/lot2 \
-mapper "python3 /big_data_tp/lot2/mapper2.py" \
-reducer "python3 /big_data_tp/lot2/reducer2.py"
```

**TO VERIFY ABOVE!!!!!!!!!!!!!!!**

### Lot 3 : Importation dans HBase et Requêtes
Dans le Lot 3, les données filtrées sont importées dans une base NoSQL HBase pour faciliter les requêtes et l'analyse des tendances. Les scripts Python sont utilisés pour interroger la base HBase et générer des rapports en CSV, Excel et PDF.

Fonctionnement :
- Importation HBase (`import_hbase.py`): Ce script charge les données dans une table HBase et les prépare pour les requêtes.
- Requêtes Python (`hbase_queries.py`): Ce script interroge la base HBase pour obtenir les meilleures commandes de Nantes, le nombre total de commandes entre 2010 et 2015, et les statistiques du client avec le plus de "timbrecde".

#### Fichiers principaux :
- `import_hbase.py` : Script pour importer les données dans HBase.
- `hbase_queries.py` : Script pour exécuter les requêtes sur la base HBase.

Résultats à obtenir :
1. Meilleure commande de Nantes en 2020.
2. Nombre total de commandes effectuées entre 2010 et 2015.
3. Client avec le plus de frais de "timbrecde" (nom, prénom, nombre de commandes, somme des quantités).

### Lot 4 : Visualisation avec ELK Stack (à venir)
Le Lot 4 se concentre sur la visualisation des données avec la stack ELK (ElasticSearch, Logstash, Kibana). Un tableau de bord interactif sera créé pour afficher les résultats des requêtes et les graphiques basés sur les données analysées dans les lots précédents.


## Installation des dépendances :

Les dépendances nécessaires sont listées dans le fichier `requirements.txt`. Vous pouvez les installer avec la commande suivante :
```bash
pip install -r requirements.txt
```

## Exécution du projet:

**Comment: VERIFY!!!!! **

1. **Nettoyage des données (Lot 0) :**
```bash
python datacleaner.py
```

2. **Exécution de MapReduce (Lot 1 et 2) :** Utilisez les commandes Hadoop décrites ci-dessus pour exécuter les jobs MapReduce et analyser les commandes.

3. **Import dans HBase (Lot 3) :** Exécutez les scripts Python pour importer les données dans HBase et interroger la base.

4. **Visualisation des données (Lot 4) :** À venir.

## Structure des fichiers:

```graphhql
TP_BIG_DATA_FBELLIN_FILIP_BERNARDO/
│
├── .idea/                        # IDE specific folder (should be ignored in Git)
│
├── data/                         # Contains the raw data and cleaning scripts
│   ├── dataw_fro03               # Original CSV file with data
│   ├── dataw_fro03_mini_1000     # Subset of data for testing purposes
│   ├── datacleaner.py            # Script for cleaning and preprocessing the data
│   └── __init__.py               # Marks this directory as a Python package
│
├── lot1/                         # Lot 1 - Scripts and results for analysis between 2006 and 2010
│   ├── mapper1.py                # Mapper script for processing data for Lot 1
│   ├── reducer1.py               # Reducer script for aggregating data for Lot 1
│   ├── Results/                  # Folder to store the output results for Lot 1
│   └── __init__.py               # Marks this directory as a Python package
│
├── lot2/                         # Lot 2 - Scripts and results for analysis between 2011 and 2016
│   ├── mapper2.py                # Mapper script for processing data for Lot 2
│   ├── reducer2.py               # Reducer script for aggregating data for Lot 2
│   ├── plottingscript.py         # Script for generating pie chart for Lot 2
│   ├── results/                  # Folder to store the output results for Lot 2
│   └── __init__.py               # Marks this directory as a Python package
│
├── lot3/                         # Lot 3 - Scripts and results for data import and analysis in HBase
│   ├── hbase_lot3.py             # Script for importing data to HBase and querying
│   ├── results/                  # Folder to store the output results for Lot 3
│   └── __init__.py               # Marks this directory as a Python package
│
├── lot4/                         # Lot 4 - Placeholder for ELK Stack (under development)
│
├── tests/                        # Folder containing test scripts for unit testing
│   └── __init__.py               # Marks this directory as a Python package
│
├── fileconverter.py              # Python script to convert text data into Excel format (Lot 1)
├── fileconverterlot2.py          # Python script to convert text data into Excel format (Lot 2)
├── main.py                       # Main script to execute the overall pipeline (cleaning, MapReduce, HBase)
├── README.md                     # Documentation for the project
├── requirements.txt              # List of dependencies for the project
└── .gitignore                    # File to ignore unnecessary files in Git

```
