#  Big Data et BI projet chez Diginamic
**Groupe 1: Bernardo, Fabrice BELLIN, Filip DABROWSKI**

## Description du projet

Ce projet vise à traiter des données issues d'une fromagerie en utilisant l'écosystème Hadoop et des bibliothèques Python. Le projet est organisé en plusieurs lots, et les lots 0 et 1 ont déjà été réalisés. Le nettoyage des données a été effectué dans le lot 0, suivi de l'utilisation de MapReduce pour le lot 1, afin de filtrer et analyser les commandes.

### Technologies utilisées:

- Hadoop (HDFS, MapReduce)
- Docker (pour l'environnement Hadoop)
- Python (pandas, unidecode)
- MapReduce Streaming

## Environnement d'exécution:

Le projet est déployé dans un environnement Hadoop, lancé à l'intérieur d'une image Docker sur une machine virtuelle (VM) de Diginamic. Voici les étapes pour configurer et exécuter le projet :

1. Accès à la VM Diginamic : Vous devez vous connecter à la VM fournie par Diginamic.
2. Lancer Docker : À l'intérieur de cette VM, un conteneur Docker est utilisé pour héberger l'environnement Hadoop.
3. Exécution de Hadoop : Une fois le conteneur en cours d'exécution, le framework Hadoop est prêt à être utilisé pour traiter les données.

### Objectif du projet:
- Nettoyage des données et correction des erreurs (lot 0).
- Analyse des commandes via MapReduce (lot 1).

## Structure du projet:
### Lot 0:

Nettoyage des données à l’aide d’un script Python pour :

1. Enlever les accents.
2. Valider les dates.
3. Remplacer les valeurs manquantes par des valeurs par défaut.
4. Supprimer les doublons.

### Lot 1:

Utilisation de MapReduce pour :

- Filtrer les commandes entre 2006 et 2010 pour les départements 53, 61 et 28.
- Trier les données et extraire les 5 meilleures commandes par ville en fonction de la quantité et du montant du « timbrecde ».

## Dépendances:

Les dépendances sont gérées via un fichier requirements.txt. Vous pouvez les installer avec la commande suivante :
```bash
pip install -r requirements.txt
```

## Exécution du projet:

**Comment: ADD CONTENT HERE **

1. Nettoyage des données (Lot 0) :
```bash

```

2. Exécution de MapReduce (Lot 1) :

**Comment: UPDATE CONTENT HERE **

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-input /input/cleaneddata.csv \
-output /output/test
-mapper "python3 /big_data_tp/test/lot1/mapper1.py" \
-reducer "python3 /big_data_tp/test/lot1/reducer1.py"
```

## Structure des fichiers:

- `datacleaner.py`: Script de nettoyage des données.
- `mapper1.py`: Mapper pour le Lot 1.
- `reducer1.py`: Reducer pour le Lot 1.
