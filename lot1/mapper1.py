import sys

# Itération sur chaque ligne de l'entrée standard (le fichier CSV)
for line in sys.stdin:
    # Supprimer les espaces en début et fin de ligne
    line = line.strip()
    # Diviser la ligne en champs en utilisant la virgule comme séparateur
    words = line.split(",")

    # Extraire l'année de la colonne 'datcde' (7ème colonne)
    try:
        year = int(words[7].split("-")[0])  # Convertir l'année en entier
    except (IndexError, ValueError):
        # Ignorer les lignes qui ne contiennent pas de date valide
        continue

    # Extraire le département de la colonne 'cpcli' (5ème colonne)
    department = words[4][:2]  # Prendre les 2 premiers chiffres du code postal

    # Extraire la quantité de la colonne 'qte' (16ème colonne)
    try:
        quantity = int(words[15])  # Convertir la quantité en entier
    except ValueError:
        # Ignorer les lignes qui ne contiennent pas de quantité valide
        continue

    # Extraire 'timbrecde' de la 10ème colonne
    try:
        timbrecde = float(words[9])  # Convertir 'timbrecde' en nombre à virgule flottante
    except ValueError:
        # Ignorer les lignes qui ne contiennent pas de 'timbrecde' valide
        continue

    # Vérifier si l'année est entre 2006 et 2010 et si le département est 53, 61 ou 28
    if 2006 <= year <= 2010 and department in ["53", "61", "28"]:
        # Afficher la ville (6ème colonne), la quantité et 'timbrecde' séparés par une tabulation
        print(f"{words[5]}\t{quantity}\t{timbrecde}")