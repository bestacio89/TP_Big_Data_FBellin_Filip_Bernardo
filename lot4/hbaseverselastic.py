import happybase
import pandas as pd
from elasticsearch import Elasticsearch, helpers



# Elasticsearch connection details
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name in Elasticsearch

# Elasticsearch credentials
ES_USER = 'elastic'
ES_PASSWORD = '4Ex79eim'  #Change password for local pw  Elastic/kibana

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


# Fetch data from HBase
df = fetch_data_from_hbase()

# Handle NaN values by replacing them with 0
df.fillna(0, inplace=True)

print(f"Fetched {len(df)} records from HBase and replaced NaN values with 0.")

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
        helpers.bulk(es, generate_es_docs(batch, INDEX_NAME))
        print(f"Successfully indexed batch {i // BATCH_SIZE + 1}")
except Exception as e:
    print(f"Error indexing data: {e}")

# Close HBase connection
connection.close()
