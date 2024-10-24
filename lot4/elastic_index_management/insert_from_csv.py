import pandas as pd
import unidecode
import sys
from elasticsearch import Elasticsearch, helpers


def read_and_clean_csv(input_file, output_file):
    """Reads a CSV file, cleans the data, and saves the cleaned data to a new CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the cleaned CSV file.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file, encoding='utf-8')
        print(f"Initial number of rows: {len(df)}")

        # Remove accents from object type columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)

        # Convert dates and remove rows with invalid dates
        df['datcde'] = pd.to_datetime(df['datcde'], errors='coerce')
        df = df.dropna(subset=['datcde'])  # Drop rows with invalid dates
        print(f"Number of rows after date conversion: {len(df)}")

        # Replace NaN values with appropriate default values
        df['codcli'] = df['codcli'].fillna(0).astype('int32')
        df['genrecli'] = df['genrecli'].fillna('').astype('string')
        df['nomcli'] = df['nomcli'].fillna('').astype('string')
        df['prenomcli'] = df['prenomcli'].fillna('').astype('string')
        df['cpcli'] = df['cpcli'].fillna('').astype('string').str.zfill(5)
        df['villecli'] = df['villecli'].fillna('').astype('string')
        df['codcde'] = df['codcde'].fillna(0).astype('int32')
        df['timbrecli'] = df['timbrecli'].fillna(0.0).astype(float)
        df['timbrecde'] = df['timbrecde'].fillna(0.0).astype(float)
        df['Nbcolis'] = df['Nbcolis'].fillna(0).astype('int8')
        df['cheqcli'] = df['cheqcli'].fillna(0.0).astype(float)
        df['barchive'] = df['barchive'].fillna(False).astype('bool')
        df['bstock'] = df['bstock'].fillna(False).astype('bool')
        df['codobj'] = df['codobj'].fillna(0).astype('int32')
        df['qte'] = df['qte'].fillna(0).astype('int16')
        df['Colis'] = df['Colis'].fillna(0).astype('int32')
        df['libobj'] = df['libobj'].fillna('').astype('string')
        df['Tailleobj'] = df['Tailleobj'].fillna('').astype('string')
        df['Poidsobj'] = df['Poidsobj'].fillna(0.0).astype(float)
        df['points'] = df['points'].fillna(0).astype('int32')
        df['indispobj'] = df['indispobj'].fillna(False).astype('bool')
        df['libcondit'] = df['libcondit'].fillna('').astype('string')
        df['prixcond'] = df['prixcond'].fillna(0.0).astype(float)
        df['puobj'] = df['puobj'].fillna(0.0).astype(float)
        print(f"Number of rows after filling missing values: {len(df)}")

        # Remove duplicates
        df = df.drop_duplicates()
        print(f"Number of rows after removing duplicates: {len(df)}")

        # Save the cleaned data to a new CSV file
        df.to_csv(output_file, index=False)
        print(f"New file created successfully: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


def index_data_to_elasticsearch(csv_file, index_name, es_user, es_password, es_host='http://localhost:9200', batch_size=1000):
    """Indexes data from a CSV file to Elasticsearch in chunks.

    Args:
        csv_file (str): Path to the cleaned CSV file.
        index_name (str): Name of the Elasticsearch index.
        es_user (str): Elasticsearch username for authentication.
        es_password (str): Elasticsearch password for authentication.
        es_host (str): Elasticsearch host URL.
        batch_size (int): Number of records to index in each batch.
    """
    try:
        # Connect to Elasticsearch
        es = Elasticsearch([es_host], http_auth=(es_user, es_password))

        # Read the cleaned CSV file in chunks
        chunk_iterator = pd.read_csv(csv_file, chunksize=batch_size)

        for chunk_number, batch in enumerate(chunk_iterator):
            # Create actions for the bulk indexing
            actions = [
                {
                    "_index": index_name,
                    "_source": record.to_dict()
                }
                for _, record in batch.iterrows()
            ]

            # Only index if there are records to index
            if actions:
                # Use bulk helper to index data
                helpers.bulk(es, actions)
                print(f"Successfully indexed records {batch.index[0] + 1} to {batch.index[-1] + 1} into {index_name}.")
            else:
                print(f"No records to index for chunk {chunk_number}.")

    except Exception as e:
        print(f"An error occurred while indexing data: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Specify the input and output file paths
    input_file = '../../data/dataw_fro03/dataw_fro03.csv'  # Change this to your input file path
    output_file = '../../data/dataw_fro03/cleaneddata.csv'  # Desired output file path
    es_index_name = 'dataw_fro03'  # Specify your Elasticsearch index name

    # Elasticsearch credentials
    ES_USER = 'elastic'
    ES_PASSWORD = '4Ex79eim'

    read_and_clean_csv(input_file, output_file)
    index_data_to_elasticsearch(output_file, es_index_name, ES_USER, ES_PASSWORD)
