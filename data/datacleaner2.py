import os
import pandas as pd
from unidecode import unidecode

# Load the CSV file
df = pd.read_csv('./dataw_fro03/dataw_fro03.csv', encoding='utf-8')

# Remove accents from string columns
df = df.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)

# Drop duplicate rows
df = df.drop_duplicates()

# Data shape after cleaning
records, features = df.shape
print(f"rows: {records}\nfeatures: {features}")

# Display the first 10 rows
print(df.head(10))

# Handle null values
# For string columns, replace NaNs with empty strings
df['genrecli'] = df['genrecli'].fillna('')
df['prenomcli'] = df['prenomcli'].fillna('')
df['Tailleobj'] = df['Tailleobj'].fillna('')

# For numerical columns, replace NaNs with appropriate values
df['Colis'] = df['Colis'].fillna(0)
df['Nbcolis'] = df['Nbcolis'].fillna(1)  # At least 1 item to ship
df['qte'] = df['qte'].fillna(1)
df['cheqcli'] = df['cheqcli'].fillna(0)
df['timbrecli'] = df['timbrecli'].fillna(0)
df['timbrecde'] = df['timbrecde'].fillna(0)
df['points'] = df['points'].fillna(0)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('./dataw_fro03/cleaneddata.csv', index=False)

# Data integrity checks
# Check for null values again
null_df = df[df.isnull().any(axis=1)]
print(null_df.shape)
print(null_df.isnull().sum())

# Unique values in columns with NaNs
print("Unique values in columns with missing data:")
print("genrecli:", null_df['genrecli'].unique())
print("prenomcli:", null_df['prenomcli'].unique())
print("timbrecde:", null_df['timbrecde'].unique())
print("cheqcli:", null_df['cheqcli'].unique())
print("Tailleobj:", null_df['Tailleobj'].unique())
print("points:", null_df['points'].unique())
