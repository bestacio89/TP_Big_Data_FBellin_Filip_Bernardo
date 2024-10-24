import happybase
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import re

# Elasticsearch connection details
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name in Elasticsearch

# Elasticsearch credentials
ES_USER = 'elastic'
ES_PASSWORD = '4Ex79eim'  # Change password for local pw  Elastic/kibana

# Create Elasticsearch client with authentication
es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USER, ES_PASSWORD)
)

# Connect to HBase
connection = happybase.Connection('node183721-env-1839015-2024-m05-etudiant07.sh1.hidora.com', 11972)
connection.open()
table = connection.table('dataw_fro')


# Function to scan HBase and convert to DataFrame
def fetch_data_from_hbase():
    data = []

    for key, data_dict in table.scan():
        # Convert HBase row data to a dictionary
        record = {column.decode('utf-8'): value.decode('utf-8') for column, value in data_dict.items()}
        data.append(record)

    return pd.DataFrame(data)


# Function to clean and rename DataFrame columns
def clean_column_names(df):
    new_columns = {}
    for col in df.columns:
        new_col = col.replace('info:', '')
        new_col = re.sub(r'[^a-zA-Z0-9]', '_', new_col)
        new_col = new_col.strip('_')  # Remove leading/trailing underscores
        new_columns[col] = new_col
    df.rename(columns=new_columns, inplace=True)


# Function to handle missing values and set data types
def process_dataframe(df):
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


# Fetch data from HBase
df = fetch_data_from_hbase()

# Handle NaN values by replacing them with 'N/A'
df.fillna('N/A', inplace=True)

# Clean the column names to make them Elasticsearch-friendly
clean_column_names(df)

# Process the DataFrame to handle missing values and set data types
process_dataframe(df)

# Convert DataFrame into a list of dictionaries for Elasticsearch bulk indexing
records = df.to_dict(orient='records')


# Function to generate Elasticsearch documents for bulk API
def generate_es_docs(records, index_name):
    for record in records:
        yield {
            "_index": index_name,
            "_source": record
        }


# Bulk index data into Elasticsearch in chunks
BATCH_SIZE = 500  # Number of records to index in each batch
try:
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        success, failures = helpers.bulk(es, generate_es_docs(batch, INDEX_NAME))
        print(f"Successfully indexed batch {i // BATCH_SIZE + 1}, indexed {success} documents.")
except Exception as e:
    print(f"Error indexing data: {e}")

# Close HBase connection
connection.close()
